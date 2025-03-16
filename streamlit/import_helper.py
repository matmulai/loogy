import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
parent_dir = str(Path(__file__).parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try to import the loogy package
try:
    import loogy
    print(f"Successfully imported loogy from {loogy.__file__}")
except ImportError as e:
    print(f"Failed to import loogy: {e}")

    # If we're in Streamlit Cloud, try to install the package
    if os.environ.get("IS_STREAMLIT_CLOUD", "false").lower() == "true":
        print("Attempting to install loogy package in Streamlit Cloud...")
        import subprocess
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "git+https://github.com/matmulai/loogy.git",
            ]
        )

        # Try importing again
        try:
            import loogy
            print(f"Successfully installed and imported loogy from {loogy.__file__}")
        except ImportError as e:
            print(f"Still failed to import loogy after installation: {e}") 
