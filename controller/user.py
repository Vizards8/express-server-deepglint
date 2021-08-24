from fastapi import APIRouter

from schema.auth import AuthDataSchema, LoginInputSchema
from service.user import UserService

router = APIRouter()


@router.post('/auth/user/login', response_model=AuthDataSchema, response_model_exclude_unset=True)
def login(*, login_input: LoginInputSchema):
    print(login_input)
    """
    用户登录
    :return:
    """
    return UserService().login_by_password(login_input.username, login_input.password)
