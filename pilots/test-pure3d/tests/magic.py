"""Change the sys path so that `test` modules can import `control` modules."""
import sys
import os

# Get the parent directory of the current directory (where the test files are located)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory of the "src" folder to the Python module search path
sys.path.insert(0, parent_dir)
