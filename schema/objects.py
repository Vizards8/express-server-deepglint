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
    device_sn_list: str = None  # ????????????


class DeviceCountSchema(BaseModel):
    product_code: Optional[str] = ''
    device_sn_list: str = ''


class OrderSchema(BaseModel):
    id: Optional[int] = 0
    dispatch_id: Optional[str] = ''
    product_id: Optional[str] = ''
    order_id: str = ''
    count: Optional[int] = 1
    unit: Optional[str] = '???'
    weight: Optional[float] = 0.0
    name: Optional[str] = '????????????'  # express job ???????????????
    device_sn_list: Optional[str] = None  # ?????????????????????????????????????????????
    store_id: Optional[str] = ''
    parcel_qty: Optional[int] = 1
    station_id: Optional[str] = ''
    device_count: List[DeviceCountSchema] = None  # ????????????
    test = True  # ???????????????True?????????????????????????????????????????????????????????


class SubOrderSchema(BaseModel):
    order_id: Optional[str] = None
    parcelQty: Optional[int] = 0
    station_id: Optional[str] = ''


class WaybillSchema(BaseModel):
    waybillType: Optional[int] = 1
    waybillNo: Optional[str] = None


class CancelOrderSchema(BaseModel):
    dispatch_id: Optional[str] = ''
    order_id: Optional[str] = None  # ???????????????
    dealType: Optional[int] = 2  # ????????????????????????,1:?????? ,2:??????
    waybillNoInfoList: Optional[List[WaybillSchema]] = None  # ????????????
    station_id: Optional[str] = ''
