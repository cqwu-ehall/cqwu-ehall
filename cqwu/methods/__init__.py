from .auth import Auth
from .epay import EPay
from .users import Users
from .xg import XG


class Methods(
    Auth,
    EPay,
    Users,
    XG,
):
    pass
