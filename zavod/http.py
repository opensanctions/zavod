import logging
import requests
from pathlib import Path
from zavod import settings

log = logging.getLogger(__name__)

# with self.http.get(
#                 url,
#                 stream=True,
#                 auth=auth,
#                 headers=headers,
#                 timeout=settings.HTTP_TIMEOUT,
#                 verify=False,


def fetch_file(url: str, name: str, data_path: Path = settings.DATA_PATH) -> Path:
    """Fetch a (large) file via HTTP to the data path."""
    out_path = data_path.joinpath(name)
    if out_path.exists():
        return out_path
    log.info("Fetching: %s", url)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as res:
        res.raise_for_status()
        with open(out_path, "wb") as fh:
            for chunk in res.iter_content(chunk_size=8192):
                fh.write(chunk)
    return out_path
