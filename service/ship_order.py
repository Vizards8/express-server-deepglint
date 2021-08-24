import json

import requests
import hashlib
import base64
import urllib
import uuid
import time

from config.fastapi import FastapiConfig


class OrderService:
    def __init__(self):
        pass

    def order(self, express_job, send_store, express_order):
        req_url = '%s' % FastapiConfig.express_addr
        partner_id = '%s' % FastapiConfig.partnerID
        check_word = '%s' % FastapiConfig.checkword
        monthly_card = '%s' % FastapiConfig.monthlyCard

        order_id = express_job.order_id
        service_code = "EXP_RECE_CREATE_ORDER"
        request_id = str(uuid.uuid1())  # 生成uuid
        timestamp = str(int(time.time()))  # 获取时间戳

        cargo_detail = {
            'amount': 1,
            'count': express_order.count,
            'name': express_order.name,  # 货物名称，必填
            'unit': express_order.unit,
            'volume': 0.0,
            'weight': express_order.weight}
        cargo_details = [cargo_detail]

        s_contact_info = {"address": send_store.address,
                         "city": send_store.city,
                         "company": send_store.company,
                         "contact": send_store.contact,
                         "contactType": 1,  # 1 寄件方信息
                         "county": send_store.county,  # 必填，国家或地区 2位代码,参照附录国家代码附件
                         "mobile": send_store.mobile,
                         "province": send_store.province}

        r_contact_info = {"address": express_job.receipt_address,
                         # "city": express_job.receipt_city,
                         # "company": "",
                         # "contact": express_job.receiver_person,
                         # "contactType": 2,  # 2，到件方信息
                         # "county": express_job.receipt_county,
                         # "mobile": express_job.receiver_phone,
                         # "province": express_job.receipt_province}
                         "city": "",
                         "company": express_job.custom_name,
                         "contact": express_job.receiver_person,
                         "contactType": 2,  # 2，到件方信息
                         "county": "",
                         "mobile": express_job.receiver_phone,
                         "province": ""}

        contactInfoList = []
        contactInfoList.append(s_contact_info)
        contactInfoList.append(r_contact_info)

        msg_data = {'cargoDetails': cargo_details,
                   'contactInfoList': contactInfoList,
                   'customsInfo': {},
                   'expressTypeId': 1,
                   'extraInfoList': [],
                   'isOneselfPickup': 0,  # 快件自取
                   'language': "zh-CN",
                   'monthlyCard': monthly_card,
                   # 'orderId': str(time.time()),
                   'orderId': order_id,
                   'parcelQty': 1,  # 包裹数
                   'payMethod': 1,  # 付款方式
                   'totalWeight': 6}  # 订单货物总重量,若为子母件必填，
        encoded_msg_data = json.dumps(msg_data)
        res = self.callSfExpressServiceByCSIM(req_url, partner_id, request_id, service_code, timestamp, encoded_msg_data,
                                              check_word)
        return res

    def sub_order(self, express_order):
        req_url = '%s' % FastapiConfig.express_addr
        partner_id = '%s' % FastapiConfig.partnerID
        check_word = '%s' % FastapiConfig.checkword
        # monthly_card = '%s' % FastapiConfig.monthlyCard

        order_id = express_order.order_id
        service_code = "EXP_RECE_GET_SUB_MAILNO"
        request_id = str(uuid.uuid1())  # 生成uuid
        timestamp = str(int(time.time()))  # 获取时间戳

        msg_data = {
            'orderId': order_id,
            'parcelQty': express_order.parcel_qty
        }
        encoded_msg_data = json.dumps(msg_data)
        res = self.callSfExpressServiceByCSIM(req_url, partner_id, request_id, service_code, timestamp, encoded_msg_data,
                                              check_word)
        return res


    def callSfExpressServiceByCSIM(self, req_url, partner_id, request_id, service_code, timestamp, msg_data, check_word):
        print('请求报文：' + msg_data)
        str = urllib.parse.quote_plus(msg_data + timestamp + check_word)
        # 先md5加密然后base64加密
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        md5Str = m.digest()
        msg_digest = base64.b64encode(md5Str).decode('utf-8')
        print("msgDigest: " + msg_digest)
        data = {"partnerID": partner_id, "requestID": request_id, "serviceCode": service_code, "timestamp": timestamp,
                "msgDigest": msg_digest, "msgData": msg_data}
        # 发送post请求
        res = requests.post(req_url, data=data)
        return res

    def cancel_order(self, cancel_order):
        req_url = '%s' % FastapiConfig.express_addr
        partner_id = '%s' % FastapiConfig.partnerID
        check_word = '%s' % FastapiConfig.checkword

        order_id = cancel_order.order_id

        service_code = "EXP_RECE_UPDATE_ORDER"
        request_id = str(uuid.uuid1())  # 生成uuid
        timestamp = str(int(time.time()))  # 获取时间戳
        waybillNoInfoList = []
        if cancel_order.waybillNoInfoList is not None and len(cancel_order.waybillNoInfoList) > 0:
            for waybillNoInfo in cancel_order.waybillNoInfoList:
                waybillNoInfoTag = {
                    'waybillType': waybillNoInfo.waybillType,
                    'waybillNo': waybillNoInfo.waybillNo
                }
                waybillNoInfoList.append(waybillNoInfoTag)
        msg_data = {
            "dealType": 2,
            "orderId": order_id,
            "waybillNoInfoList":waybillNoInfoList
            }
        encoded_msg_data = json.dumps(msg_data)
        res = self.callSfExpressServiceByCSIM(req_url, partner_id, request_id, service_code, timestamp, encoded_msg_data,
                                              check_word)
        return res