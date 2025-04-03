import os
import sys

test_dir = os.path.join(os.path.dirname(__file__), "..")
if test_dir not in sys.path:
    sys.path.insert(0, test_dir)
