from pathlib import Path

from publisher.env import HugoConf
from publisher.hugo import download_hugo


def test_download():
    hugo_exe = Path("hugo")
    hugo_exe.unlink(missing_ok=True)

    download_hugo(HugoConf(**{
        "version": "extended_0.131.0"
    }))

    assert hugo_exe.exists()

    hugo_exe.unlink(missing_ok=True)
    hugo_tar = Path("hugo.tar.gz")
    hugo_tar.unlink(missing_ok=True)
