from dao.base import BaseDao
from schema.base import ListArgsSchema, ListFilterSchema, ListOrderSchema


class SendStoreDao(BaseDao):
    pass

    def get_one(self, store_id):
        args = ListArgsSchema()
        args.filters = []
        q_filter = ListFilterSchema(key='store_id', condition='=', value=store_id)
        args.filters.append(q_filter)
        args.orders = []
        q_order = ListOrderSchema(key='update_by', condition='acs')
        args.orders.append(q_order)
        return self.read_one(args)
