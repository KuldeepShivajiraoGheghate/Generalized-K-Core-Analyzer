"""
Environment Verification Smoke Test (Phase 1).
Validates that Stage-1 prerequisite dependencies are properly installed.
"""

import sys

def verify_environment():
    print(f"Python version: {sys.version}")
    
    modules = ["networkx", "numpy", "pandas", "matplotlib", "scipy", "pytest"]
    success = True
    
    for mod_name in modules:
        try:
            mod = __import__(mod_name)
            version = getattr(mod, "__version__", "unknown")
            print(f"  [OK] {mod_name:12s} version: {version}")
        except ImportError as e:
            print(f"  [FAIL] {mod_name:12s} could not be imported: {e}")
            success = False
            
    if success:
        print("\n[SUCCESS] Environment verification completed successfully. All Stage-1 dependencies are verified.")
        return 0
    else:
        print("\n[ERROR] Environment verification failed. Missing dependencies.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_environment())
