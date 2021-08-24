from sqlalchemy.sql import sqltypes
from model.base import *


class ExpressJob(Base):
    __tablename__ = 't_express_job'
    __table_args__ = {'comment': '发货任务'}

    dispatch_id = Column(String(64), nullable=False, server_default=text("''"), comment='出库单号')
    shipment_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递单号')
    order_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货单号-出库单号')
    store_id = Column(String(64), nullable=False, server_default=text("''"), comment='仓库编码')
    with_tray = Column(sqltypes.BOOLEAN, nullable=False, server_default=text("''"), comment='是否是子母单')
    custom_name = Column(String(256), nullable=False, server_default=text("''"), comment='收货地址')
    receipt_address = Column(String(256), nullable=False, server_default=text("''"), comment='收货地址')
    receiver_person = Column(String(64), nullable=False, server_default=text("''"), comment='收货人')
    receiver_phone = Column(String(64), nullable=False, server_default=text("''"), comment='收货人电话')
    carrier = Column(String(64), nullable=False, server_default=text("''"), comment='物流承运商')
    transportation = Column(String(64), nullable=False, server_default=text("''"), comment='发运方式')
    station_id = Column(String(64), nullable=False, server_default=text("''"), comment='操作工位')
    status = Column(sqltypes.INTEGER, nullable=False, server_default=text("0"), comment='任务状态')
    lock_status = Column(sqltypes.INTEGER, nullable=False, server_default=text("0"), comment='任务锁定状态')
    shipment_msg_data = Column(String(2048), nullable=False, server_default=text("''"), comment='下单返回信息')
    receipt_province = Column(String(64), nullable=False, server_default=text("''"), comment='收货人省份')
    receipt_city = Column(String(64), nullable=False, server_default=text("''"), comment='收货人城市')
    receipt_county = Column(String(64), nullable=False, server_default=text("''"), comment='收货人县/区级行政区名称')
