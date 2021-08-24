import hashlib
import uuid

from service.base import BaseService
from utils.obj2dict import obj2dict
from utils.redis import RedisUtils

from dao.user import UserDao
from model.user import User


class UserService(BaseService):
    def __init__(self, auth_data: dict = None):
        auth_data = dict() if not auth_data else auth_data

        user_id = auth_data.get('user_id', 0)
        self.Model = User
        self.dao = UserDao(user_id)
        self.dao.Model = User
        self.redis = RedisUtils()
        # self.wxapp = WxappUtils()

        super().__init__(user_id, auth_data)

    def _login_success(self, user):
        token = str(user.id) + str(uuid.uuid1())

        redis_data = {
            'user_id': user.id,
            'access': token
        }

        data = {
            'code': 200,
            'access': token
        }
        self.redis.set('token:' + token, redis_data, 360000)

        return data

    def login_by_password(self, username: str, password: str):
        """
        通过username、password进行登录
        :param username:
        :param password:
        :return:
        """

        user = self.dao.read_by_username(username)

        if not user:
            return {
                'code': 2008061621,
                'message': '用户不存在'
            }
        temp = hashlib.md5((user.username + password).encode(encoding='UTF-8')).hexdigest()
        print(temp)
        if user.password != temp:
            return {
                'code': 401,
                'message': '密码错误'
            }

        return self._login_success(user)
