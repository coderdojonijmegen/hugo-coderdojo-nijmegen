import logging
from subprocess import Popen, PIPE

logger = logging.getLogger(__file__)


def execute(cmd: str, env=None) -> tuple[int, str, str]:
    return execute_args(cmd.split(), env)


def execute_args(args: list[str], env=None) -> tuple[int, str, str]:
    logger.debug(f"Executing: {args}")
    with Popen(args, env=env, stdout=PIPE, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
        return proc.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')
