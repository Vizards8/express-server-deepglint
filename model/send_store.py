from sqlalchemy.sql import sqltypes

from model.base import *


class SendStore(Base):
    __tablename__ = 't_send_store'
    __table_args__ = {'comment': '日线数据'}


    store_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货仓ID')
    address = Column(String(255), nullable=False, server_default=text("''"), comment='地址')
    city = Column(String(64), nullable=False, server_default=text("''"), comment='城市')
    company = Column(String(64), nullable=False, server_default=text("''"), comment='公司')
    contact = Column(String(64), nullable=False, server_default=text("''"), comment='联系人')
    county = Column(String(256), nullable=False, server_default=text("''"), comment='县/区')
    mobile = Column(String(64), nullable=False, server_default=text("''"), comment='电话')
    province = Column(String(64), nullable=False, server_default=text("''"), comment='省份')
