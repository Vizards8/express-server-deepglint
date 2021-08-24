
from service.base import BaseService

from dao.express_job import ExpressJobDao
from model.express_job import ExpressJob


class ExpressJobService(BaseService):
    def __init__(self, auth_data: dict = None):
        user_id = auth_data.get('user_id', 0)
        self.Model = ExpressJob
        self.dao = ExpressJobDao(user_id)
        self.dao.Model = ExpressJob

        super().__init__(user_id, auth_data)

    def get_one(self, dispatch_id):
        return self.dao.get_one(dispatch_id)
