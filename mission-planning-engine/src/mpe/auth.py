"""JWT authentication for the MPE operator API.

Two roles:
  viewer   — read-only access (GET endpoints only)
  operator — full access (GET + POST + DELETE)

Token flow:
  POST /api/auth/login  → access_token (15 min) + refresh_token (7 days)
  POST /api/auth/refresh → new access_token from valid refresh_token
  POST /api/auth/logout  → clears client token (stateless — just instruction)

User store:
  JSON file at users.json next to this module (or path set by MPE_USERS_FILE
  env var). Auto-created with two default users on first run:
    admin / admin123 (operator)
    viewer / viewer123 (viewer)

  IMPORTANT: Change default passwords before production deployment.
"""

from __future__ import annotations

import json
import os
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import hashlib
import hmac

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# ── Config ──────────────────────────────────────────────────────────────────

# Secret key — override via MPE_JWT_SECRET env var.
# Generated fresh if not set, meaning tokens invalidate on server restart.
# Set a persistent value in production.
_SECRET = os.environ.get(
    "MPE_JWT_SECRET",
    secrets.token_hex(32),
)
_ALGORITHM = "HS256"
_ACCESS_TTL  = 15 * 60          # 15 minutes
_REFRESH_TTL = 7 * 24 * 3600    # 7 days

# Users file — JSON list of {username, hashed_password, role}
_USERS_FILE = Path(
    os.environ.get(
        "MPE_USERS_FILE",
        Path(__file__).parent / "users.json",
    )
)

# Password hashing — PBKDF2-HMAC-SHA256, stdlib only (no bcrypt compat issues)
def _hash_password(password: str) -> str:
    """Hash a password with PBKDF2-HMAC-SHA256 + random salt."""
    import os
    salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000).hex()
    return f"pbkdf2$sha256$260000${salt}${digest}"


def _verify_password(password: str, hashed: str) -> bool:
    """Constant-time verify a password against a stored hash."""
    try:
        _, alg, iters, salt, stored = hashed.split("$")
        digest = hashlib.pbkdf2_hmac(alg, password.encode(), salt.encode(), int(iters)).hex()
        return hmac.compare_digest(digest, stored)
    except (ValueError, KeyError):
        return False

# Bearer scheme — auto_error=False so we can return a proper JSON 401
_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── User store ───────────────────────────────────────────────────────────────

def _default_users() -> list[dict]:
    return [
        {
            "username": "admin",
            "hashed_password": _hash_password("admin123"),
            "role": "operator",
        },
        {
            "username": "viewer",
            "hashed_password": _hash_password("viewer123"),
            "role": "viewer",
        },
    ]


def _load_users() -> list[dict]:
    if not _USERS_FILE.exists():
        users = _default_users()
        _USERS_FILE.write_text(json.dumps(users, indent=2))
        return users
    try:
        return json.loads(_USERS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return _default_users()


def _get_user(username: str) -> dict | None:
    for u in _load_users():
        if u["username"] == username:
            return u
    return None


# ── Token helpers ────────────────────────────────────────────────────────────

def _make_token(username: str, role: str, ttl: int, token_type: str) -> str:
    now = int(time.time())
    payload = {
        "sub": username,
        "role": role,
        "type": token_type,
        "iat": now,
        "exp": now + ttl,
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)


def _decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises HTTPException on any failure."""
    try:
        return jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── Dependency: current user ─────────────────────────────────────────────────

class CurrentUser(BaseModel):
    username: str
    role: str


def _extract_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser:
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = _decode_token(creds.credentials)
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expected access token",
        )
    return CurrentUser(username=payload["sub"], role=payload["role"])


def require_viewer(user: Annotated[CurrentUser, Depends(_extract_user)]) -> CurrentUser:
    """Allow viewer and operator roles."""
    return user


def require_operator(user: Annotated[CurrentUser, Depends(_extract_user)]) -> CurrentUser:
    """Allow operator role only."""
    if user.role != "operator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator role required",
        )
    return user


# ── Request/response models ──────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = _ACCESS_TTL
    role: str
    username: str


class RefreshRequest(BaseModel):
    refresh_token: str


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """Authenticate with username + password, receive JWT tokens."""
    user = _get_user(req.username)
    # Constant-time check — always run _verify_password even on unknown user
    stored_hash = user["hashed_password"] if user is not None else _hash_password("dummy")
    if user is None or not _verify_password(req.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access  = _make_token(user["username"], user["role"], _ACCESS_TTL,  "access")
    refresh = _make_token(user["username"], user["role"], _REFRESH_TTL, "refresh")
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        role=user["role"],
        username=user["username"],
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshRequest):
    """Exchange a valid refresh token for a new access token."""
    payload = _decode_token(req.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expected refresh token",
        )
    username = payload["sub"]
    user = _get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )
    access  = _make_token(user["username"], user["role"], _ACCESS_TTL,  "access")
    new_refresh = _make_token(user["username"], user["role"], _REFRESH_TTL, "refresh")
    return TokenResponse(
        access_token=access,
        refresh_token=new_refresh,
        role=user["role"],
        username=user["username"],
    )


@router.post("/logout")
async def logout(user: Annotated[CurrentUser, Depends(require_viewer)]):
    """Signal logout. Client must discard stored tokens."""
    return {"status": "logged_out", "username": user.username}


@router.get("/me")
async def whoami(user: Annotated[CurrentUser, Depends(require_viewer)]):
    """Return current user info."""
    return {"username": user.username, "role": user.role}
