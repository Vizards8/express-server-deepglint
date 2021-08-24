from dao.device_list import DeviceListDao
from model.device_list import DeviceList
from service.base import BaseService


class DeviceListService(BaseService):
    def __init__(self, auth_data: dict = None):
        user_id = auth_data.get('user_id', 0)
        self.Model = DeviceList
        self.dao = DeviceListDao(user_id)
        self.dao.Model = DeviceList

        super().__init__(user_id, auth_data)

    def get_one(self, device_sn_list):
        return self.dao.get_one(device_sn_list)

