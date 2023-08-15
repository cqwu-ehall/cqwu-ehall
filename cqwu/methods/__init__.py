from .auth import Auth
from .epay import EPay
from .pay import Pay
from .users import Users
from .webvpn import WebVPN
from .xg import XG


class Methods(
    Auth,
    EPay,
    Pay,
    Users,
    WebVPN,
    XG,
):
    pass
