import os
from pathlib import Path

DATA_PATH_ = os.environ.get("ZAVOD_DATA_PATH", "data")
DATA_PATH = Path(DATA_PATH_).resolve()
