from sqlalchemy.sql import sqltypes

from model.base import *


class DeviceList(Base):
    __tablename__ = 't_express_device_list'
    __table_args__ = {'comment': '设备详细列表'}

    product_code = Column(String(64), nullable=False, server_default=text("''"), comment='产品编码')
    device_sn_list = Column(String(2048), nullable=False, server_default=text("''"), comment='产品序列号')
    shipment_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递母单号')
    shipment_sub_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递子单号')
    dispatch_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递母单号')