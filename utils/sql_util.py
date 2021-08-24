from itertools import groupby


class SQLUtil:
    def __init__(self):
        pass

    @staticmethod
    def remove_num(a):
        b = []
        for i in a:
            if i not in "0123456789":
                b.append(i)
        return "".join(b)

    @staticmethod
    def create_raw_sql_for_day_data(date_from, date_to, contract_list):
        if contract_list is not None:
            if len(contract_list) == 2:
                f_contract_name = contract_list[0].contract_name
                if f_contract_name and len(f_contract_name) > 3:
                    last_two = f_contract_name[-2:]
                    char_part = SQLUtil.remove_num(f_contract_name)
                    f_contract_name = char_part + '%' + last_two
                s_contract_name = contract_list[1].contract_name
                if s_contract_name and len(s_contract_name) > 3:
                    last_two = s_contract_name[-2:]
                    char_part = SQLUtil.remove_num(s_contract_name)
                    s_contract_name = char_part + '%' + last_two

                raw_sql = 'select a.high ahigh,a.low alow,a.open aopen,a.close aclose, b.high bhigh,b.low blow,' \
                          'b.open bopen,b.close bclose,a.trading_day '
                f_contract_type = contract_list[0].contract_type
                if f_contract_type == "CTP" or f_contract_type is None:
                    raw_sql = raw_sql + 'from t_market_day_data a '
                elif f_contract_type == "ATP":
                    raw_sql = raw_sql + 'from t_market_day_data a '

                s_contract_type = contract_list[1].contract_type
                if s_contract_type == "CTP" or s_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_day_data b '
                elif s_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_day_data b '
                raw_sql = raw_sql + 'on a.trading_day=b.trading_day '

                raw_sql = raw_sql + "where a.contract_name like  '" + f_contract_name + "' "
                raw_sql = raw_sql + "and b.contract_name like  '" + s_contract_name + "' "
                raw_sql = raw_sql + "and a.trading_day >=  '" + date_from + "' "
                raw_sql = raw_sql + "and a.trading_day <=  '" + date_to + "' "
                return raw_sql
            elif len(contract_list) == 3:
                f_contract_name = contract_list[0].contract_name
                if f_contract_name and len(f_contract_name) > 3:
                    last_two = f_contract_name[-2:]
                    char_part = SQLUtil.remove_num(f_contract_name)
                    f_contract_name = char_part + '%' + last_two

                s_contract_name = contract_list[1].contract_name
                if s_contract_name and len(s_contract_name) > 3:
                    last_two = s_contract_name[-2:]
                    char_part = SQLUtil.remove_num(s_contract_name)
                    s_contract_name = char_part + '%' + last_two

                t_contract_name = contract_list[2].contract_name
                if t_contract_name and len(t_contract_name) > 3:
                    last_two = t_contract_name[-2:]
                    char_part = SQLUtil.remove_num(t_contract_name)
                    t_contract_name = char_part + '%' + last_two

                raw_sql = 'select a.high ahigh,a.low alow,a.open aopen,a.close aclose, b.high bhigh,b.low blow,' \
                          'b.open bopen,b.close bclose, c.high chigh,c.low clow,c.open copen,' \
                          'c.close cclose ,a.trading_day '
                f_contract_type = contract_list[0].contract_type
                if f_contract_type == "CTP" or f_contract_type is None:
                    raw_sql = raw_sql + 'from t_market_day_data a '
                elif f_contract_type == "ATP":
                    raw_sql = raw_sql + 'from t_market_day_data a '

                s_contract_type = contract_list[1].contract_type
                if s_contract_type == "CTP" or s_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_day_data b '
                elif s_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_day_data b '
                raw_sql = raw_sql + 'on a.trading_day=b.trading_day '

                t_contract_type = contract_list[2].contract_type
                if t_contract_type == "CTP" or t_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_day_data c '
                elif t_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_day_data c '
                raw_sql = raw_sql + 'on a.trading_day=c.trading_day '

                raw_sql = raw_sql + "where a.contract_name like  '" + f_contract_name + "' "
                raw_sql = raw_sql + "and b.contract_name like  '" + s_contract_name + "' "
                raw_sql = raw_sql + "and c.contract_name like  '" + t_contract_name + "' "
                raw_sql = raw_sql + "and a.trading_day >=  '" + date_from + "' "
                raw_sql = raw_sql + "and a.trading_day <=  '" + date_to + "' "
                return raw_sql
            else:
                return ''
        return ''

    @staticmethod
    def create_raw_sql_for_minute_data(date_from, date_to, contract_list):
        if contract_list is not None:
            if len(contract_list) == 2:
                f_contract_name = contract_list[0].contract_name
                if f_contract_name and len(f_contract_name) > 3:
                    last_two = f_contract_name[-2:]
                    char_part = SQLUtil.remove_num(f_contract_name)
                    f_contract_name = char_part + '%' + last_two
                s_contract_name = contract_list[1].contract_name
                if s_contract_name and len(s_contract_name) > 3:
                    last_two = s_contract_name[-2:]
                    char_part = SQLUtil.remove_num(s_contract_name)
                    s_contract_name = char_part + '%' + last_two

                raw_sql = 'select a.high ahigh,a.low alow,a.open aopen,a.close aclose, b.high bhigh,b.low blow,' \
                          'b.open bopen,b.close bclose,a.trading_time '
                f_contract_type = contract_list[0].contract_type
                if f_contract_type == "CTP" or f_contract_type is None:
                    raw_sql = raw_sql + 'from t_market_minute_data a '
                elif f_contract_type == "ATP":
                    raw_sql = raw_sql + 'from t_market_minute_data a '

                s_contract_type = contract_list[1].contract_type
                if s_contract_type == "CTP" or s_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_minute_data b '
                elif s_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_minute_data b '
                raw_sql = raw_sql + 'on a.trading_time=b.trading_time '

                raw_sql = raw_sql + "where a.contract_name like  '" + f_contract_name + "' "
                raw_sql = raw_sql + "and b.contract_name like  '" + s_contract_name + "' "
                raw_sql = raw_sql + "and a.trading_time >=  '" + date_from + "' "
                raw_sql = raw_sql + "and a.trading_time <=  '" + date_to + "' "
                return raw_sql
            elif len(contract_list) == 3:
                f_contract_name = contract_list[0].contract_name
                if f_contract_name and len(f_contract_name) > 3:
                    last_two = f_contract_name[-2:]
                    char_part = SQLUtil.remove_num(f_contract_name)
                    f_contract_name = char_part + '%' + last_two

                s_contract_name = contract_list[1].contract_name
                if s_contract_name and len(s_contract_name) > 3:
                    last_two = s_contract_name[-2:]
                    char_part = SQLUtil.remove_num(s_contract_name)
                    s_contract_name = char_part + '%' + last_two

                t_contract_name = contract_list[2].contract_name
                if t_contract_name and len(t_contract_name) > 3:
                    last_two = t_contract_name[-2:]
                    char_part = SQLUtil.remove_num(t_contract_name)
                    t_contract_name = char_part + '%' + last_two

                raw_sql = 'select a.high ahigh,a.low alow,a.open aopen,a.close aclose, b.high bhigh,b.low blow,' \
                          'b.open bopen,b.close bclose, c.high chigh,c.low clow,c.open copen,' \
                          'c.close cclose ,a.trading_time '
                f_contract_type = contract_list[0].contract_type
                if f_contract_type == "CTP" or f_contract_type is None:
                    raw_sql = raw_sql + 'from t_market_minute_data a '
                elif f_contract_type == "ATP":
                    raw_sql = raw_sql + 'from t_market_minute_data a '

                s_contract_type = contract_list[1].contract_type
                if s_contract_type == "CTP" or s_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_minute_data b '
                elif s_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_minute_data b '
                raw_sql = raw_sql + 'on a.trading_time=b.trading_time '

                t_contract_type = contract_list[2].contract_type
                if t_contract_type == "CTP" or t_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_minute_data c '
                elif t_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_minute_data c '
                raw_sql = raw_sql + 'on a.trading_time=c.trading_time '

                raw_sql = raw_sql + "where a.contract_name like  '" + f_contract_name + "' "
                raw_sql = raw_sql + "and b.contract_name like  '" + s_contract_name + "' "
                raw_sql = raw_sql + "and c.contract_name like  '" + t_contract_name + "' "
                raw_sql = raw_sql + "and a.trading_time >=  '" + date_from + "' "
                raw_sql = raw_sql + "and a.trading_time <=  '" + date_to + "' "
                return raw_sql
            else:
                return ''
        return ''

    @staticmethod
    def create_raw_sql_for_second_data(date_from, date_to, contract_list):
        if contract_list is not None:
            if len(contract_list) == 2:
                f_contract_name = contract_list[0].contract_name
                if f_contract_name and len(f_contract_name) > 3:
                    last_two = f_contract_name[-2:]
                    char_part = SQLUtil.remove_num(f_contract_name)
                    f_contract_name = char_part + '%' + last_two
                s_contract_name = contract_list[1].contract_name
                if s_contract_name and len(s_contract_name) > 3:
                    last_two = s_contract_name[-2:]
                    char_part = SQLUtil.remove_num(s_contract_name)
                    s_contract_name = char_part + '%' + last_two

                raw_sql = 'select a.high ahigh,a.low alow,a.open aopen,a.close aclose, b.high bhigh,b.low blow,' \
                          'b.open bopen,b.close bclose,a.trading_time '
                f_contract_type = contract_list[0].contract_type
                if f_contract_type == "CTP" or f_contract_type is None:
                    raw_sql = raw_sql + 'from t_market_second_data a '
                elif f_contract_type == "ATP":
                    raw_sql = raw_sql + 'from t_market_second_data a '

                s_contract_type = contract_list[1].contract_type
                if s_contract_type == "CTP" or s_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_second_data b '
                elif s_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_second_data b '
                raw_sql = raw_sql + 'on a.trading_time=b.trading_time '

                raw_sql = raw_sql + "where a.contract_name like  '" + f_contract_name + "' "
                raw_sql = raw_sql + "and b.contract_name like  '" + s_contract_name + "' "
                raw_sql = raw_sql + "and a.trading_time >=  '" + date_from + "' "
                raw_sql = raw_sql + "and a.trading_time <=  '" + date_to + "' "
                return raw_sql
            elif len(contract_list) == 3:
                f_contract_name = contract_list[0].contract_name
                if f_contract_name and len(f_contract_name) > 3:
                    last_two = f_contract_name[-2:]
                    char_part = SQLUtil.remove_num(f_contract_name)
                    f_contract_name = char_part + '%' + last_two

                s_contract_name = contract_list[1].contract_name
                if s_contract_name and len(s_contract_name) > 3:
                    last_two = s_contract_name[-2:]
                    char_part = SQLUtil.remove_num(s_contract_name)
                    s_contract_name = char_part + '%' + last_two

                t_contract_name = contract_list[2].contract_name
                if t_contract_name and len(t_contract_name) > 3:
                    last_two = t_contract_name[-2:]
                    char_part = SQLUtil.remove_num(t_contract_name)
                    t_contract_name = char_part + '%' + last_two

                raw_sql = 'select a.high ahigh,a.low alow,a.open aopen,a.close aclose, b.high bhigh,b.low blow,' \
                          'b.open bopen,b.close bclose, c.high chigh,c.low clow,c.open copen,' \
                          'c.close cclose ,a.trading_time '
                f_contract_type = contract_list[0].contract_type
                if f_contract_type == "CTP" or f_contract_type is None:
                    raw_sql = raw_sql + 'from t_market_second_data a '
                elif f_contract_type == "ATP":
                    raw_sql = raw_sql + 'from t_market_second_data a '

                s_contract_type = contract_list[1].contract_type
                if s_contract_type == "CTP" or s_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_second_data b '
                elif s_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_second_data b '
                raw_sql = raw_sql + 'on a.trading_time=b.trading_time '

                t_contract_type = contract_list[2].contract_type
                if t_contract_type == "CTP" or t_contract_type is None:
                    raw_sql = raw_sql + 'left join t_market_second_data c '
                elif t_contract_type == "ATP":
                    raw_sql = raw_sql + 'left join t_market_second_data c '
                raw_sql = raw_sql + 'on a.trading_time=c.trading_time '

                raw_sql = raw_sql + "where a.contract_name like  '" + f_contract_name + "' "
                raw_sql = raw_sql + "and b.contract_name like  '" + s_contract_name + "' "
                raw_sql = raw_sql + "and c.contract_name like  '" + t_contract_name + "' "
                raw_sql = raw_sql + "and a.trading_time >=  '" + date_from + "' "
                raw_sql = raw_sql + "and a.trading_time <=  '" + date_to + "' "
                return raw_sql
            else:
                return ''
        return ''

    @staticmethod
    def get_contract_list_name(contract_list):
        all_contract_name = ''
        if contract_list is not None:
            for ontract_item in contract_list:
                contract_name = ontract_item.contract_name
                if contract_name and len(contract_name) > 3:
                    last_two = contract_name[-2:]
                    char_part = SQLUtil.remove_num(contract_name)
                    contract_name = char_part + '%' + last_two
                    all_contract_name = all_contract_name + contract_name + '_'
        return all_contract_name

    @staticmethod
    def contract_g(contract):
        if '3M' in contract:
            return contract
        arr = [''.join(list(g)) for k, g in groupby(contract, key=lambda x: x.isdigit())]
        s1 = arr[0]
        s2 = arr[1][-2:]
        if len(arr) == 3:
            s3 = s1 + s2 + arr[2]
        else:
            s3 = s1 + s2
        return s3
