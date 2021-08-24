from dao.base import BaseDao
from schema.base import ListArgsSchema, ListFilterSchema, ListOrderSchema


class ExpressJobDao(BaseDao):
    pass

    def get_one(self, dispatch_id):
        args = ListArgsSchema()
        args.filters = []
        q_filter = ListFilterSchema(key='dispatch_id', condition='=', value=dispatch_id)
        args.filters.append(q_filter)
        args.orders = []
        q_order = ListOrderSchema(key='update_by', condition='acs')
        args.orders.append(q_order)
        return self.read_one(args)
