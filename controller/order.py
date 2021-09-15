import json
import uuid

from fastapi import Depends, APIRouter

from application.controller import error, success
from application.logger import get_controller_logger
from schema.base import ListArgsSchema, ListFilterSchema, ListOrderSchema
from schema.objects import OrderSchema, CancelOrderSchema, DeviceSchema
from service.device_list import DeviceListService
from service.express_job import ExpressJobService
from service.express_product import ExpressProductService
from service.send_store import SendStoreService
from service.ship_order import OrderService
from utils.auth import get_auth_data

router = APIRouter()
LOGGER = get_controller_logger('Order')


@router.post('/api/express/mainorder')
def create_express_order_main(*, express_order: OrderSchema, auth_data: dict = Depends(get_auth_data)):
    dispatch_id = express_order.dispatch_id
    if dispatch_id is None:
        return error(msg='请求dispatch_id参数为空')
    if express_order.station_id is None or len(express_order.station_id) == 0:
        return error(msg='请求station_id参数为空')

    express_job = ExpressJobService(auth_data).get_one(dispatch_id)
    if express_job is None:
        return error(msg='dispatch_id 无效')

    if express_job.shipment_id is None or len(express_job.shipment_id) == 0:
        return create_express_order(express_order, auth_data)
    else:
        return create_express_sub_order(express_order, auth_data)


# @router.post('/api/express/sn')
# def create_express_sn(*, device: DeviceSchema, auth_data: dict = Depends(get_auth_data)):
def create_express_sn(device: DeviceSchema, auth_data):
    """
    Args:
    args: 列表请求参数，详见ListArgsSchema
    """
    if device is not None and device.device_sn_list is not None \
            and len(device.device_sn_list) > 0:
        existing_object = DeviceListService(auth_data).get_one(device.device_sn_list)
        if existing_object is not None:
            device.id = existing_object.id
            DeviceListService(auth_data).update(device)
        else:
            DeviceListService(auth_data).create(device)
        return success(None, 'Success')
    else:
        return error(msg='请求参数为空')


# @router.post('/api/express/order')
# def create_express_order(*, express_order: OrderSchema, auth_data: dict = Depends(get_auth_data)):
def create_express_order(express_order: OrderSchema, auth_data):
    dispatch_id = express_order.dispatch_id
    if dispatch_id is None:
        return error(msg='请求dispatch_id参数为空')

    if express_order.station_id is None or len(express_order.station_id) == 0:
        return error(msg='请求station_id参数为空')

    express_job = ExpressJobService(auth_data).get_one(dispatch_id)
    if express_job is None:
        return error(msg='dispatch_id 无效')
    # 目前出库仓比较少，store_id（包括匿名ID），如果 store_id-0，则为匿名ID
    store_id = express_order.store_id
    if store_id is None or len(store_id) == 0:
        store_id = express_job.store_id
    send_store = SendStoreService(auth_data).get_one(store_id)
    if send_store is None:
        return error(msg='store_id 无效')
    # 出货单号+来源订单号，由创建express_job 的时候保存在数据库中
    order_id = express_order.order_id
    if order_id is None or len(order_id) == 0:
        order_id = express_job.order_id
        if order_id is not None and len(order_id) > 0:
            express_order.order_id = order_id

    if order_id is None or len(order_id) == 0:
        return error(msg='order_id 无效')

    if express_job.lock_status == 0:
        return error(msg='请先执行锁定操作', code=4001)
    elif express_job.station_id != express_order.station_id:
        return error(msg='该任务由其他操作台锁定，你无权操作该任务', code=4002)

    if express_order.device_count is None and len(express_order.device_count) == 0:
        return error(msg='请求device_count参数为空')
    else:
        # 判断重复sn
        duplicate_sn = []
        for count_info in express_order.device_count:
            device_sn_list = count_info.device_sn_list.split(',')
            for device_sn in device_sn_list:
                existing_object = DeviceListService(auth_data).get_one(device_sn)
                if existing_object is not None:
                    duplicate_sn.append(device_sn)
        if len(duplicate_sn) > 0:
            return error(data=duplicate_sn, msg='sn已存在', code=4003)

        for count_info in express_order.device_count:
            device_sn_list = count_info.device_sn_list.split(',')
            count = len(device_sn_list)
            # 判断打包数量是否超过需求
            product_code = count_info.product_code
            existing_product_object = ExpressProductService(auth_data).get_one(dispatch_id, product_code)
            if existing_product_object is not None:
                existing_product_object.packed_count = existing_product_object.packed_count + count
                exceed = existing_product_object.packed_count - existing_product_object.product_count
                if exceed > 0:
                    return error(data={'product_code': product_code, 'exceed_num': exceed}, msg='产品打包数量超出', code=4004)
            else:
                return error(data=product_code, msg='该订单不需要此产品', code=4005)

    express_job.status = 1
    ExpressJobService(auth_data).update_by_model(express_job)

    res = OrderService().order(express_job, send_store, express_order)
    order_result = json.loads(res.text)
    if res.status_code == 200:
        apiResultCode = order_result['apiResultCode']
        if apiResultCode != 'A1000':
            express_job.status = 0
            ExpressJobService(auth_data).update_by_model(express_job)
            return error(data=order_result, msg=order_result['apiErrorMsg'], code=4006)
        elif order_result['apiResultData'] is not None:
            apiResultDataStr = order_result['apiResultData']
            apiResultData = json.loads(apiResultDataStr)
            if apiResultData['errorCode'] is not None and apiResultData['errorCode'] == 'S0000' \
                    and apiResultData['msgData'] is not None:
                msgData = apiResultData['msgData']
                if msgData['filterResult'] == 3:
                    return error(data=apiResultData, msg='不可以收派', code=4007)
                waybillNoInfoList = msgData['waybillNoInfoList']
                return_orderId = msgData['orderId']
                # 僅供調試時注釋，實際生產記得還原
                # if return_orderId != express_order.order_id:
                #     express_job.status = 0
                #     ExpressJobService(auth_data).update_by_model(express_job)
                #     return error(data=apiResultData, msg='order id is error')
                if waybillNoInfoList is not None and len(waybillNoInfoList) > 0:
                    waybillNoInfo = waybillNoInfoList[0]
                    shipment_id = waybillNoInfo['waybillNo']
                    waybillType = waybillNoInfo['waybillType']  # 运单号类型1：母单 2 :子单 3 : 签回单
                    express_job.shipment_id = shipment_id
                    express_job.shipment_msg_data = json.dumps(msgData)
                    express_job.status = 2
                    ExpressJobService(auth_data).update_by_model(express_job)
                    # 需要指定产品SN，并保存到数据库中
                    if express_order.device_count is not None and len(express_order.device_count) > 0:
                        for count_info in express_order.device_count:
                            # 处理同一个产品的sn_list
                            device_sn_list = count_info.device_sn_list.split(',')
                            for device_sn in device_sn_list:
                                device = DeviceSchema()
                                device.dispatch_id = dispatch_id
                                device.device_sn_list = device_sn
                                device.shipment_id = shipment_id
                                device.product_code = count_info.product_code
                                DeviceListService(auth_data).create(device)

                            product_code = count_info.product_code
                            existing_product_object = ExpressProductService(auth_data).get_one(dispatch_id,
                                                                                               product_code)
                            if existing_product_object is not None:
                                # 前面count过了，可以直接用
                                existing_product_object.packed_count = existing_product_object.packed_count + count
                                ExpressProductService(auth_data).update_by_model(existing_product_object)

                        res = {'waybillNoInfoList': waybillNoInfoList,
                               'routeLabelData': msgData['routeLabelInfo'][0]['routeLabelData']}
                        return success(res, 'Success')  # 如果返回信息中无地址，需要从Expreess_job中找到返回给前端，供打印
                    else:
                        return error(msg='请求device_count参数为空')
                else:
                    express_job.status = 0
                    ExpressJobService(auth_data).update_by_model(express_job)
                    return error(data=apiResultData, msg='there is no waybillNo')
            else:
                express_job.status = 0
                ExpressJobService(auth_data).update_by_model(express_job)
                return error(data=apiResultData, msg=apiResultData['errorMsg'])
        else:
            express_job.status = 0
            ExpressJobService(auth_data).update_by_model(express_job)
            return error(data=order_result, msg=order_result['apiErrorMsg'])
    else:
        express_job.status = 0
        ExpressJobService(auth_data).update_by_model(express_job)
        return error(data=order_result, msg=order_result['apiErrorMsg'])


# @router.post('/api/express/sub_order')
# def create_express_sub_order(*, express_order: OrderSchema, auth_data: dict = Depends(get_auth_data)):
def create_express_sub_order(express_order: OrderSchema, auth_data):
    dispatch_id = express_order.dispatch_id
    if dispatch_id is None:
        return error(msg='请求dispatch_id参数为空')

    if express_order.station_id is None or len(express_order.station_id) == 0:
        return error(msg='请求station_id参数为空')

    express_job = ExpressJobService(auth_data).get_one(dispatch_id)
    if express_job is None:
        return error(msg='dispatch_id 无效')
    if express_job.shipment_id is None or len(express_job.shipment_id) == 0:
        return error(msg='查询不到母单号', code=4008)
    # 目前出库仓比较少，store_id（包括匿名ID），如果 store_id-0，则为匿名ID
    store_id = express_order.store_id
    if store_id is None or len(store_id) == 0:
        store_id = express_job.store_id
    send_store = SendStoreService(auth_data).get_one(store_id)
    if send_store is None:
        return error(msg='store_id 无效')
    # 出货单号+来源订单号，由创建express_job 的时候保存在数据库中
    order_id = express_order.order_id
    if order_id is None or len(order_id) == 0:
        order_id = express_job.order_id
        if order_id is not None and len(order_id) > 0:
            express_order.order_id = order_id

    if order_id is None or len(order_id) == 0:
        return error(msg='查询不到母单对应的order_id')

    if express_job.lock_status == 0:
        return error(msg='请先执行锁定操作', code=4001)
    elif express_job.station_id != express_order.station_id:
        return error(msg='改任务由其他操作台锁定，你无权操作该任务', code=4002)

    if express_order.parcel_qty is None:
        express_order.parcel_qty = 1

    if express_order.device_count is None and len(express_order.device_count) == 0:
        return error(msg='请求device_count参数为空')
    else:
        # 判断重复sn
        duplicate_sn = []
        for count_info in express_order.device_count:
            device_sn_list = count_info.device_sn_list.split(',')
            for device_sn in device_sn_list:
                existing_object = DeviceListService(auth_data).get_one(device_sn)
                if existing_object is not None:
                    duplicate_sn.append(device_sn)
        if len(duplicate_sn) > 0:
            return error(data=duplicate_sn, msg='sn已存在', code=4003)

        for count_info in express_order.device_count:
            device_sn_list = count_info.device_sn_list.split(',')
            count = len(device_sn_list)
            # 判断打包数量是否超过需求
            product_code = count_info.product_code
            existing_product_object = ExpressProductService(auth_data).get_one(dispatch_id, product_code)
            if existing_product_object is not None:
                existing_product_object.packed_count = existing_product_object.packed_count + count
                exceed = existing_product_object.packed_count - existing_product_object.product_count
                if exceed > 0:
                    return error(data={'product_code': product_code, 'exceed_num': exceed}, msg='产品打包数量超出', code=4004)
            else:
                return error(data=product_code, msg='该订单不需要此产品', code=4005)

    res = OrderService().sub_order(express_order)
    order_result = json.loads(str(res.content, 'utf8'))
    if res.status_code == 200:
        apiResultCode = order_result['apiResultCode']
        if apiResultCode != 'A1000':
            return error(data=order_result, msg=order_result['apiErrorMsg'], code=4006)
        elif order_result['apiResultData'] is not None:
            apiResultDataStr = order_result['apiResultData']
            apiResultData = json.loads(apiResultDataStr)
            if apiResultData['errorCode'] is not None and apiResultData['errorCode'] == 'S0000' \
                    and apiResultData['msgData'] is not None:
                msgData = apiResultData['msgData']
                waybillNoInfoList = msgData['waybillNoInfoList']
                return_orderId = msgData['orderId']
                # 僅供調試時注釋，實際生產記得還原
                # if return_orderId != express_order.order_id:
                #     return error(data=apiResultData, msg='order id is error')
                if waybillNoInfoList is not None and len(waybillNoInfoList) > 0:
                    for waybillNoInfo in waybillNoInfoList:
                        shipment_sub_id = waybillNoInfo['waybillNo']
                        waybillType = waybillNoInfo['waybillType']  # 运单号类型1：母单 2 :子单 3 : 签回单
                        if waybillType == 2:
                            # 需要指定产品SN，并保存到数据库中
                            if express_order.device_count is not None and len(express_order.device_count) > 0:
                                for count_info in express_order.device_count:
                                    # 处理同一个产品的sn_list
                                    device_sn_list = count_info.device_sn_list.split(',')
                                    for device_sn in device_sn_list:
                                        device = DeviceSchema()
                                        device.dispatch_id = dispatch_id
                                        device.device_sn_list = device_sn
                                        device.shipment_id = express_job.shipment_id
                                        device.shipment_sub_id = shipment_sub_id
                                        device.product_code = count_info.product_code
                                        DeviceListService(auth_data).create(device)

                                    product_code = count_info.product_code
                                    # 前面count过了，可以直接用
                                    existing_product_object = ExpressProductService(auth_data).get_one(dispatch_id,
                                                                                                       product_code)
                                    if existing_product_object is not None:
                                        existing_product_object.packed_count = existing_product_object.packed_count + count
                                        ExpressProductService(auth_data).update_by_model(existing_product_object)

                                res = {'waybillNoInfoList': waybillNoInfoList, 'routeLabelData': ''}
                                main_msgData = json.loads(express_job.shipment_msg_data)['routeLabelInfo'][0]
                                res['routeLabelData'] = main_msgData['routeLabelData']
                                return success(res, 'Success')  # 如果返回信息中无地址，需要从Expreess_job中找到返回给前端，供打印
                            else:
                                return error(msg='请求device_count参数为空')
                        else:
                            continue
                else:
                    return error(data=apiResultData, msg='there is no waybillNo')
            else:
                return error(data=apiResultData, msg=apiResultData['errorMsg'])
        else:
            return error(data=order_result, msg=order_result['apiErrorMsg'])
    else:
        return error(data=order_result, msg=order_result['apiErrorMsg'])


@router.delete('/api/express/order')
def delete_express_order(*, express_order: CancelOrderSchema, auth_data: dict = Depends(get_auth_data)):
    dispatch_id = express_order.dispatch_id
    if dispatch_id is None:
        return error(msg='请求dispatch_id参数为空')

    if express_order.station_id is None or len(express_order.station_id) == 0:
        return error(msg='请求station_id参数为空')

    express_job = ExpressJobService(auth_data).get_one(dispatch_id)
    if express_job is None:
        return error(msg='dispatch_id 无效')
    if express_job.shipment_id is None or len(express_job.shipment_id) == 0:
        return error(msg='查询不到母单号')

    order_id = express_order.order_id
    if order_id is None or len(order_id) == 0:
        order_id = express_job.order_id
        if order_id is not None and len(order_id) > 0:
            express_order.order_id = order_id

    if order_id is None:
        return error(msg='请求order_id参数为空')

    if express_job.lock_status == 1:
        return error(msg='该任务被锁定，请先执行解锁操作')

    res = OrderService().cancel_order(express_order)
    order_result = json.loads(str(res.content, 'utf8'))
    if res.status_code == 200:
        apiResultCode = order_result['apiResultCode']
        if apiResultCode != 'A1000':
            return error(data=order_result, msg=order_result['apiErrorMsg'])
        elif order_result['apiResultData'] is not None:
            apiResultDataStr = order_result['apiResultData']
            apiResultData = json.loads(apiResultDataStr)
            if apiResultData['errorCode'] is not None and apiResultData['errorCode'] == 'S0000' \
                    and apiResultData['msgData'] is not None:
                msgData = apiResultData['msgData']
                waybillNoInfoList = msgData['waybillNoInfoList']
                return_orderId = msgData['orderId']
                if return_orderId != express_order.order_id:
                    return error(data=apiResultData, msg='order id is error')
                elif waybillNoInfoList is not None and len(waybillNoInfoList) > 0:
                    for waybillNoInfo in waybillNoInfoList:
                        shipment_sub_id = waybillNoInfo['waybillNo']
                        waybillType = waybillNoInfo['waybillType']  # 运单号类型1：母单 2 :子单 3 : 签回单
                        # delete device table
                        existing_objects = None
                        args = ListArgsSchema()
                        args.filters = []

                        if waybillType == 2:
                            q_filter = ListFilterSchema(key='shipment_sub_id', condition='=', value=shipment_sub_id)
                            args.filters.append(q_filter)
                        elif waybillType == 1:
                            q_filter = ListFilterSchema(key='shipment_id', condition='=', value=shipment_sub_id)
                            args.filters.append(q_filter)

                        args.user_id = auth_data.get('user_id')
                        LOGGER.debug('Get  Data list ')
                        if len(args.filters) > 0:
                            existing_objects = DeviceListService(auth_data).list(args)
                            if existing_objects is not None:
                                for device in existing_objects:
                                    DeviceListService(auth_data).delete(df['id'])
                            else:
                                return error(msg='查询不到sn_list')

                        # cancel all order
                        if waybillType == 1:
                            express_job.status = 0
                            express_job.shipment_id = None
                            ExpressJobService(auth_data).update_by_model(express_job)

                    return success(apiResultData, 'Success')
                else:
                    # cancel all order
                    express_job.status = 0
                    express_job.shipment_id = None
                    ExpressJobService(auth_data).update_by_model(express_job)
                    return success(apiResultData, 'Success')
            else:
                return error(data=apiResultData, msg=apiResultData['errorMsg'])
        else:
            return error(data=order_result, msg=order_result['apiErrorMsg'])
    else:
        return error(data=order_result, msg=order_result['apiErrorMsg'])


@router.get('/api/express/search_order')
def search_express_order(*, dispatch_id: str = '', auth_data: dict = Depends(get_auth_data)):
    if not dispatch_id:
        return error(msg='请求dispatch_id参数为空')

    express_job = ExpressJobService(auth_data).get_one(dispatch_id)
    if express_job is None:
        return error(msg='dispatch_id 无效')

    order_id = express_job.order_id
    if order_id is None:
        return error(msg='请求order_id参数为空')

    res = OrderService().search_order(order_id)
    order_result = json.loads(str(res.content, 'utf8'))
    if res.status_code == 200:
        apiResultCode = order_result['apiResultCode']
        if apiResultCode != 'A1000':
            return error(data=order_result, msg=order_result['apiErrorMsg'])
        elif order_result['apiResultData'] is not None:
            apiResultDataStr = order_result['apiResultData']
            apiResultData = json.loads(apiResultDataStr)

            if apiResultData['errorCode'] is not None and apiResultData['errorCode'] == 'S0000' \
                    and apiResultData['msgData'] is not None:
                msgData = apiResultData['msgData']
                waybillNoInfoList = msgData['waybillNoInfoList']
                routeLabelInfo = msgData['routeLabelInfo']
                if waybillNoInfoList is not None and len(waybillNoInfoList) > 0:
                    res = {'waybillNoInfoList': waybillNoInfoList, 'routeLabelInfo': routeLabelInfo}
                    return success(res, 'Success')
                else:
                    return error(data=apiResultData, msg='there is no waybillNo')
            else:
                return error(data=apiResultData, msg=order_result['apiErrorMsg'])
        else:
            return error(data=order_result, msg=order_result['apiErrorMsg'])
    else:
        return error(data=order_result, msg=order_result['apiErrorMsg'])
