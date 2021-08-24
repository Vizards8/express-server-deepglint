from controller import base, item, websocket, user, express_job, order
from middleware import connection, auth
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def register_controllers(app: FastAPI) -> None:
    """
    register controller callbacks to routers
    NOTE: /docs & /redoc are internal routers of fastapi
    :param app: fastapi app
    :return: None
    """
    app.include_router(base.router)
    app.include_router(item.router)
    app.include_router(user.router)
    app.include_router(express_job.router)
    app.include_router(order.router)
    app.include_router(websocket.router)


def register_middlewares(app: FastAPI) -> None:
    """
    register middlewares
    :param app: fastapi app
    :return: None
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware('http')(connection.calc_time)
    app.middleware('http')(auth.auth_token)
