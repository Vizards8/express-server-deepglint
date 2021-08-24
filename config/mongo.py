# 配置文件：MongoConfig
from utils.mongo import MongoConfig

mongo_config = MongoConfig()
mongo_config.host = '10.10.100.118'
mongo_config.port = '27017'
mongo_config.username = 'root'
mongo_config.password = 'XianDai456'
mongo_config.database = 'tick'
