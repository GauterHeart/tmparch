from src.cmd.executer.admin import AdminExec
from src.cmd.http import Http
from src.cmd.http_lock import HttpLock
from src.cmd.rabbitmq import AdminRabbit
from src.pkg.arch import Init


class Runner(Init):
    APP_MAP = {
        Http.name: Http,
        HttpLock.name: HttpLock,
        AdminExec.name: AdminExec,
        AdminRabbit.name: AdminRabbit,
    }
