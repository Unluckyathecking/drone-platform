#!/bin/bash
# install-sitl.sh — Install ArduPilot SITL on macOS for the Drone Project
#
# Usage:
#   cd ~/Documents/Drone\ project
#   chmod +x install-sitl.sh
#   ./install-sitl.sh
#
# After installation, run:
#   sim_vehicle.py -v ArduPlane --map --console
#   (wait for GPS lock)
#   python mission-planning-engine/sitl/fly_mission.py

set -e

echo "=== ArduPilot SITL Installer for macOS ==="
echo ""

# --- Step 1: Check/install Homebrew dependencies ---
echo "[1/5] Checking Homebrew dependencies..."
DEPS=(python@3.11 gcc ccache gawk git wget)
MISSING=()
for dep in "${DEPS[@]}"; do
    if ! brew list "$dep" &>/dev/null; then
        MISSING+=("$dep")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "  Installing: ${MISSING[*]}"
    brew install "${MISSING[@]}"
else
    echo "  All Homebrew dependencies present."
fi

# --- Step 2: Clone ArduPilot ---
ARDUPILOT_DIR="$HOME/ardupilot"
echo ""
echo "[2/5] Setting up ArduPilot repo..."
if [ -d "$ARDUPILOT_DIR" ]; then
    echo "  ArduPilot already cloned at $ARDUPILOT_DIR"
    cd "$ARDUPILOT_DIR"
    git pull --rebase 2>/dev/null || echo "  (pull skipped — might be on a detached HEAD)"
else
    echo "  Cloning ArduPilot (this takes a few minutes)..."
    git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git "$ARDUPILOT_DIR"
    cd "$ARDUPILOT_DIR"
fi

# --- Step 3: Update submodules ---
echo ""
echo "[3/5] Updating submodules..."
git submodule update --init --recursive

# --- Step 4: Install Python dependencies ---
echo ""
echo "[4/5] Installing Python dependencies..."
# Use the ArduPilot prereqs installer
if [ -f Tools/environment_install/install-prereqs-mac.sh ]; then
    Tools/environment_install/install-prereqs-mac.sh -y
else
    # Fallback: install manually
    pip3 install --user -r Tools/environment_install/requirements.txt 2>/dev/null || true
    pip3 install --user pymavlink MAVProxy empy==3.3.4 pexpect future
fi

# --- Step 5: Build ArduPlane SITL ---
echo ""
echo "[5/5] Building ArduPlane SITL..."
./waf configure --board sitl
./waf plane

# --- Add to PATH ---
PROFILE="$HOME/.zshrc"
SITL_BIN="$ARDUPILOT_DIR/Tools/autotest"
if ! grep -q "ardupilot/Tools/autotest" "$PROFILE" 2>/dev/null; then
    echo "" >> "$PROFILE"
    echo "# ArduPilot SITL" >> "$PROFILE"
    echo "export PATH=\"\$PATH:$SITL_BIN\"" >> "$PROFILE"
    echo "  Added $SITL_BIN to PATH in $PROFILE"
fi

# --- Install mission-planning-engine deps ---
echo ""
echo "[+] Installing mission-planning-engine dependencies..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/mission-planning-engine"
pip3 install --user -e ".[dev]"

echo ""
echo "=== Installation complete ==="
echo ""
echo "To run SITL:"
echo "  source ~/.zshrc"
echo "  sim_vehicle.py -v ArduPlane --map --console"
echo ""
echo "Then in another terminal:"
echo "  cd ~/Documents/Drone\\ project"
echo "  python mission-planning-engine/sitl/fly_mission.py"
echo ""
echo "In the MAVProxy console:"
echo "  mode auto"
echo "  arm throttle"
echo "  (watch the plane fly the triangle near Epsom)"
