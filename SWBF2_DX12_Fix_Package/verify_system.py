#!/usr/bin/env python3
"""
SWBF2 DX12 Fix - System Verification Script
==========================================

Run this script before applying the main fix to verify your system
is compatible and has all required components.

Usage: python verify_system.py
"""

import sys
import os
import platform
import ctypes
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.6+")
        return False

def check_windows_version():
    """Check if Windows version is compatible."""
    version = platform.version()
    release = platform.release()
    
    if platform.system() != "Windows":
        print(f"❌ OS: {platform.system()} - Windows required")
        return False
    
    if release in ["10", "11"]:
        print(f"✅ Windows {release} - Compatible")
        return True
    else:
        print(f"⚠️  Windows {release} - May work but not fully tested")
        return True

def check_admin_privileges():
    """Check if running with administrator privileges."""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin:
            print("✅ Administrator privileges - Available")
            return True
        else:
            print("⚠️  Administrator privileges - Not available (some fixes may not apply)")
            return True
    except:
        print("❓ Administrator privileges - Cannot determine")
        return True

def check_dependencies():
    """Check if required Python packages are available."""
    try:
        import psutil
        version = psutil.__version__
        print(f"✅ psutil {version} - Available")
        return True
    except ImportError:
        print("❌ psutil - Not installed (will be auto-installed)")
        return True  # Auto-install will handle this

def find_game_installation():
    """Check if SWBF2 installation can be found."""
    # Check parent directory first (since we're in a package subdirectory)
    parent_dir = Path.cwd().parent
    if (parent_dir / "starwarsbattlefrontii.exe").exists():
        print(f"✅ Game found in parent directory: {parent_dir}")
        return True
        
    # Check current directory
    current_dir = Path.cwd()
    if (current_dir / "starwarsbattlefrontii.exe").exists():
        print(f"✅ Game found in current directory: {current_dir}")
        return True
        
    # Check common Steam locations
    steam_paths = [
        Path(r"C:\Program Files (x86)\Steam\steamapps\common\STAR WARS Battlefront II"),
        Path(r"C:\Program Files\Steam\steamapps\common\STAR WARS Battlefront II"),
        Path(r"D:\Steam\steamapps\common\STAR WARS Battlefront II"),
        Path(r"E:\SteamLibrary\steamapps\common\STAR WARS Battlefront II")
    ]
    
    for path in steam_paths:
        if path.exists() and (path / "starwarsbattlefrontii.exe").exists():
            print(f"✅ Game found at: {path}")
            return True
            
    # Check EA/Origin locations
    ea_paths = [
        Path(r"C:\Program Files (x86)\EA Games\STAR WARS Battlefront II"),
        Path(r"C:\Program Files\EA Games\STAR WARS Battlefront II"),
        Path(r"C:\Program Files (x86)\Origin Games\STAR WARS Battlefront II"),
        Path(r"C:\Program Files\Origin Games\STAR WARS Battlefront II")
    ]
    
    for path in ea_paths:
        if path.exists() and (path / "starwarsbattlefrontii.exe").exists():
            print(f"✅ Game found at: {path}")
            return True
            
    print("❌ SWBF2 installation not found")
    print("   Make sure the game is installed and this fix package is in the game directory")
    return False

def check_disk_space():
    """Check if there's enough disk space for backups."""
    try:
        free_space = os.statvfs('.').f_frsize * os.statvfs('.').f_bavail
        if free_space > 100 * 1024 * 1024:  # 100 MB
            print("✅ Disk space - Sufficient for backups")
            return True
        else:
            print("⚠️  Disk space - Low (may affect backup creation)")
            return True
    except:
        # Windows doesn't have statvfs, use shutil
        try:
            import shutil
            _, _, free = shutil.disk_usage('.')
            if free > 100 * 1024 * 1024:  # 100 MB
                print("✅ Disk space - Sufficient for backups")
                return True
            else:
                print("⚠️  Disk space - Low (may affect backup creation)")
                return True
        except:
            print("❓ Disk space - Cannot determine")
            return True

def check_package_integrity():
    """Check if all required fix files are present."""
    required_files = [
        "SWBF2_DX12_Complete_Fix.py",
        "README_SWBF2_DX12_Fix.md",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if not missing_files:
        print("✅ Fix package - All files present")
        return True
    else:
        print(f"❌ Fix package - Missing files: {', '.join(missing_files)}")
        return False

def main():
    """Run all system verification checks."""
    print("=" * 60)
    print("SWBF2 DX12 Fix - System Verification")
    print("=" * 60)
    print()
    
    # Show current location for context
    print(f"📁 Running from: {Path.cwd()}")
    print(f"📦 Package directory: {Path.cwd().name}")
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Windows Version", check_windows_version),
        ("Administrator Privileges", check_admin_privileges),
        ("Python Dependencies", check_dependencies),
        ("Game Installation", find_game_installation),
        ("Package Integrity", check_package_integrity),
        ("Disk Space", check_disk_space)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"Checking {name}...")
        if check_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"VERIFICATION COMPLETE: {passed}/{total} checks passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 Your system is ready for the SWBF2 DX12 fix!")
        print("   You can proceed with running SWBF2_DX12_Complete_Fix.py")
    elif passed >= total - 1:
        print("✅ Your system should work with the fix.")
        print("   Minor issues detected but fix should still apply.")
    else:
        print("⚠️  Some issues detected. The fix may not work optimally.")
        print("   Please address the failed checks before proceeding.")
    
    print()
    print("Next steps:")
    print("1. Run: python SWBF2_DX12_Complete_Fix.py")
    print("2. Follow the on-screen instructions")
    print("3. Launch SWBF2 when prompted")
    
    print()
    print("💡 Directory Structure:")
    print("   📂 STAR WARS Battlefront II/          # Game directory")
    print("   ├── 🎮 starwarsbattlefrontii.exe     # Game executable")
    print("   └── 📂 SWBF2_DX12_Fix_Package/        # Fix package (current location)")
    print("       ├── 📄 SWBF2_DX12_Complete_Fix.py # Main fix script")
    print("       └── 📄 verify_system.py           # This script")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 