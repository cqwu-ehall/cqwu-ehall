from .gen_pay_qrcode import GenPayQrcode
from .get_balance import GetBalance
from .get_orders import GetOrders


class EPay(
    GenPayQrcode,
    GetBalance,
    GetOrders
):
    pass
