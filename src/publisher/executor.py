import logging
from subprocess import Popen, PIPE

logger = logging.getLogger(__file__)


def execute(args, env=None) -> tuple[int, str, str]:
    logger.info(f"Executing: {args}")
    with Popen(args.split(" "), env=env, stdout=PIPE, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')
