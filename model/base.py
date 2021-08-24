from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, text, DECIMAL, Date
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    基础Model模型对象
    """
    __abstract__ = True

    id = Column(BIGINT(20), primary_key=True, comment='序号')
    create_by = Column(BIGINT(20), nullable=False, server_default=text("0"), default='0', comment='创建人')
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), default=datetime.now,
                         comment='创建时间')
    update_by = Column(BIGINT(20), nullable=False, server_default=text("0"), default='0', comment='更新人')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
                         default=datetime.now, comment='更新时间')
    del_flag = Column(TINYINT(1), nullable=False, server_default=text("0"), default='0', comment='软删')
