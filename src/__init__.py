from src.cmd import Runner
from src.config import get_config
from src.pkg.arch.exception import CmdNotFound

if get_config().TESTING is True:
    runner = Runner()
else:
    program = get_config().CMD
    if program not in Runner.APP_MAP:
        raise CmdNotFound()

    app = Runner().APP_MAP[program]()
