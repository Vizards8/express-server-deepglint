import json
from typing import Optional

from fastapi import APIRouter, Depends
from application.controller import success, error
from application.logger import get_controller_logger
from config.redis import redis_config
from schema.base import ListArgsSchema, ListFilterSchema, ListOrderSchema
from schema.objects import ExpressJobSchema, ExpressProductSchema, ExpressJobProductSchema, DeviceSchema
from service.device_list import DeviceListService
from service.express_job import ExpressJobService
from service.express_product import ExpressProductService
from service.ship_order import OrderService
from utils.auth import get_auth_data
from utils.redis import RedisUtils
import pandas as pd
import numpy as np

router = APIRouter()
LOGGER = get_controller_logger('Express JOB')


@router.get('/api/express/job')
def get_express_job(dispatch_id: Optional[str] = '', shipment_id: Optional[str] = '', store_id: Optional[str] = '',
                    carrier: Optional[str] = '', with_tray: Optional[int] = -1, custom_name: Optional[str] = '',
                    status: Optional[int] = -1, station_id: Optional[str] = '', page_size: Optional[int] = -1,
                    page_index: Optional[int] = -1, auth_data: dict = Depends(get_auth_data)):
    """
    Args:
    args: 列表请求参数，详见ListArgsSchema
    """
    # 已揽件的标记status = 3
    check_job(auth_data)

    args = ListArgsSchema()
    args.size = page_size
    args.page = page_index
    args.filters = []
    key = ''
    if dispatch_id is not None and len(dispatch_id) > 0:
        q_filter = ListFilterSchema(key='dispatch_id', condition='=', value=dispatch_id)
        key = dispatch_id
        args.filters.append(q_filter)
    if shipment_id is not None and len(shipment_id) > 0:
        q_filter = ListFilterSchema(key='shipment_id', condition='=', value=shipment_id)
        args.filters.append(q_filter)

    if store_id is not None and len(store_id) > 0:
        q_filter = ListFilterSchema(key='store_id', condition='=', value=store_id)
        args.filters.append(q_filter)

    if carrier is not None and len(carrier) > 0:
        q_filter = ListFilterSchema(key='carrier', condition='=', value=carrier)
        args.filters.append(q_filter)

    if custom_name is not None and len(custom_name) > 0:
        q_filter = ListFilterSchema(key='custom_name', condition='like', value=custom_name)
        args.filters.append(q_filter)

    if station_id is not None and len(station_id) > 0:
        q_filter = ListFilterSchema(key='station_id', condition='=', value=station_id)
        args.filters.append(q_filter)

    if with_tray != -1:
        if with_tray == 0:
            with_tray = False
        elif with_tray == 1:
            with_tray = True
        q_filter = ListFilterSchema(key='with_tray', condition='=', value=with_tray)
        args.filters.append(q_filter)

    if status != -1:
        if status == 0:
            status = 0
        elif status == 1:
            status = 1
        elif status == 2:
            status = 2
        elif status == 3:
            status = 3
        q_filter = ListFilterSchema(key='status', condition='=', value=status)
        args.filters.append(q_filter)
    else:
        status = 2
        q_filter = ListFilterSchema(key='status', condition='!=', value=status)
        args.filters.append(q_filter)

    args.orders = []
    q_order = ListOrderSchema(key='update_by', condition='acs')
    args.orders.append(q_order)

    args.user_id = auth_data.get('user_id')
    LOGGER.debug('Get  Data list ')
    if len(args.filters) >= 0:
        data = None
        if key is not None and len(key) > 0:
            data = RedisUtils().get(key)
        if data:
            df = pd.read_json(data)
            df = df.to_json(orient="records", force_ascii=False, date_format='iso')
            json_obj = json.loads(df)
            return success(json_obj)
        else:
            df = ExpressJobService(auth_data).list(args)
            if df is None:
                return error(msg='Cannot found  Data list')
            else:
                df = df.drop(['create_by'], axis=1)
                df = df.drop(['create_time'], axis=1)
                df = df.drop(['update_by'], axis=1)
                df = df.drop(['update_time'], axis=1)
                if key is not None and len(key) > 0:
                    RedisUtils().set(key, df.to_json(force_ascii=False, date_format='iso'), redis_config.keeptime)
                df = df.to_json(orient="records", force_ascii=False, date_format='iso')
                json_obj = json.loads(df)
                return success(json_obj)
    else:
        return error(msg='请求参数为空')


@router.post('/api/express/file')
async def upload_json(*, data: dict, auth_data: dict = Depends(get_auth_data)):
    for job in data['data']:
        print(job)
        try:
            express_job_product = ExpressJobProductSchema()
            express_job_product.source_order_id = job['出库单号']
            express_job_product.custom_name = job['客户']
            express_job_product.product_code = job['存货编码']
            express_job_product.product_name = job['存货名称']
            express_job_product.product_model = job['规格型号']
            express_job_product.product_count = job['数量']
            express_job_product.dispatch_id = job['发货单id']
            express_job_product.store_id = job['货位编码']
            express_job_product.receipt_address = job['收货地址']
            express_job_product.receiver_person = job['收货人']
            express_job_product.receiver_phone = job['收货人电话']
            express_job_product.carrier = job['物流承运商']
            express_job_product.transportation = job['发运方式']
            create_express_job(express_job_product, auth_data)
        except:
            print('error:字段属性缺失')

    return success(msg='收到json,处理完毕')


# @router.post('/api/express/job')
# def create_express_job(*, express_job_product: ExpressJobProductSchema, auth_data: dict = Depends(get_auth_data)):
def create_express_job(express_job_product: ExpressJobProductSchema, auth_data):
    """
    Args:
    args: 列表请求参数，详见ListArgsSchema
    """
    if express_job_product is not None and express_job_product.dispatch_id is not None \
            and len(express_job_product.dispatch_id) > 0:
        express_job_data = ExpressJobSchema()
        existing_object = ExpressJobService(auth_data).get_one(express_job_product.dispatch_id)
        if existing_object is not None:
            express_job_data.id = existing_object.id
        if existing_object is not None and existing_object.status != 0:
            return error(msg='任务状态不为0')

        express_job_data.order_id = express_job_product.dispatch_id + '-' + express_job_product.source_order_id
        express_job_data.dispatch_id = express_job_product.dispatch_id
        express_job_data.store_id = express_job_product.store_id  # 仓库编码
        express_job_data.custom_name = express_job_product.custom_name
        express_job_data.receipt_address = express_job_product.receipt_address
        express_job_data.receiver_person = express_job_product.receiver_person
        express_job_data.receiver_phone = express_job_product.receiver_phone
        express_job_data.carrier = express_job_product.carrier
        express_job_data.transportation = express_job_product.transportation
        express_job_data.receipt_province = express_job_product.receipt_province
        express_job_data.receipt_city = express_job_product.receipt_city
        express_job_data.receipt_county = express_job_product.receipt_county
        express_job_data.create_by = auth_data.get('user_id')
        express_job_data.update_by = auth_data.get('user_id')
        if existing_object is None:
            ExpressJobService(auth_data).create(express_job_data)
        # else:
        # ExpressJobService(auth_data).update(express_job_data)

        express_product_data = ExpressProductSchema()
        # 一个出库单下面的产品有可能重复
        existing_product_object = ExpressProductService(auth_data).get_one(express_job_product.dispatch_id,
                                                                           express_job_product.product_code)
        if existing_product_object is not None:
            express_product_data.id = existing_product_object.id
        express_product_data.dispatch_id = express_job_product.dispatch_id
        express_product_data.product_code = express_job_product.product_code
        express_product_data.product_count = express_job_product.product_count
        express_product_data.product_model = express_job_product.product_model
        express_product_data.product_name = express_job_product.product_name
        if existing_product_object is None:
            ExpressProductService(auth_data).create(express_product_data)
        # else:
        # ExpressProductService(auth_data).update(express_product_data)

        return success(None, 'Success')
    else:
        return error(msg='请求参数为空')


@router.put('/api/express/job')
def update_express_job(*, express_job: ExpressJobSchema, auth_data: dict = Depends(get_auth_data)):
    """
    Args:
    args: 列表请求参数，详见ListArgsSchema
    """
    if express_job is not None:
        r_id = -1
        # if express_job.id is not None \
        #         and express_job.id >= 0:
        #     r_id = express_job.id
        if express_job.dispatch_id is not None \
                and len(express_job.dispatch_id) > 0:
            existing_object = ExpressJobService(auth_data).get_one(express_job.dispatch_id)
            if existing_object is not None:
                r_id = existing_object.id
        if r_id >= 0:
            # express_job_data = ExpressJobSchema()
            # express_job_data.id = r_id
            # express_job_data.status = express_job.status
            # ExpressJobService(auth_data).update(express_job_data)
            express_job.id = r_id
            ExpressJobService(auth_data).update(express_job)
            return success(None, 'Success')
        else:
            return error(msg='请求参数无效')
    else:
        return error(msg='请求参数为空')


@router.put('/api/express/job/lock/status')
def update_express_job_lock_status(*, express_job: ExpressJobSchema, auth_data: dict = Depends(get_auth_data)):
    """
    Args:
    args: 列表请求参数，详见ListArgsSchema
    """
    if express_job is not None:
        r_id = -1
        exist_lock_status = 0
        exist_station_id = ''
        # if express_job.id is not None \
        #         and express_job.id >= 0:
        #     r_id = express_job.id
        if express_job.dispatch_id is not None \
                and len(express_job.dispatch_id) > 0:
            existing_object = ExpressJobService(auth_data).get_one(express_job.dispatch_id)
            if existing_object is not None:
                r_id = existing_object.id
                exist_lock_status = existing_object.lock_status
                exist_station_id = existing_object.station_id
                # exist_station_id:当前加锁的station_id
        if r_id >= 0 and express_job.station_id is not None and len(express_job.station_id) > 0:
            if exist_lock_status == 1:
                if express_job.lock_status == 0:
                    if express_job.station_id == exist_station_id:
                        express_job_data = ExpressJobSchema()
                        express_job_data.id = r_id
                        express_job_data.lock_status = express_job.lock_status
                        express_job_data.station_id = ''
                        ExpressJobService(auth_data).update(express_job_data)
                        data = {'lock_status': 0, 'station_id': express_job_data.station_id}
                        return success(data, 'Success,解锁成功')
                    else:
                        data = {'lock_status': 1, 'station_id': exist_station_id}
                        return error(data, '无权解锁')
                else:
                    data = {'lock_status': 1, 'station_id': exist_station_id}
                    return error(data, msg='参数错误，当前已是锁定状态')
            elif exist_lock_status == 0:
                if express_job.lock_status == 1:
                    express_job_data = ExpressJobSchema()
                    express_job_data.id = r_id
                    express_job_data.station_id = express_job.station_id
                    express_job_data.lock_status = express_job.lock_status
                    ExpressJobService(auth_data).update(express_job_data)
                    data = {'lock_status': 1, 'station_id': express_job_data.station_id}
                    return success(data, 'Success，锁定成功')
                else:
                    data = {'lock_status': 0, 'station_id': ''}
                    return error(data, '参数错误，当前已是解锁状态')
        else:
            return error(msg='请求参数无效')
    else:
        return error(msg='请求参数为空')


@router.put('/api/express/product')
def update_express_product(*, express_product: ExpressProductSchema, auth_data: dict = Depends(get_auth_data)):
    """
    Args:
    args: 列表请求参数，详见ListArgsSchema
    """
    if express_product is not None:
        r_id = -1
        # if express_product.id is not None \
        #         and express_product.id >= 0:
        #     r_id = express_product.id
        if express_product.dispatch_id is not None \
                and len(express_product.dispatch_id) > 0:

            existing_product_object = ExpressProductService(auth_data).get_one(express_product.dispatch_id,
                                                                               express_product.product_code)
            if existing_product_object is not None:
                r_id = existing_product_object.id
        if r_id >= 0:
            express_product.id = r_id
            ExpressProductService(auth_data).update(express_product)
            return success(None, 'Success')
        else:
            return error(msg='请求参数无效')
    else:
        return error(msg='请求参数为空')


@router.get('/api/express/product')
def get_express_job_product(dispatch_id: Optional[str] = '', product_code: Optional[str] = '',
                            product_model: Optional[str] = '', page_size: Optional[int] = -1,
                            page_index: Optional[int] = -1, auth_data: dict = Depends(get_auth_data)):
    args = ListArgsSchema()
    args.size = page_size
    args.page = page_index
    args.filters = []
    key = ''
    if dispatch_id is not None and len(dispatch_id) > 0:
        q_filter = ListFilterSchema(key='dispatch_id', condition='=', value=dispatch_id)
        key = dispatch_id
        args.filters.append(q_filter)
    if product_code is not None and len(product_code) > 0:
        q_filter = ListFilterSchema(key='product_code', condition='=', value=product_code)
        args.filters.append(q_filter)
    if product_model is not None and len(product_model) > 0:
        q_filter = ListFilterSchema(key='product_model', condition='like', value=product_model)
        args.filters.append(q_filter)

    args.orders = []
    q_order = ListOrderSchema(key='update_by', condition='acs')
    args.orders.append(q_order)

    args.user_id = auth_data.get('user_id')
    LOGGER.debug('Get  Data list ')
    if len(args.filters) > 0:
        df = ExpressProductService(auth_data).list(args)
        if df is None:
            return error(msg='Cannot found  Data list')
        else:
            df = df.drop(['create_by'], axis=1)
            df = df.drop(['create_time'], axis=1)
            df = df.drop(['update_by'], axis=1)
            df = df.drop(['update_time'], axis=1)
            df = df.to_json(orient="records", force_ascii=False, date_format='iso')
            json_obj = json.loads(df)
            return success(json_obj)
    else:
        return error(msg='请求参数为空')


# 返回一个dispatch_id中的所有device_sn_list
@router.get('/api/express/sn')
def get_express_sn(product_id: Optional[str] = '', dispatch_id: Optional[str] = '', shipment_id: Optional[str] = '',
                   shipment_sub_id: Optional[str] = '',
                   page_size: Optional[int] = -1,
                   page_index: Optional[int] = -1, auth_data: dict = Depends(get_auth_data)):
    args = ListArgsSchema()
    args.size = page_size
    args.page = page_index
    args.filters = []
    key = ''
    if dispatch_id is not None and len(dispatch_id) > 0:
        q_filter = ListFilterSchema(key='dispatch_id', condition='=', value=dispatch_id)
        args.filters.append(q_filter)

    if product_id is not None and len(product_id) > 0:
        q_filter = ListFilterSchema(key='product_id', condition='=', value=product_id)
        args.filters.append(q_filter)

    if shipment_id is not None and len(shipment_id) > 0:
        q_filter = ListFilterSchema(key='shipment_id', condition='=', value=shipment_id)
        args.filters.append(q_filter)

    if shipment_sub_id is not None and len(shipment_sub_id) > 0:
        q_filter = ListFilterSchema(key='shipment_sub_id', condition='like', value=shipment_sub_id)
        args.filters.append(q_filter)

    args.orders = []
    q_order = ListOrderSchema(key='update_by', condition='acs')
    args.orders.append(q_order)

    args.user_id = auth_data.get('user_id')
    LOGGER.debug('Get  Data list ')
    if len(args.filters) > 0:
        df = DeviceListService(auth_data).list(args)
        if df is None:
            return error(msg='Cannot found  Data list')
        else:
            df = df.drop(['create_by'], axis=1)
            df = df.drop(['create_time'], axis=1)
            df = df.drop(['update_by'], axis=1)
            df = df.drop(['update_time'], axis=1)
            df = df.to_json(orient="records", force_ascii=False, date_format='iso')
            json_obj = json.loads(df)
            return success(json_obj)
    else:
        return error(msg='请求参数为空')


def check_job(auth_data):
    args = ListArgsSchema()
    args.filters = []

    q_filter = ListFilterSchema(key='status', condition='=', value=2)
    args.filters.append(q_filter)
    args.user_id = auth_data.get('user_id')

    express_jobs = ExpressJobService(auth_data).list(args)

    if express_jobs is not None:
        express_jobs = express_jobs.to_json(orient="records", force_ascii=False, date_format='iso')
        express_jobs = json.loads(express_jobs)
        for express_job in express_jobs:
            res = OrderService().check_order(express_job['shipment_id'])
            order_result = json.loads(str(res.content, 'utf8'))
            if res.status_code == 200:
                apiResultCode = order_result['apiResultCode']
                if apiResultCode != 'A1000':
                    return print(order_result['apiErrorMsg'])
                elif order_result['apiResultData'] is not None:
                    apiResultDataStr = order_result['apiResultData']
                    apiResultData = json.loads(apiResultDataStr)
                    if apiResultData['errorCode'] is not None and apiResultData['errorCode'] == 'S0000' \
                            and apiResultData['msgData'] is not None:
                        msgData = apiResultData['msgData']
                        routes = msgData['routeResps'][0]['routes']
                        if routes is not None:
                            for route in routes:
                                if route['opcode'] == "50":
                                    express_job['status'] = 3
                        else:
                            print('尚未揽件')
                    else:
                        print('api error')
                else:
                    print('api error')
            else:
                print('api error')
            if express_job['status'] == 3:
                print('update job: ' + express_job['id'])
                ExpressJobService(auth_data).update_by_model(express_job)
        else:
            print('下了订单却没有shipment_id?')
