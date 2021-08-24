from fastapi import FastAPI
from application import router, config, logger
from application.util import pfmt
from typing import Dict, Any
from starlette.routing import Route, WebSocketRoute
from config.db import db_config
from config.mongo import mongo_config
from config.redis import redis_config
from utils.db import DbUtils
from utils.mongo import MongoUtils
from utils.redis import RedisUtils
from fastapi.middleware.cors import CORSMiddleware

"""
USE os.getenv() TO GET ENV VARS IN dev.cfg OR prod.cfg
"""

env: str = config.get('ENV')
app_name: str = config.get('APP_NAME')
description: str = config.get('DESCRIPTION')
version: str = config.get('VERSION')
debug: bool = config.get_bool('DEBUG')

fastapi_cfg: Dict[str, Any] = {
    'debug': env != 'prod',
    'title': app_name,
    'description': description,
    'version': version,
    'is_debug': debug
}

# init app
app = FastAPI(**fastapi_cfg)
router.register_controllers(app)
router.register_middlewares(app)

LOGGER = logger.get_application_logger()
DbUtils.default_config = db_config
MongoUtils.default_config = mongo_config
RedisUtils.default_config = redis_config

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def start_app():
    LOGGER.info('Launching application: %s\n%s' % (app_name, pfmt(fastapi_cfg)))
    # dump routers
    LOGGER.info('ROUTERS:')
    for route in app.routes:
        if isinstance(route, Route):
            LOGGER.info('HTTP Router %s: %s %s' %
                        (route.name, route.path, route.methods))
        elif isinstance(route, WebSocketRoute):
            LOGGER.info('WebSocket Router %s: %s ' %
                        (route.name, route.path))
    # dump user middlewares
    LOGGER.info('USER MIDDLEWARES:')
    for user_middleware in app.user_middleware:
        LOGGER.info(repr(user_middleware))


@app.on_event('shutdown')
async def shutdown_app():
    LOGGER.info('Shutdown application~')
