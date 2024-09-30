from sanic import Sanic


class HelpDesk(Sanic):
    ...

appserver = HelpDesk(__name__)