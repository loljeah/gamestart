#!/usr/bin/env bash
# Kill all wine/gaming processes

patterns=(
    "Dead Space"
    "xalia"
    "winedevice"
    "wine64-preloader"
    "wine-preloader"
    "wineserver"
    "proton"
    "umu-run"
    "umu-shim"
    "pressure-vessel"
    "pv-adverb"
    "srt-bwrap"
    "gamescopereaper"
    "gamescope"
)

killed=0
for p in "${patterns[@]}"; do
    if pkill -9 -f "$p" 2>/dev/null; then
        ((killed++))
        echo "Killed: $p"
    fi
done

if [[ $killed -gt 0 ]]; then
    echo "Cleaned up $killed process groups"
    sleep 2
else
    echo "No gaming processes found"
fi
