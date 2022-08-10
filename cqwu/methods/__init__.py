from .auth import Auth
from .epay import EPay
from .users import Users


class Methods(
    Auth,
    EPay,
    Users
):
    pass
