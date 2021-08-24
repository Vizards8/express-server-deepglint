# 配置文件：DbConfig
from utils.db import DbConfig

db_config = DbConfig()
db_config.host = '127.0.0.1'
db_config.port = '3306'
db_config.username = 'root'
db_config.password = '666'
db_config.database = 'express'
db_config.echo = False
