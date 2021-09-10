from typing import Optional, List

from pydantic import BaseModel


class ExpressJobSchema(BaseModel):
    id: Optional[int] = 0
    dispatch_id: str = None
    shipment_id: Optional[str] = ''
    order_id: Optional[str] = ''
    store_id: Optional[str] = ''
    with_tray: Optional[bool] = False
    custom_name: Optional[str] = ''
    receipt_address: Optional[str] = ''
    receiver_person: Optional[str] = ''
    receiver_phone: Optional[str] = ''
    carrier: Optional[str] = ''
    transportation: Optional[str] = ''
    status: Optional[int] = 0
    create_by: Optional[str] = ''
    update_by: Optional[str] = ''
    lock_status: Optional[int] = 0
    station_id: Optional[str] = ''
    shipment_msg_data: Optional[str] = ''
    receipt_province: Optional[str] = ''
    receipt_city: Optional[str] = ''
    receipt_county: Optional[str] = ''


class ExpressProductSchema(BaseModel):
    id: Optional[int] = 0
    dispatch_id: str = None
    product_code: Optional[str] = ''
    product_name: Optional[str] = ''
    product_model: Optional[str] = ''
    product_count: Optional[str] = ''
    packed_count: Optional[float] = 0
    # create_by: Optional[int] = None
    # update_by: Optional[int] = None


class ExpressJobProductSchema(BaseModel):
    id: Optional[int] = 0
    dispatch_id: str = None
    shipment_id: Optional[str] = None
    order_id: Optional[str] = None
    store_id: Optional[str] = None
    with_tray: Optional[bool] = False
    custom_name: Optional[str] = None
    receipt_address: Optional[str] = None
    receiver_person: Optional[str] = None
    receiver_phone: Optional[str] = None
    carrier: Optional[str] = None
    transportation: Optional[str] = None
    station_id: Optional[str] = None
    status: Optional[int] = 0
    receipt_province: Optional[str] = ''
    receipt_city: Optional[str] = ''
    receipt_county: Optional[str] = ''
    source_order_id: Optional[str] = None
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    product_model: Optional[str] = None
    product_count: Optional[str] = None


class DeviceSchema(BaseModel):
    id: Optional[int] = 0
    dispatch_id: Optional[str] = ''
    product_code: Optional[str] = ''
    shipment_id: Optional[str] = ''
    shipment_sub_id: Optional[str] = ''
    device_sn_list: str = None  # 过滤条件


class DeviceCountSchema(BaseModel):
    product_code: Optional[str] = ''
    device_sn_list: str = ''


class OrderSchema(BaseModel):
    id: Optional[int] = 0
    dispatch_id: Optional[str] = ''
    product_id: Optional[str] = ''
    order_id: str = ''
    count: Optional[int] = 1
    unit: Optional[str] = '个'
    weight: Optional[float] = 0.0
    name: Optional[str] = '数码产品'  # express job 中产品信息
    device_sn_list: Optional[str] = None  # 如果一起上传，则保存到数据库中
    store_id: Optional[str] = ''
    parcel_qty: Optional[int] = 1
    station_id: Optional[str] = ''
    device_count: List[DeviceCountSchema] = None  # 字段条件
    test = True  # 测试字段，True使用顺丰沙盒接口，反之使用实际生产接口


class SubOrderSchema(BaseModel):
    order_id: Optional[str] = None
    parcelQty: Optional[int] = 0
    station_id: Optional[str] = ''


class WaybillSchema(BaseModel):
    waybillType: Optional[int] = 1
    waybillNo: Optional[str] = None


class CancelOrderSchema(BaseModel):
    dispatch_id: Optional[str] = ''
    order_id: Optional[str] = None  # 客户订单号
    dealType: Optional[int] = 2  # 客户订单操作标识,1:确认 ,2:取消
    waybillNoInfoList: List[WaybillSchema] = None  # 字段条件
    station_id: Optional[str] = ''
