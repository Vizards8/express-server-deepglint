Base:
id = Column(BIGINT(20), primary_key=True, comment='序号')
create_by = Column(BIGINT(20), nullable=False, server_default=text("0"), default='0', comment='创建人')
create_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"), default=datetime.now,
                     comment='创建时间')
update_by = Column(BIGINT(20), nullable=False, server_default=text("0"), default='0', comment='更新人')
update_time = Column(TIMESTAMP, nullable=False,
                     server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
                     default=datetime.now, comment='更新时间')
del_flag = Column(TINYINT(1), nullable=False, server_default=text("0"), default='0', comment='软删')

express_job:发货任务
dispatch_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货单号')
shipment_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递单号')
order_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货单号-出库单号')
store_id = Column(String(64), nullable=False, server_default=text("''"), comment='仓库编码')
with_tray = Column(sqltypes.BOOLEAN, nullable=False, server_default=text("''"), comment='是否带托盘')
custom_name = Column(String(256), nullable=False, server_default=text("''"), comment='客户名')
receipt_address = Column(String(256), nullable=False, server_default=text("''"), comment='收货地址')
receiver_person = Column(String(64), nullable=False, server_default=text("''"), comment='收货人')
receiver_phone = Column(String(64), nullable=False, server_default=text("''"), comment='收货人电话')
carrier = Column(String(64), nullable=False, server_default=text("''"), comment='物流承运商')
transportation = Column(String(64), nullable=False, server_default=text("''"), comment='发运方式')
station_id = Column(String(64), nullable=False, server_default=text("''"), comment='操作工位')
status = Column(sqltypes.INTEGER, nullable=False, server_default=text("0"), comment='任务状态')
lock_status = Column(sqltypes.INTEGER, nullable=False, server_default=text("0"), comment='任务锁定状态')
shipment_msg_data = Column(String(2048), nullable=False, server_default=text("''"), comment='下单返回信息')
receipt_province = Column(String(64), nullable=False, server_default=text("''"), comment='收货人省份')
receipt_city = Column(String(64), nullable=False, server_default=text("''"), comment='收货人城市')
receipt_county = Column(String(64), nullable=False, server_default=text("''"), comment='收货人县/区级行政区名称')

express_product:发货产品
dispatch_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货单号')
product_code = Column(String(64), nullable=False, server_default=text("''"), comment='存货编码')
product_name = Column(String(128), nullable=False, server_default=text("''"), comment='存货名称')
product_model = Column(String(64), nullable=False, server_default=text("''"), comment='规格型号')
product_count = Column(FLOAT, nullable=False, server_default=text("''"), comment='数量')
packed_count = Column(FLOAT, nullable=False, server_default=text("''"), comment='已打包数量')

device_list:设备详细列表
product_code = Column(sqltypes.INTEGER, nullable=False, server_default=text("''"), comment='产品ID')
device_sn_list = Column(String(2048), nullable=False, server_default=text("''"), comment='产品序列号')
shipment_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递母单号')
shipment_sub_id = Column(String(64), nullable=False, server_default=text("''"), comment='快递子单号')
dispatch_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货单号')

send_store:日现数据
store_id = Column(String(64), nullable=False, server_default=text("''"), comment='发货仓ID')
address = Column(String(255), nullable=False, server_default=text("''"), comment='地址')
city = Column(String(64), nullable=False, server_default=text("''"), comment='城市')
company = Column(String(64), nullable=False, server_default=text("''"), comment='公司')
contact = Column(String(64), nullable=False, server_default=text("''"), comment='联系人')
county = Column(String(256), nullable=False, server_default=text("''"), comment='县/区')
mobile = Column(String(64), nullable=False, server_default=text("''"), comment='电话')
province = Column(String(64), nullable=False, server_default=text("''"), comment='省份')

Excel:
仓库：委外仓
出库日期：2021-07-08
出库单号：source_order_id
出库类别：销售出库
销售部门：产品部1
业务员：周成
客户：custom_name
存货编码：product_code
存货名称：product_name
规格型号：product_model
数量：product_count
发货单id：dispatch_id
项目：农行（重庆市分行）安防设备项目
货位编码：store_id
货位：初始化时插入数据库
收货地址：receipt_address
收货人：receiver_person
收货人电话：receiver_phone
物流承运商：carrier
发运方式：transportation