import cqwu


class Order:
    def __init__(
        self,
        orderno: str = None,
        payproname: str = None,
        orderamt: float = None,
        createtime: str = None,
        payflag: str = "",
        **_
    ):
        """
        订单

        :param orderno: 订单编号
        :param payproname: 缴费项目
        :param orderamt: 缴费金额
        :param createtime: 订单生成时间
        :param payflag: 缴费状态
        """
        self.order_id = orderno
        self.project = payproname
        self.amount = orderamt / 100
        self.create_time = createtime
        self.status = cqwu.enums.OrderStatus(int(payflag))
