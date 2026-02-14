#!/usr/bin/env python3
"""Dead Space launcher for Sway/Wayland with gamescope."""

import os
import signal
import subprocess
import sys
import time

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Run: nix-shell")
    sys.exit(1)


# Game configuration
GAME_CONFIG = "/home/ljsm/Games/deadspace/deadspace.toml"
WINEPREFIX = "/home/ljsm/Games/deadspace"
GAME_EXE = "Dead Space.exe"

# Display settings
GAME_WIDTH = int(os.environ.get("GAME_WIDTH", 1920))
GAME_HEIGHT = int(os.environ.get("GAME_HEIGHT", 1080))
GAME_REFRESH = int(os.environ.get("GAME_REFRESH", 240))

# Feature toggles
ENABLE_HDR = os.environ.get("ENABLE_HDR", "0") == "1"
ENABLE_VRR = os.environ.get("ENABLE_VRR", "1") == "1"
ENABLE_MANGOHUD = os.environ.get("ENABLE_MANGOHUD", "0") == "1"
ENABLE_FSR = os.environ.get("ENABLE_FSR", "0") == "1"


def cleanup_previous_instances():
    """Kill ALL wine/gaming processes - nuclear option."""
    # Patterns to kill (order matters - kill children first)
    kill_patterns = [
        'Dead Space',
        'xalia',
        'winedevice',
        'wine64-preloader',
        'wine-preloader',
        'wineserver',
        'proton',
        'umu-run',
        'umu-shim',
        'pressure-vessel',
        'pv-adverb',
        'srt-bwrap',
        'gamescopereaper',
        'gamescope',
    ]

    killed_count = 0
    for pattern in kill_patterns:
        result = subprocess.run(
            ['pkill', '-9', '-f', pattern],
            capture_output=True
        )
        if result.returncode == 0:
            killed_count += 1

    if killed_count > 0:
        print(f"Cleaned up {killed_count} process groups")
        time.sleep(3)
    else:
        print("No previous instances found")


def get_environment():
    """Build environment variables for optimal AMD gaming."""
    env = os.environ.copy()

    # AMD RADV (Mesa Vulkan) optimizations for RDNA2
    env['AMD_VULKAN_ICD'] = 'RADV'
    env['RADV_PERFTEST'] = 'aco,video_decode'
    env['RADV_DEBUG'] = 'novrsflatshading'

    # DXVK optimizations
    env['DXVK_ASYNC'] = '1'
    env['DXVK_HUD'] = '0'
    env['DXVK_CONFIG_FILE'] = ''
    env['DXVK_FRAME_RATE'] = '0'

    # Wine/Proton optimizations
    env['WINE_FULLSCREEN_FSR'] = '0'
    env['WINE_FULLSCREEN_FSR_STRENGTH'] = '0'
    env['PROTON_NO_ESYNC'] = '1'
    env['PROTON_NO_FSYNC'] = '0'
    env['WINEFSYNC'] = '1'
    env['PROTON_ENABLE_NVAPI'] = '0'
    env['PROTON_HIDE_NVIDIA_GPU'] = '0'
    env['PROTON_USE_GAMEMODE'] = '1'
    env['WINE_LARGE_ADDRESS_AWARE'] = '1'

    # VKD3D-Proton (DX12) optimizations
    env['VKD3D_DEBUG'] = 'none'
    env['VKD3D_SHADER_DEBUG'] = 'none'
    env['VKD3D_FEATURE_LEVEL'] = '12_1'

    # System
    env['vblank_mode'] = '0'
    env['MANGOHUD'] = '0'

    # HDR
    if ENABLE_HDR:
        env['ENABLE_HDR_WSI'] = '1'

    # jemalloc if available
    jemalloc = '/run/current-system/sw/lib/libjemalloc.so'
    if os.path.exists(jemalloc):
        env['LD_PRELOAD'] = jemalloc

    return env


def build_gamescope_args():
    """Build gamescope command line arguments."""
    args = [
        'gamescope',
        '-W', str(GAME_WIDTH),
        '-H', str(GAME_HEIGHT),
        '-w', str(GAME_WIDTH),
        '-h', str(GAME_HEIGHT),
        '-r', str(GAME_REFRESH),
        '-f',
        '--force-grab-cursor',
        '--backend', 'sdl',
    ]

    if ENABLE_VRR:
        args.append('--adaptive-sync')

    if ENABLE_HDR:
        args.extend(['--hdr-enabled', '--hdr-itm-enable'])

    if ENABLE_FSR:
        args.extend(['-F', 'fsr', '--fsr-sharpness', '5'])

    if ENABLE_MANGOHUD:
        args.append('--mangoapp')

    args.extend(['--', 'umu-run', '--config', GAME_CONFIG])

    return args


def switch_workspace():
    """Switch to gaming workspace."""
    try:
        subprocess.run(['swaymsg', 'workspace', '5'], capture_output=True, timeout=2)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


def main():
    print("Dead Space Launcher")
    print(f"  Resolution: {GAME_WIDTH}x{GAME_HEIGHT}@{GAME_REFRESH}Hz")
    print(f"  VRR: {ENABLE_VRR}, HDR: {ENABLE_HDR}, FSR: {ENABLE_FSR}")
    print(f"  MangoHud: {ENABLE_MANGOHUD}")
    print(f"  GPU: AMD RX 6600 (RDNA2)")
    print()

    cleanup_previous_instances()
    switch_workspace()

    env = get_environment()
    args = build_gamescope_args()

    print(f"Launching: {' '.join(args[:5])}...")
    print()

    try:
        proc = subprocess.Popen(args, env=env)
        proc.wait()
    except KeyboardInterrupt:
        print("\nInterrupted, cleaning up...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        sys.exit(0)


if __name__ == '__main__':
    main()
