from dao.base import BaseDao
from schema.base import ListArgsSchema, ListFilterSchema, ListOrderSchema


class DeviceListDao(BaseDao):
    pass

    def get_one(self, device_sn_list):
        args = ListArgsSchema()
        args.filters = []
        if device_sn_list is not None and len(device_sn_list) > 0:
            q_filter = ListFilterSchema(key='device_sn_list', condition='=', value=device_sn_list)
            args.filters.append(q_filter)
        args.orders = []
        q_order = ListOrderSchema(key='update_by', condition='acs')
        args.orders.append(q_order)
        return self.read_one(args)
