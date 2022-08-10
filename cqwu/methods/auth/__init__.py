from .login_with_password import LoginWithPassword
from .login_with_cookie import LoginWithCookie
from .login_with_cookie_file import LoginWithCookieFile
from .export_cookie_to_file import ExportCookieToFile
from .oauth import Oauth


class Auth(
    LoginWithPassword,
    LoginWithCookie,
    LoginWithCookieFile,
    ExportCookieToFile,
    Oauth
):
    pass
