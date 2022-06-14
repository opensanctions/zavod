import os
from pathlib import Path

DATA_PATH_ = os.environ.get("ZAVOD_DATA_PATH", "data")
DATA_PATH = Path(DATA_PATH_)

HTTP_TIMEOUT = 1200
HTTP_USER_AGENT = "Mozilla/5.0 (zavod/ftm-datafactory)"
