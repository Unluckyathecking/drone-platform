#!/usr/bin/env python3
"""Verify PostgreSQL+PostGIS persistence end-to-end.

Run this script against a live PostGIS instance to confirm that the full
persistence stack works: schema creation, track writes, entity upserts,
spatial queries, FK constraints, and audit trail.

Usage:
    # Start PostGIS container (one-time)
    docker run -d --name mpe-db \
        -e POSTGRES_USER=mpe \
        -e POSTGRES_PASSWORD=mpe \
        -e POSTGRES_DB=mpe_c2 \
        -p 5432:5432 \
        postgis/postgis:16-3.4

    # Wait for it to be ready (~5s), then run:
    cd mission-planning-engine
    source .venv/bin/activate
    PYTHONPATH=src python scripts/verify_db.py

    # Or with a custom URL:
    PYTHONPATH=src python scripts/verify_db.py \
        --db-url postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone


PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"

_results: list[tuple[str, str, str]] = []


def _report(status: str, name: str, detail: str = "") -> None:
    _results.append((status, name, detail))
    icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "–"}.get(status, "?")
    print(f"  {icon} [{status}] {name}", f"({detail})" if detail else "")


async def verify(db_url: str) -> int:
    """Run all verification checks. Returns 0 if all pass, 1 if any fail."""
    print(f"\nConnecting to: {db_url.split('@')[-1]}")

    from mpe.db.engine import Database
    from mpe.db.models import AuditLog, Classification, Entity, TrackUpdate
    from mpe.db.repository import (
        AlertRepository,
        AuditRepository,
        EntityRepository,
        TrackRepository,
    )
    from sqlalchemy import select, func

    db = Database(url=db_url)

    # ------------------------------------------------------------------
    # 1. Connection + schema creation
    # ------------------------------------------------------------------
    print("\n--- Schema ---")
    try:
        await db.connect()
        _report(PASS, "connect()")
    except Exception as exc:
        _report(FAIL, "connect()", str(exc))
        print("\nCannot connect to database. Is PostGIS running?")
        print("  docker run -d --name mpe-db \\")
        print("      -e POSTGRES_USER=mpe -e POSTGRES_PASSWORD=mpe -e POSTGRES_DB=mpe_c2 \\")
        print("      -p 5432:5432 postgis/postgis:16-3.4")
        return 1

    try:
        await db.create_tables()
        _report(PASS, "create_tables() (includes PostGIS extension)")
    except Exception as exc:
        _report(FAIL, "create_tables()", str(exc))

    # ------------------------------------------------------------------
    # 2. Track writes and history
    # ------------------------------------------------------------------
    print("\n--- TrackRepository ---")
    entity_id = f"VERIFY-ADSB-{datetime.now(timezone.utc).strftime('%H%M%S')}"

    async with db.session() as session:
        try:
            repo = TrackRepository(session)
            update = await repo.record_update(
                entity_id, "adsb",
                lat=51.5074, lon=-0.1278,
                alt=10500.0, heading=270.0, speed_mps=245.0,
                raw_data={"callsign": "TEST123", "squawk": "1234"},
            )
            await session.commit()
            _report(PASS, "record_update() single track")
            assert update.entity_id == entity_id
        except Exception as exc:
            _report(FAIL, "record_update()", str(exc))

        try:
            # Write 4 more positions
            for i in range(4):
                await repo.record_update(
                    entity_id, "adsb",
                    lat=51.5074 + i * 0.01, lon=-0.1278 + i * 0.01,
                )
            await session.commit()
            _report(PASS, "record_update() bulk (5 total)")
        except Exception as exc:
            _report(FAIL, "record_update() bulk", str(exc))

        try:
            history = await repo.get_track_history(entity_id, hours=1)
            assert len(history) == 5, f"Expected 5, got {len(history)}"
            _report(PASS, f"get_track_history() returned {len(history)} rows")
        except Exception as exc:
            _report(FAIL, "get_track_history()", str(exc))

    # ------------------------------------------------------------------
    # 3. Entity upsert
    # ------------------------------------------------------------------
    print("\n--- EntityRepository ---")

    async with db.session() as session:
        try:
            repo = EntityRepository(session)
            entity = await repo.upsert(
                entity_id,
                domain="air",
                affiliation="neutral",
                threat_level=2,
                threat_category="low",
                confidence=0.85,
            )
            await session.commit()
            assert entity.id == entity_id
            _report(PASS, "upsert() create new entity")
        except Exception as exc:
            _report(FAIL, "upsert() create", str(exc))

        try:
            entity = await repo.upsert(
                entity_id,
                domain="air",
                affiliation="suspect",
                threat_level=7,
                threat_category="high",
                confidence=0.95,
            )
            await session.commit()
            assert entity.affiliation == "suspect"
            assert entity.threat_level == 7
            _report(PASS, "upsert() update classification")
        except Exception as exc:
            _report(FAIL, "upsert() update", str(exc))

        try:
            active = await repo.get_all_active(stale_minutes=1)
            assert any(e.id == entity_id for e in active)
            _report(PASS, f"get_all_active() found {len(active)} active entity/entities")
        except Exception as exc:
            _report(FAIL, "get_all_active()", str(exc))

        # PostGIS spatial query
        try:
            nearby = await repo.get_entities_near(lat=51.5074, lon=-0.1278, radius_km=10)
            _report(PASS, f"get_entities_near() PostGIS ST_DWithin returned {len(nearby)} result(s)")
        except Exception as exc:
            _report(FAIL, "get_entities_near() PostGIS spatial query", str(exc))

    # ------------------------------------------------------------------
    # 4. Classification FK constraint
    # ------------------------------------------------------------------
    print("\n--- Classification ---")

    async with db.session() as session:
        try:
            session.add(Classification(
                entity_id=entity_id,
                affiliation="suspect",
                threat_level=7,
                threat_category="high",
                confidence=0.95,
                reasoning=["Speed anomaly", "ICAO in watch list"],
                anomalies=[{"type": "excessive_speed", "description": "35 kts"}],
            ))
            await session.commit()
            _report(PASS, "Classification insert with FK to entities")
        except Exception as exc:
            _report(FAIL, "Classification FK insert", str(exc))

        try:
            result = await session.execute(
                select(Classification).where(Classification.entity_id == entity_id),
            )
            rows = list(result.scalars().all())
            assert len(rows) >= 1
            assert rows[-1].reasoning == ["Speed anomaly", "ICAO in watch list"]
            _report(PASS, "Classification JSON roundtrip (reasoning, anomalies)")
        except Exception as exc:
            _report(FAIL, "Classification JSON roundtrip", str(exc))

    # ------------------------------------------------------------------
    # 5. Alert lifecycle
    # ------------------------------------------------------------------
    print("\n--- AlertRepository ---")

    async with db.session() as session:
        try:
            repo = AlertRepository(session)
            alert = await repo.create_alert(
                entity_id=entity_id,
                alert_type="threat",
                severity=7,
                title="Suspect vessel detected",
                description="MMSI in watch list, speed anomaly",
            )
            await session.commit()
            assert alert.id is not None
            _report(PASS, f"create_alert() id={alert.id}")
        except Exception as exc:
            _report(FAIL, "create_alert()", str(exc))

        try:
            unacked = await repo.get_unacknowledged()
            assert any(a.entity_id == entity_id for a in unacked)
            _report(PASS, f"get_unacknowledged() returned {len(unacked)} alert(s)")
        except Exception as exc:
            _report(FAIL, "get_unacknowledged()", str(exc))

        try:
            # Acknowledge
            alert_to_ack = next(a for a in unacked if a.entity_id == entity_id)
            alert_to_ack.acknowledged = True
            alert_to_ack.acknowledged_by = "verify-script"
            alert_to_ack.acknowledged_at = datetime.now(timezone.utc)
            await session.commit()

            unacked_after = await repo.get_unacknowledged()
            assert not any(a.id == alert_to_ack.id for a in unacked_after)
            _report(PASS, "Alert acknowledge lifecycle")
        except Exception as exc:
            _report(FAIL, "Alert acknowledge", str(exc))

    # ------------------------------------------------------------------
    # 6. Audit trail
    # ------------------------------------------------------------------
    print("\n--- AuditRepository ---")

    async with db.session() as session:
        try:
            repo = AuditRepository(session)
            await repo.log(
                action="verify_script_run",
                actor="verify_db.py",
                target_type="entity",
                target_id=entity_id,
                details={"ts": datetime.now(timezone.utc).isoformat()},
            )
            await session.commit()
            _report(PASS, "audit log entry written")
        except Exception as exc:
            _report(FAIL, "audit log write", str(exc))

        try:
            from sqlalchemy import select as sa_select
            result = await session.execute(
                sa_select(AuditLog).where(AuditLog.target_id == entity_id),
            )
            rows = list(result.scalars().all())
            assert len(rows) >= 1
            _report(PASS, f"audit log query returned {len(rows)} entry/entries")
        except Exception as exc:
            _report(FAIL, "audit log query", str(exc))

    # ------------------------------------------------------------------
    # 7. Row counts
    # ------------------------------------------------------------------
    print("\n--- Row counts ---")

    async with db.session() as session:
        for model, label in [
            (TrackUpdate, "track_updates"),
            (Entity, "entities"),
            (Classification, "classifications"),
        ]:
            try:
                result = await session.execute(select(func.count()).select_from(model))
                count = result.scalar()
                _report(PASS, f"{label}: {count} row(s)")
            except Exception as exc:
                _report(FAIL, label, str(exc))

    await db.disconnect()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 50)
    passed = sum(1 for s, _, _ in _results if s == PASS)
    failed = sum(1 for s, _, _ in _results if s == FAIL)
    print(f"Results: {passed} passed, {failed} failed")

    if failed:
        print("\nFailed checks:")
        for status, name, detail in _results:
            if status == FAIL:
                print(f"  ✗ {name}: {detail}")
        return 1

    print("\nAll checks passed. PostgreSQL+PostGIS persistence is working.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify MPE DB persistence")
    parser.add_argument(
        "--db-url",
        default="postgresql+asyncpg://mpe:mpe@localhost:5432/mpe_c2",
        help="PostgreSQL+asyncpg URL",
    )
    args = parser.parse_args()
    sys.exit(asyncio.run(verify(args.db_url)))


if __name__ == "__main__":
    main()
