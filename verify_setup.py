#!/usr/bin/env python3
"""
AI Corp WebUI API Client - Setup Verification Script
This script verifies that the installation is working correctly.
"""

import sys
import subprocess
import importlib.util
import os
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    version = sys.version_info
    required = (3, 8)
    
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= required:
        print("✅ Python version is compatible")
        return True
    else:
        print(f"❌ Python {required[0]}.{required[1]}+ required")
        return False

def check_package_installed():
    """Check if the aicorp package is installed."""
    try:
        spec = importlib.util.find_spec("aicorp")
        if spec is not None:
            print("✅ aicorp package is installed")
            print(f"   Location: {spec.origin}")
            return True
        else:
            print("❌ aicorp package not found")
            return False
    except Exception as e:
        print(f"❌ Error checking package: {e}")
        return False

def check_command_available():
    """Check if aicorp command is available in PATH."""
    try:
        result = subprocess.run(['which', 'aicorp'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ aicorp command is available in PATH")
            print(f"   Location: {result.stdout.strip()}")
            return True
        else:
            print("❌ aicorp command not found in PATH")
            return False
    except Exception as e:
        print(f"❌ Error checking command: {e}")
        return False

def check_command_works():
    """Test if the aicorp command actually works."""
    try:
        result = subprocess.run(['aicorp', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ aicorp command executes successfully")
            return True
        else:
            print("❌ aicorp command failed to execute")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ aicorp command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def check_config_file():
    """Check if configuration file exists."""
    env_file = Path('.env')
    example_file = Path('.env.example')
    
    if env_file.exists():
        print("✅ .env configuration file exists")
        return True
    elif example_file.exists():
        print("⚠️  .env file missing, but .env.example found")
        print("   Run: cp .env.example .env")
        return False
    else:
        print("❌ No configuration files found")
        return False

def check_dependencies():
    """Check if required dependencies are available."""
    required_packages = ['requests', 'python-dotenv']
    all_good = True
    
    for package in required_packages:
        try:
            spec = importlib.util.find_spec(package.replace('-', '_'))
            if spec is not None:
                print(f"✅ {package} is installed")
            else:
                print(f"❌ {package} is missing")
                all_good = False
        except Exception as e:
            print(f"❌ Error checking {package}: {e}")
            all_good = False
    
    return all_good

def check_urllib3_compatibility():
    """Check urllib3 version for LibreSSL compatibility."""
    try:
        import urllib3
        version = urllib3.__version__
        major, minor = version.split('.')[:2]
        
        print(f"🔗 urllib3 version: {version}")
        
        if int(major) >= 2:
            print("⚠️  urllib3 v2.x detected - may cause LibreSSL warnings on macOS")
            print("   Recommended: urllib3 < 2.0.0 for LibreSSL compatibility")
            return False
        else:
            print("✅ urllib3 version is LibreSSL compatible")
            return True
            
    except ImportError:
        print("❌ urllib3 not found")
        return False
    except Exception as e:
        print(f"❌ Error checking urllib3: {e}")
        return False

def suggest_fixes():
    """Suggest common fixes for installation issues."""
    print("\n🔧 Common fixes:")
    print("   1. Add ~/.local/bin to PATH:")
    print("      echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.zshrc")
    print("      source ~/.zshrc")
    print()
    print("   2. Reinstall the package:")
    print("      pip3 install -e . --user --force-reinstall")
    print()
    print("   3. Create configuration file:")
    print("      cp .env.example .env")
    print()
    print("   4. Install missing dependencies:")
    print("      pip3 install -r requirements.txt")

def main():
    """Run all verification checks."""
    print("🔍 AI Corp WebUI API Client - Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Package Installation", check_package_installed),
        ("Command Availability", check_command_available),
        ("Command Functionality", check_command_works),
        ("Configuration File", check_config_file),
        ("Dependencies", check_dependencies),
        ("urllib3 Compatibility", check_urllib3_compatibility),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        if check_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your installation is working correctly.")
        print("\n🚀 Try running:")
        print("   aicorp --list-models")
        print("   aicorp --prompt \"Hello, world!\"")
    else:
        print("⚠️  Some checks failed. See suggestions below:")
        suggest_fixes()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
