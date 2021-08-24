from starlette.requests import Request
from starlette.responses import Response
from application.logger import get_middleware_logger
import json

from utils.auth import get_auth_data_by_authorization
from utils.request_log import create_log, update_log
from config.anonymous import anonymous_path_list

LOGGER = get_middleware_logger('auth')


async def auth_token(req: Request, call_next):
    response_type = 1
    response = Response(json.dumps({
        'code': 401,
        'message': 'Unauthorized',
    }), status_code=401)
    path = req.method + req.url.path

    # 判断是否可匿名访问
    if path in anonymous_path_list or path.find('GET/res/') == 0:
        response_type = 2
        response = await call_next(req)
    else:
        authorization = req.headers.get('authorization')
        if authorization and authorization.find('Bearer') >= 0:
            auth_list = authorization.split(' ')
            if len(auth_list) > 1:
                authorization = auth_list[1]
                authorization = authorization.strip()
        auth_data = get_auth_data_by_authorization(authorization, 360000)

        if auth_data:
            response_type = 3
            response = await call_next(req)

    '''
    if response_type == 1:
        log = await create_log(req)
        await update_log(log, response)
    '''

    return response
