from dao.send_store import SendStoreDao
from model.send_store import SendStore
from service.base import BaseService


class SendStoreService(BaseService):
    def __init__(self, auth_data: dict = None):
        user_id = auth_data.get('user_id', 0)
        self.Model = SendStore
        self.dao = SendStoreDao(user_id)
        self.dao.Model = SendStore

        super().__init__(user_id, auth_data)

    def get_one(self, store_id):
        return self.dao.get_one(store_id)
