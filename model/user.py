from model.base import *

from sqlalchemy.ext.declarative import declarative_base
DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = 't_user'
    __table_args__ = {'comment': '用户'}

    id = Column(BIGINT(20), primary_key=True, comment='序号')
    username = Column(String(255), nullable=False, server_default=text("''"), comment='账号')
    password = Column(String(255), nullable=False, server_default=text("''"), comment='密码')
