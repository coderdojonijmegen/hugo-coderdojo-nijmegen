import logging
import re
import tarfile
from pathlib import Path

from requests import get

from publisher.env import HugoConf
from publisher.executor import execute

HUGO_TAR_GZ = "hugo.tar.gz"
HUGO_DOWNLOAD_URL = "https://github.com/gohugoio/hugo/releases/download/v{hugo_base_version}/" \
                    "hugo_{hugo_version}_Linux-64bit.tar.gz"

logger = logging.getLogger(__file__)


def download_hugo(conf: HugoConf) -> None:
    hugo_base_version = re.compile(r"(\d+.\d+.\d+)").search(conf.version).group(0)

    download_url = HUGO_DOWNLOAD_URL.format(hugo_base_version=hugo_base_version, hugo_version=conf.version)

    logger.info(f"downloading {download_url} to {HUGO_TAR_GZ}")
    with open(HUGO_TAR_GZ, "wb") as hugo_tar_gz:
        hugo_tar_gz.write(get(download_url, allow_redirects=True).content)

    logger.info(f"extracting {HUGO_TAR_GZ}")
    with tarfile.open(HUGO_TAR_GZ, "r:gz") as tar:
        tar.extract("hugo", filter='data')
    hugo_path = Path("hugo").resolve()
    assert hugo_path.exists()
    logger.debug(hugo_path)


def run_hugo(target_dir: str) -> None:
    logger.info(f"building site into {target_dir}")
    ret_code, out, err = execute(f"./hugo --gc --minify --cleanDestinationDir -d {target_dir}/")
    if ret_code != 0:
        raise RuntimeError(f"Hugo error: {out} {err}")
