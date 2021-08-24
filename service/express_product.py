from dao.express_product import ExpressProductDao
from model.express_product import ExpressProduct
from service.base import BaseService


class ExpressProductService(BaseService):
    def __init__(self, auth_data: dict = None):
        user_id = auth_data.get('user_id', 0)
        self.Model = ExpressProduct
        self.dao = ExpressProductDao(user_id)
        self.dao.Model = ExpressProduct

        super().__init__(user_id, auth_data)

    def get_one(self, dispatch_id, product_code):
        return self.dao.get_one(dispatch_id, product_code)