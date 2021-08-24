from model.base import *
from sqlalchemy import Column, text, Date, FLOAT
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class ExpressProduct(Base):
    __tablename__ = 't_express_product'
    __table_args__ = {'comment': '节假日'}

    dispatch_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货单号')
    product_code = Column(String(64), nullable=False, server_default=text("''"), comment='存货编码')
    product_name = Column(String(128), nullable=False, server_default=text("''"), comment='存货名称')
    product_model = Column(String(64), nullable=False, server_default=text("''"), comment='规格型号')
    product_count = Column(FLOAT, nullable=False, server_default=text("''"), comment='数量')
    packed_count = Column(FLOAT, nullable=False, server_default=text("''"), comment='已打包数量')
