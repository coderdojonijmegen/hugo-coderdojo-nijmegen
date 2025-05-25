import logging
from subprocess import Popen
from typing import Any

logger = logging.getLogger(__file__)

def execute(args, env=None) -> tuple[int | Any, bytes, bytes]:
    logger.info(f"Executing: {args}")
    with Popen(args, env=env) as proc:
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout, stderr
