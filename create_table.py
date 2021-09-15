import pymysql
from utils.db import DbUtils
from config.db import db_config


def create_db():
    DbUtils.default_config = db_config
    config = DbUtils.default_config
    db = pymysql.connect(host=config.host, user=config.username, password=config.password, port=int(config.port))
    cursor = db.cursor()
    sql = f'DROP DATABASE IF EXISTS {config.database};'
    cursor.execute(sql)
    sql = f'create database if not exists {config.database} character set utf8;'
    cursor.execute(sql)
    # 关闭游标连接
    cursor.close()
    # 关闭数据库连接
    db.close()


def create_table():
    # 连接本地数据库
    DbUtils.default_config = db_config
    config = DbUtils.default_config
    db = pymysql.connect(host=config.host, user=config.username, password=config.password, port=int(config.port),
                         database=config.database, charset="utf8")

    # 创建游标
    cursor = db.cursor()
    # 如果存在表，则删除
    cursor.execute("DROP TABLE IF EXISTS t_user")
    cursor.execute("DROP TABLE IF EXISTS t_express_job")
    cursor.execute("DROP TABLE IF EXISTS t_express_product")
    cursor.execute("DROP TABLE IF EXISTS t_event_log")
    cursor.execute("DROP TABLE IF EXISTS t_express_device_list")
    cursor.execute("DROP TABLE IF EXISTS t_send_store")

    # 创建表 t_user
    sql = """
        create table t_user(
        id bigint(20) PRIMARY KEY auto_increment,
        username varchar(255),
        password varchar(255))
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)

    # 插入 t_user
    sql = """
        insert into t_user(username, password) VALUES
        ('admin','58097ab97fc84ec7109f3fdf5def91ac'),
        ('user','a951456dfd640864f5ce3c13cd7d2d33');
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("插入数据库成功")
        db.commit()
    except Exception as e:
        print("插入数据库失败：case%s" % e)

    # 创建表 t_express_job
    sql = """
        create table t_express_job(
        id bigint(20) PRIMARY KEY auto_increment,
        create_by bigint(20) default 0,
        create_time timestamp default current_timestamp,
        update_by bigint(20) default 0,
        update_time timestamp default current_timestamp ON UPDATE current_timestamp,
        del_flag tinyint(1) default 0,
        
        dispatch_id char(64),
        shipment_id char(64),
        order_id char(64),
        store_id char(64),
        with_tray boolean,
        custom_name varchar(256),
        receipt_address varchar(256),
        receiver_person char(64),
        receiver_phone char(64),
        carrier char(64),
        transportation char(64),
        station_id char(64),
        status int default 0,
        lock_status int default 0,
        shipment_msg_data varchar(2048),
        receipt_province char(64),
        receipt_city char(64),
        receipt_county char(64))
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)

    # 创建表 t_express_product
    sql = """
        create table t_express_product(
        id bigint(20) PRIMARY KEY auto_increment,
        create_by bigint(20) default 0,
        create_time timestamp default current_timestamp,
        update_by bigint(20) default 0,
        update_time timestamp default current_timestamp ON UPDATE current_timestamp,
        del_flag tinyint(1) default 0,

        dispatch_id char(64),
        product_code char(64),
        product_name char(128),
        product_model char(64),
        product_count float,
        packed_count float)
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)

    # 创建表 t_event_log
    sql = """
        create table t_event_log(
        id bigint(20) PRIMARY KEY auto_increment,
        create_by bigint(20) default 0,
        create_time timestamp default current_timestamp,
        update_by bigint(20) default 0,
        update_time timestamp default current_timestamp ON UPDATE current_timestamp,
        del_flag tinyint(1) default 0,

        user_id BIGINT(20) default 0,
        relation_obj char(255),
        relation_id bigint(20) default 0,
        relation_name char(255),
        event_id bigint(20) default 0,
        event_time timestamp default current_timestamp,
        event_from char(255),
        before_data longtext,
        change_data longtext,
        after_data longtext)
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)

    # 创建表 t_express_device_list
    sql = """
        create table t_express_device_list(
        id bigint(20) PRIMARY KEY auto_increment,
        create_by bigint(20) default 0,
        create_time timestamp default current_timestamp,
        update_by bigint(20) default 0,
        update_time timestamp default current_timestamp ON UPDATE current_timestamp,
        del_flag tinyint(1) default 0,

        product_code char(64),
        device_sn_list varchar(2048),
        shipment_id char(64),
        shipment_sub_id char(64),
        dispatch_id char(64))
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)

    # 创建表 t_send_store
    sql = """
        create table t_send_store(
        id bigint(20) PRIMARY KEY auto_increment,
        create_by bigint(20) default 0,
        create_time timestamp default current_timestamp,
        update_by bigint(20) default 0,
        update_time timestamp default current_timestamp ON UPDATE current_timestamp,
        del_flag tinyint(1) default 0,

        store_id char(64),
        address char(255),
        city char(64),
        company char(64),
        contact char(64),
        county varchar(256),
        mobile char(64),
        province char(64))
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("创建数据库成功")
    except Exception as e:
        print("创建数据库失败：case%s" % e)

    # 插入 t_send_store
    sql = """
        insert into t_send_store(store_id, address, city, company, contact, county, mobile) VALUES(
        '04002',
        '北京市海淀区天地邻枫产业园1号楼B栋', 
        '北京市',
        '北京格灵深瞳信息技术股份有限公司',
        '樊成水',
        '海淀区',
        '15116960344'
        )
    """
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("插入数据库成功")
        db.commit()
    except Exception as e:
        print("插入数据库失败：case%s" % e)
    finally:
        # 关闭游标连接
        cursor.close()
        # 关闭数据库连接
        db.close()


def main():
    create_db()
    create_table()


if __name__ == "__main__":
    main()
