# 此文件用于编写数据接口---类方式实现

import datetime
import holidays
import pandas as pd
import dolphindb as ddb
from pandas.tseries.offsets import BDay

from dict_data import get_price_frequency_dict, get_price_data_type_dict, get_instruments_type_dict
# from dolphin_db_info import HOST, PORT, USER_ID, PASSWORD, COMPANY_HOST, COMPANY_PORT, COMPANY_USER_ID, \
#     COMPANY_PASSWORD, get_price_db_path, get_price_db_table_name, \
#     get_instruments_db_path, get_instruments_db_table_name, get_margin_ratio_db_path, get_margin_ratio_db_table_name, \
#     get_fee_db_path, get_fee_db_table_name, get_limit_position_db_path, get_limit_position_db_table_name, \
#     get_active_contract_db_path, get_active_contract_db_table_name, \
#     history_future_tick_db_path, history_future_tick_db_table_name, history_future_min_db_path, \
#     history_future_min_db_table_name, history_future_day_db_path, history_future_day_db_table_name, \
#     history_option_tick_db_path, history_option_tick_db_table_name, history_option_min_db_path, \
#     history_option_min_db_table_name, history_option_5min_db_path, history_option_5min_db_table_name, \
#     history_option_15min_db_path, history_option_15min_db_table_name

from dolphin_db_info import *


class GJDataC:

    def __init__(self):
        # 数据库参数
        # 本地服务器

        self.host = HOST
        self.port = PORT
        self.user_id = USER_ID
        self.password = PASSWORD

        # 公司服务器
        # self.host = COMPANY_HOST
        # self.port = COMPANY_PORT
        # self.user_id = COMPANY_USER_ID
        # self.password = COMPANY_PASSWORD

        # 连接数据库
        self.db_session = ddb.session()
        self.db_session.connect(self.host, self.port, self.user_id, self.password)

        self.db_data = None  # 测试

        ''' get_price 接口相关属性 '''
        self.get_price_general_fields = ["order_book_ids", "datetime"]
        self.get_price_data = None  # 用于获取get_price接口数据

        ''' get_instruments 接口相关属性 '''
        self.get_instruments_general_fields = ["order_book_id"]
        self.get_instruments_data = None  # 用于获取get_instruments接口数据

        ''' get_margin_ratio 接口相关属性 '''
        self.get_margin_ratio_data = None  # 用于获取get_margin_ratio接口数据

        ''' get_fee 接口相关属性 '''
        self.get_fee_data = None  # 用于获取get_fee接口数据

        ''' get_limit_position 接口相关属性 '''
        self.get_limit_position_data = None  # 用于获取get_limit_position接口数据

        ''' get_activate_contract 接口相关属性 '''
        self.get_active_contract_data = None  # 用于获取get_activate_contract接口数据

        ''' 数据库相关操作 '''
        # self.connect_db()  # 将数据获取到内存中，后续直接从内存中获取数据
        #
        # self.db_session.close()  # 关闭数据库连接

    def connect_db(self):
        """
        连接dolphindb数据库获取数据
        return: 获取的数据
        """

        # 从数据库中获取数据
        get_price_data = self.db_session.loadTable(tableName=get_price_db_table_name, dbPath=get_price_db_path)
        get_instruments_data = self.db_session.loadTable(tableName=get_instruments_db_table_name,
                                                         dbPath=get_instruments_db_path)
        get_margin_ratio_data = self.db_session.loadTable(tableName=get_margin_ratio_db_table_name,
                                                          dbPath=get_margin_ratio_db_path)
        get_fee_data = self.db_session.loadTable(tableName=get_fee_db_table_name, dbPath=get_fee_db_path)
        get_limit_position_data = self.db_session.loadTable(tableName=get_limit_position_db_table_name,
                                                            dbPath=get_limit_position_db_path)
        get_active_contract_data = self.db_session.loadTable(tableName=get_active_contract_db_table_name,
                                                             dbPath=get_active_contract_db_path)

        ''' sql筛选操作 '''
        # print("总数据量: ", self.db_session.run("count", self.data))
        # print(self.data)
        # data = self.db_session.loadTableBySQL
        # (tableName="firsttb", dbPath="dfs://firstdb", sql="select * from firsttb")

        # 对数据进行筛选
        # data = data.select(["id", "sym", "price", "qty"]).where("id<2").toDF()  # 对数据进行筛选

        ''' 将Table对象转换为DataFrame对象 '''
        # 在数据库连接关闭之前将Table对象转换为DataFrame对象，以便后续直接从内存中获取数据
        self.get_price_data = get_price_data.toDF()
        self.get_instruments_data = get_instruments_data.toDF()
        self.get_margin_ratio_data = get_margin_ratio_data.toDF()
        self.get_fee_data = get_fee_data.toDF()
        self.get_limit_position_data = get_limit_position_data.toDF()
        self.get_active_contract_data = get_active_contract_data.toDF()
        self.db_data = get_price_data.toDF()  # 将数据从dolphindb表中获取到内存中

        print("test_data: ", self.get_price_data.iloc[0]["datetime"], type(self.get_price_data.iloc[0]["datetime"]))

        time_param = "2019-01-01 09:10:00"
        # 将时间参数转换为 pandas.Timestamp 类型
        start_time = pd.Timestamp(time_param)
        print("时间数据：", start_time, type(start_time))

        # 获取 `datetime` 列并转换为 pandas.Timestamp 类型
        # datetime_series = pd.to_datetime(get_price_data["datetime"])
        print("提取的时间列数据: \n", get_price_data["datetime"])

        # 筛选数据
        # filtered_data = datetime_series[(datetime_series <= start_time)]

        # print("筛选后的数据: \n", filtered_data)

    @staticmethod
    def connect_db_company(table_name, db_path):
        """ 此方法用于根据不同的数据表及数据库获取数据，只返回Table对象，对应的数据处理在对应的数据接口处理 """

        # 连接数据库
        db_session = ddb.session()
        db_session.connect(COMPANY_HOST, COMPANY_PORT, COMPANY_USER_ID, COMPANY_PASSWORD)

        # 从数据库中获取数据
        data = db_session.loadTable(tableName=table_name, dbPath=db_path)
        # print("所有数据\n", data)

        return data

    """ 通用方法 """

    @staticmethod
    def general_validate_params_required(param, param_name):
        """
        校验参数是否必填
        :param param: 参数值
        :param param_name: 参数名称
        """
        if not param:
            raise ValueError(f"{param_name} is required")

    @staticmethod
    def general_validate_either_or(field_1_name, field_1_value, field_2_name, field_2_value):
        """ 此方法用于验证二选一类型的参数情况 """
        if not field_1_value and not field_2_value:
            raise ValueError(f"{field_1_name} or {field_2_name} is required")
        if field_1_value and field_2_value:
            raise ValueError(f"{field_1_name} and {field_2_name} cannot be both provided")

    def general_validate_date(self, date_str):
        """
        判断字符串是否为datetime.date, datetime.datetime格式。
        param: date_str: 待判断的字符串。
        Returns:
            True: 如果是日期格式，返回 True。
            False: 否则返回 False。
        """
        if not self.general_validate_date_str_is_datetime_type(date_str):
            return self.general_validate_date_str_is_date_type(date_str)
        return True

    @staticmethod
    def general_validate_date_str_is_datetime_type(date_data):
        """
        此方法用于验证日期字段是否为可以转换为datetime的类型
        """

        try:
            datetime.datetime.strptime(date_data, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def general_validate_date_str_is_date_type(date_data):
        """
        此方法用于验证日期字段是否为可以转换为date的类型
        """

        try:
            datetime.datetime.strptime(date_data, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def general_validate_field_str_or_list(field_value, field_name):
        """
        对参数的类型进行校验，判断是否为字符串或字符串列表。
        :param field_value: 待校验的参数值。
        :param field_name: 待校验的参数名称。
        :return: None
        """

        if field_value and not isinstance(field_value, (str, list)):
            raise ValueError(f"{field_name} should be a string or a list of strings")

    @staticmethod
    def general_validate_param_is_str(param_name, param_value):
        """
        校验参数是否为str类型
        """

        if not isinstance(param_value, str):
            raise ValueError(f"{param_name} 类型错误，请传入 str 类型")

    def general_validate_asset_type(self, asset_type):
        """
        对asset_type进行校验
        :param asset_type: str, 合约类型
        :return: None
        """
        self.general_validate_params_required(asset_type, "asset_type")  # 校验必填参数
        if not isinstance(asset_type, str):
            raise ValueError("asset_type should be a string")
        if asset_type not in ["future", "option"]:
            raise ValueError("asset_type should be 'future' or 'option'")

    # def general_validate_fields_old(self, data, fields, field_list, asset_type):
    #     """
    #     对fields进行校验
    #     :param fields: 字段列表--用户传入的需要返回的字段
    #     :param field_list: 通用字段列表---每个接口通用的字段列表
    #     :param data: 接口数据
    #     :param asset_type: 合约类型
    #     :return: None
    #
    #     """
    #
    #     ''' 校验fields '''
    #     # 如果没有传入fields, 则返回所有字段
    #     if not fields:
    #         return data[data["type"] == asset_type]
    #     self.general_validate_field_str_or_list(fields, "fields")
    #
    #     ''' 根据fields进行处理 '''
    #     # 如果传入了fields，则根据传入的fields进行处理
    #     columns_list = data.columns.tolist()
    #
    #     if isinstance(fields, str):
    #         self._deal_fields(fields, columns_list, field_list)
    #         data = data[field_list + [fields]][
    #             data["type"] == asset_type]
    #     elif isinstance(fields, list):
    #         for field in fields:
    #             self._deal_fields(field, columns_list, field_list)
    #         data = data[
    #             [field for field in field_list] + fields][
    #             data["type"] == asset_type]
    #
    #     return data

    def general_validate_fields(self, data, fields):
        """
        对fields进行校验
        :param fields: 字段列表--用户传入的需要返回的字段
        :param data: 接口数据
        :return: None

        """

        ''' 校验fields '''
        # 如果没有传入fields, 则返回所有字段
        if not fields:
            return data
        self.general_validate_field_str_or_list(fields, "fields")

        ''' 根据fields进行处理 '''
        # 如果传入了fields，则根据传入的fields进行处理
        columns_list = data.columns.tolist()

        if isinstance(fields, str):
            self._deal_fields(fields, columns_list)
            data = data[[fields]]
        elif isinstance(fields, list):
            for field in fields:
                self._deal_fields(field, columns_list)
            data = data[fields]

        return data

    @staticmethod
    def _deal_fields(_field, columns_list):
        """
        处理fields
        :param _field: 用户需要返回的字段
        :param columns_list: 数据的所有字段列表
        """
        if _field not in columns_list:
            raise ValueError(
                f"fields: got invalided value '{_field}', choose any in "
                f"{columns_list}")

    @staticmethod
    def general_filter_data_by_field(data, field_name, field_value):
        """
        根据指定的字段进行数据过滤
        :param data: pandas.DataFrame, 数据
        :param field_name: str, 过滤字段
        :param field_value: str or list, 过滤值
        """

        return data[data[field_name].isin(field_value)] if isinstance(
            field_value, list) else data[data[field_name] == field_value]

    def _general_filter_data_by_field(self, data, field_name, field_value):
        self.general_validate_field_str_or_list(field_value, field_name)
        return self.general_filter_data_by_field(data, field_name, field_value)

    @staticmethod
    def general_date_str_to_date(date_str):
        """ 将date类型的str转换成datetime.date类型 """
        if isinstance(date_str, str):
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    """ get_price(获取行情数据接口) """

    def get_price(self, order_book_ids=None, asset_type="future", frequency=None, start_date=None, end_date=None,
                  fields=None):
        """
        行情数据接口
        :param order_book_ids: 合约代码--必填
        :param asset_type: 合约类型--必填, 默认为--'future'
        :param frequency: 频率--必填
        :param start_date: 开始日期--选填
        :param end_date: 结束日期--选填
        :param fields: 字段列表--选填
        :return: 行情数据
        """

        # 从数据库获取的数据是Table类型，需要转换为DataFrame类型, 并按照时间进行排序
        self.get_price_data = self.get_price_data.sort_values(by='datetime', ascending=True)

        ''' 数据校验 (先校验必填参数及类型)'''
        # 对order_book_ids进行校验
        self.get_price_validate_order_book_ids(order_book_ids)

        # 对asset_type进行校验
        self.general_validate_asset_type(asset_type)

        # 对frequency进行校验
        self.get_price_validate_frequency(frequency)

        # 对 start_date 和 end_date 进行校验
        self.get_price_validate_start_end_date(start_date, end_date)

        ''' 参数校验完成后，开始根据参数从服务器获取数据 '''
        # 根据order_book_ids, asset_type, frequency获取数据
        self.get_price_get_data(order_book_ids, asset_type, frequency)

        ''' 数据处理 '''
        # 根据frequency进行处理
        self.get_price_by_type_frequency(asset_type, frequency)

        # 根据order_book_ids筛选数据
        self.get_price_filter_by_order_book_ids(order_book_ids)

        # 对fields进行处理
        self.get_price_validate_fields(asset_type, fields)

        # 根据start_date和end_date筛选数据
        self.get_price_filter_by_date(start_date, end_date, order_book_ids)

        return self.get_price_data

    # @staticmethod
    def get_price_validate_order_book_ids(self, order_book_ids):
        """
        对order_book_ids 类型 以及 是否必填 进行校验
        """
        self.general_validate_params_required(order_book_ids, "order_book_ids")  # 校验必填参数
        self.general_validate_field_str_or_list(order_book_ids, "order_book_ids")

    def get_price_filter_by_order_book_ids(self, order_book_ids):
        """
        根据order_book_ids筛选数据
        """
        if isinstance(order_book_ids, str):
            self.get_price_data = self.get_price_data[self.get_price_data["order_book_ids"] == order_book_ids]
        elif isinstance(order_book_ids, list):
            self.get_price_data = self.get_price_data[self.get_price_data["order_book_ids"].isin(order_book_ids)]
        return self.get_price_data

    def get_price_validate_frequency(self, frequency):
        """
        对frequency进行校验
        """

        self.general_validate_params_required(frequency, "frequency")  # 校验必填参数
        if not isinstance(frequency, str):
            raise ValueError("frequency should be a string")

    def get_price_validate_start_end_date(self, start_date, end_date):
        """
        对 start_date 和 end_date 进行校验
        校验 start_date 和 end_date 是否同时提供，或者都不提供。
        """
        if (start_date and not end_date) or (not start_date and end_date):
            raise ValueError("start_date and end_date should be both provided or not provided at all")
        if start_date and end_date:
            # 如果提供了，则进行进一步校验
            is_start_datetime = self._is_datetime_or_convertible(start_date)
            is_end_datetime = self._is_datetime_or_convertible(end_date)
            if not is_end_datetime or not is_start_datetime:
                raise ValueError(
                    "start_date and end_date should be datetime.datetime objects or "
                    "convertible to datetime.datetime objects")

            # 如果传入的数据类型符合要求，进行转换
            start_date, end_date = self._get_price_convert_start_end_date(start_date, end_date)
            if start_date > end_date:
                raise ValueError("start_date should be earlier than end_date")

    @staticmethod
    def _get_price_convert_start_end_date(start_date, end_date):
        """
        将 start_date 和 end_date 转换为 datetime 类型。
        """

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S') if isinstance(start_date, str) \
            else start_date
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') if isinstance(end_date, str) \
            else end_date

        return start_date, end_date

    @staticmethod
    def _is_datetime_or_convertible(date_data):
        """
        判断 date_data 是否是 datetime 类型或可以转换成 datetime 类型的字符串，并精确到秒。
        param: date_data: 要判断的值。

        Returns:
            True 如果 start_date 是 datetime 类型或可以转换成 datetime 类型的字符串，否则 False。
        """

        if isinstance(date_data, datetime.datetime):
            return True
        elif isinstance(date_data, str):
            try:
                datetime.datetime.strptime(date_data, "%Y-%m-%d %H:%M:%S")
                return True
            except ValueError:
                return False
        else:
            return False

    def get_price_filter_by_date(self, start_date, end_date, order_book_ids):
        """
        根据start_date和end_date筛选数据
        """
        # 将'date_time'列转换为datetime类型
        try:
            if self.get_price_data['datetime'].dtype != 'datetime64[ns]':
                self.get_price_data['datetime'] = pd.to_datetime(self.get_price_data['datetime'])
        except ValueError:
            raise ValueError("source data's datetime format is not correct")

        # 如果传递了start_date 和 end_date, 则返回时间段内的数据
        if start_date and end_date:
            self.get_price_data = self.get_price_data[
                (self.get_price_data['datetime'] >= start_date) & (self.get_price_data['datetime'] <= end_date)]
            return self.get_price_data
        # 如果没有传递start_date 和 end_date, 则根据传入的order_book_ids返回每个合约距离当前时间最近的一条数据
        elif not start_date and not end_date:
            date_time = datetime.datetime.now()
            self.get_price_data = self.get_price_data[
                self.get_price_data["datetime"] <= date_time]

            # 根据传入的order_book_ids进行处理
            if isinstance(order_book_ids, str):
                self.get_price_data = self.get_price_data.tail(1)
            else:
                # 将order_book_id作为分组键，并找到每个分组中距离当前时间最近的数据
                nearest_data = self.get_price_data.groupby('order_book_ids')
                # 使用 tail(1) 获取每个组的最后一条数据
                self.get_price_data = nearest_data.apply(lambda x: x.tail(1)).reset_index(drop=True)

            return self.get_price_data

    # 对fields进行处理
    def get_price_validate_fields(self, asset_type, fields):
        """
        对fields进行校验
        :param asset_type: 合约类型
        :param fields: 字段列表 -- 用户传入的需要返回的字段

        """
        self.get_price_data = self.general_validate_fields(self.get_price_data, fields)

        return self.get_price_data

    # 根据合约类型和frequency获取数据
    def get_price_by_type_frequency(self, asset_type, frequency):
        # 判断asset_type是否存在
        if not get_price_frequency_dict.get(asset_type, None):
            raise ValueError(
                f"asset_type: got invalided value {asset_type}, choose any in {list(get_price_frequency_dict.keys())}")

        # frequency是否存在
        exists, suffix = self._ends_with(frequency, list(get_price_frequency_dict[asset_type].keys()))
        if not exists:
            raise ValueError(f"{frequency} is not a valid frequency for {asset_type} contract")
        # frequency存在再根据频率对数据做进一步处理
        else:
            bar_or_tick = get_price_frequency_dict[asset_type][suffix]  # 获取bar或tick
            self.get_price_by_type_frequency_bar_tick(asset_type, frequency, bar_or_tick)
            self.get_price_data_rename_columns(bar_or_tick)  # 重命名字段

        return self.get_price_data

    # 判断frequency的频率是否存在
    @staticmethod
    def _ends_with(variable, suffixes):
        """判断变量是否以列表中的元素结尾。
        :param variable: 待判断的变量
        :param suffixes: 列表，元素为字符串，表示后缀
        :return: True or False
        """
        for suffix in suffixes:
            if variable.endswith(suffix):
                return True, suffix
        return False, ""

    # bar行情和tick行情出参不同，需要单独处理
    # @staticmethod
    def get_price_by_type_frequency_bar_tick(self, asset_type, frequency, bar_or_tick):
        """
        future-期货枚举值：
        1d-对应日bar行情
        1min-对应分钟bar行情
        1min_gtja-对应我司合成的分钟bar行情
        tick_l1-对应L1级别tick行情
        tick_l2-对应L2级别tick行情

        option期权枚举值：
        1d-对应日bar行情
        1min-对应分钟bar行情
        tick-对应tick行情

        tick数据：按照交易频率统计的所有数据，例如：10s交易了5次，那就有5条tick数据
        """

        # 正式代码中，应该根据不同行情(bar or tick)返回对应的字段，因为order_book_ids和datetime是通用的，所以应该在这里排除
        # self.get_price_data = self.get_price_data[
        #     self.get_price_general_fields + [field for field in get_price_data_type_dict[bar_or_tick] if
        #                                      field not in self.get_price_general_fields]]

        # 测试使用字段(自己伪造的数据，字段不够完全)
        if bar_or_tick == "bar":
            self.get_price_data = self.get_price_data[
                self.get_price_general_fields + [field for field in self.get_price_data.columns.tolist() if
                                                 field not in self.get_price_general_fields]]
        else:
            self.get_price_data = self.get_price_data[
                self.get_price_general_fields + [field for field in ["order_book_ids", "open", "close"] if
                                                 field not in self.get_price_general_fields]]

        ''' 根据不同频率获取对应数据 '''

        if frequency.endswith("d"):
            self.get_daily_data(asset_type, frequency)
        elif frequency.endswith("min"):
            self.get_minute_data()
        elif frequency.endswith("tick"):
            self.get_tick_data()

        return self.get_price_data

    # 日级别数据
    # @staticmethod
    def get_daily_data(self, asset_type, frequency):
        """
        获取日级别数据
        :param asset_type: 合约类型---根据合约类型及频率获取对应的数据库及表
        :param frequency: 频率---根据合约类型及频率获取对应的数据库及表
        :return: 日级别数据

        """

        print("测试日频率数据: \n", self.db_data.head(10))

        return self.db_data

    # 分钟级别数据
    # @staticmethod
    def get_minute_data(self):
        """
        获取分钟级别数据
        :return: 分钟级别数据

        """

        print("测试分钟频率数据: \n", self.db_data.head(10))

        return self.db_data

    # tick级别数据
    # @staticmethod
    def get_tick_data(self):
        """
        获取tick级别数据
        :return: tick级别数据

        """

        print("测试tick数据: \n", self.db_data.head(10))

        return self.db_data

    def _get_price_get_data(self, order_book_ids, table_name, db_path):
        """
        用于接收数据表以及数据库，获取数据
        """
        get_price_data = self.connect_db(table_name, db_path)

        # 使用 DolphinDB 的 where 子句筛选数据
        if isinstance(order_book_ids, str):
            filtered_data = get_price_data.where(f"instrument_id='{order_book_ids}'").toDF()
        else:
            filtered_data = get_price_data.where(f"instrument_id in {order_book_ids}").toDF()

        return filtered_data

    def get_price_get_data(self, order_book_ids, asset_type, frequency):
        """ 根据参数获取数据库和表名，调用接口获取数据 """

        ''' 期货行情数据 '''
        if asset_type == "future":
            if frequency == "tick_l1":  # 期货l1级别tick行情数据
                self.get_price_data = self._get_price_get_data(order_book_ids, history_future_tick_db_table_name,
                                                               history_future_tick_db_path)
            elif frequency == "1d":  # 期货日bar行情数据
                self.get_price_data = self._get_price_get_data(order_book_ids, history_future_day_db_table_name,
                                                               history_future_day_db_path)
            elif frequency == "1min":  # 期货分钟bar行情数据
                self.get_price_data = self._get_price_get_data(order_book_ids, history_future_min_db_table_name,
                                                               history_future_min_db_path)
            # 数据库暂无数据
            # elif frequency == "1min_gtja":  # 公司合成的分钟bar行情数据
            #     # self.get_price_data = self._get_price_get_data(order_book_ids, history_future_min_gtja_db_table_name,
            #     #                                                history_future_min_gtja_db_path)
            # elif frequency == "tick_l2":  # 期货l2级别tick行情数据
            #     self.get_price_data = self._get_price_get_data(order_book_ids, history_future_tick_l2_db_table_name,
            #                                                      history_future_tick_l2_db_path)
            # else:
            #     raise Exception("frequency is not valid for future contract")
        elif asset_type == "option":
            if frequency == "1d":  # 期权日bar行情数据
                self.get_price_data = self._get_price_get_data(order_book_ids, history_option_day_db_table_name,
                                                               history_option_day_db_path)
            elif frequency == "1min":  # 期权分钟bar行情数据
                self.get_price_data = self._get_price_get_data(order_book_ids, history_option_min_db_table_name,
                                                               history_option_min_db_path)
            elif frequency == "tick":  # 期权tick行情数据
                self.get_price_data = self._get_price_get_data(order_book_ids, history_option_tick_db_table_name,
                                                               history_option_tick_db_path)
            else:
                raise Exception("frequency is not valid for option contract")
        else:
            raise Exception("asset_type is not valid")

    def get_price_data_rename_columns(self, bar_or_tick):
        """
        将从数据库中获取的数据列名重命名为文档要求的名字
        """

        if bar_or_tick == "bar":
            new_columns = {'trading_day': 'trading_day', 'trade_time': 'datetime', 'exchange_id': 'exchange_id',
                           'instrument_id': 'order_book_ids', 'open_price': 'open', 'highest_price': 'high',
                           'lowest_price': 'low', 'close_price': 'close', 'settlement_price': 'settlement',
                           'upper_limit_price': 'limit_up', 'lower_limit_price': 'limit_down',
                           'pre_settlement_price': 'prev_settlement',
                           'volume': 'volume', 'turnover': 'total_turnover', 'open_interest': 'open_interest'}
        else:
            new_columns = {'trading_day': 'trading_day', 'trade_time': 'datetime', 'exchange_id': 'exchange_id',
                           'instrument_id': 'order_book_ids', 'last_price': 'last', 'open_price': 'open',
                           'highest_price': 'high', 'lowest_price': 'low', 'close_price': 'close',
                           'settlement_price': 'settlement', 'upper_limit_price': 'limit_up',
                           'lower_limit_price': 'limit_down', 'pre_settlement_price': 'prev_settlement',
                           'pre_close_price': 'prev_close', 'volume': 'volume', 'turnover': 'total_turnover',
                           'open_interest': 'open_interest', 'ask_price1': 'a1', 'ask_price2': 'a2', 'ask_price3': 'a3',
                           'ask_price4': 'a4', 'ask_price5': 'a5', 'ask_volume1': 'a1_v', 'ask_volume2': 'a2_v',
                           'ask_volume3': 'a3_v', 'ask_volume4': 'a4_v', 'ask_volume5': 'a5_v', 'bid_price1': 'b1',
                           'bid_price2': 'b2', 'bid_price3': 'b3', 'bid_price4': 'b4', 'bid_price5': 'b5',
                           'bid_volume1': 'b1_v', 'bid_volume2': 'b2_v', 'bid_volume3': 'b3_v', 'bid_volume4': 'b4_v',
                           'bid_volume5': 'b5_v'}
        self.get_price_data = self.get_price_data.rename(columns=new_columns)

    """ get_instruments(合约基础信息) """

    def get_instruments(self, order_book_ids=None, commodity=None, asset_type=None, fields=None):
        """
        获取合约基础信息接口
        :param order_book_ids: str or list,合约代码 和 commodity_type 必填 二选一
        :param commodity: str or list, 合约品种  和 commodity_type 必填 二选一  若填写品种参数，则返回该品种所有合约基础信息
        :param asset_type: str, 合约类型--必填
        :param fields: str or list, 字段列表--选填，默认为全部字段
        :return: 返回一个 instrument 对象，或一个 instrument list
        """

        ''' 数据校验 '''
        # 对order_book_ids和commodity_type进行校验
        self.get_instruments_validate_order_book_ids_commodity(order_book_ids, commodity)

        # 对asset_type进行校验
        self.general_validate_asset_type(asset_type)

        # 对fields进行校验
        self.get_instruments_validate_fields(asset_type, fields)

        ''' 处理数据 '''
        # 根据asset_type返回数据（future和option需要返回的字段不同）
        self.get_instruments_by_asset_type(asset_type)

        return self.get_instruments_data

    def get_instruments_validate_order_book_ids_commodity(self, order_book_ids, commodity):
        """
        对order_book_ids和commodity_type进行校验
        order_book_ids和commodity_type二选一，且只能二选一
        :param order_book_ids: str or list,合约代码
        :param commodity: str or list, 合约品种
        :return: None
        """

        ''' 对order_book_ids和commodity_type进行校验 '''
        self.general_validate_either_or("order_book_ids", order_book_ids, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_ids:
            self.get_instruments_data = self._general_filter_data_by_field(self.get_instruments_data, "order_book_id",
                                                                           order_book_ids)

        if commodity:
            self.get_instruments_data = self._general_filter_data_by_field(self.get_instruments_data, "commodity",
                                                                           commodity)

    def get_instruments_filter_order_book_ids(self, order_book_ids):
        """
        根据order_book_ids筛选数据
        :param order_book_ids: str or list,合约代码
        :return: None
        """

        self.get_instruments_data = self.get_instruments_data[
            self.get_instruments_data["order_book_id"].isin(order_book_ids)] if isinstance(
            order_book_ids, list) else self.get_instruments_data[
            self.get_instruments_data["order_book_id"] == order_book_ids]

        return self.get_instruments_data

    def get_instruments_filter_commodity(self, commodity):
        """
        根据commodity筛选数据
        :param commodity: str or list, 合约品种
        :return: None

        """

        self.get_instruments_data = self.get_instruments_data[
            self.get_instruments_data["commodity"].isin(commodity)] if isinstance(
            commodity, list) else self.get_instruments_data[
            self.get_instruments_data["commodity"] == commodity]

        return self.get_instruments_data

    def get_instruments_validate_fields(self, asset_type, fields):
        """
        对fields进行校验
        :param fields: str or list, 字段列表
        :param asset_type: str, 合约类型
        :return: None
        """

        self.get_instruments_data = self.general_validate_fields(self.get_instruments_data, fields,
                                                                 self.get_instruments_general_fields, asset_type)

        return self.get_instruments_data

    def get_instruments_by_asset_type(self, asset_type):
        """
        根据asset_type返回不同的字段
        :param asset_type: str, 合约类型
        :return: None

        """

        try:
            # 根据asset_type返回不同的字段
            # self.get_instruments_data = self.get_instruments_data[
            #     [field for field in get_instruments_type_dict[asset_type]]]

            self.get_instruments_data = self.get_instruments_data[self.get_instruments_data["type"] == asset_type]
            return self.get_instruments_data
        except Exception:
            raise ValueError(
                f"asset_type: got invalided value {asset_type}, choose any in {list(get_instruments_type_dict.keys())}")

    """   get_trading_dates(交易日历)  """

    def get_trading_dates(self, date=datetime.date.today(), n=None, start_date=None, end_date=None):
        """
        获取交易日历接口
        :param date: str--选填, 日期
        :param n: str--必填，根据不同值获取对应的交易日历
        :param start_date: str（datetime.date, datetime.datetime）--选填, 开始日期
        :param end_date: str（datetime.date, datetime.datetime）--选填, 结束日期
        若填写【date、n】为入参，则无法填写【start_date、end_date】，反之依然
        :return:
        """

        """ 校验数据 """
        trading_calendar_result = self.get_trading_dates_validate_date_n_start_end(date, n, start_date, end_date)

        return trading_calendar_result

    def get_trading_dates_validate_date_n_start_end(self, date, n, start_date, end_date):
        """
        校验date、n和start_date、end_date有效性
        """

        if (date and n) and (start_date and end_date):
            raise ValueError("date、n和start_date、end_date只能二选一")

        if n and (start_date or end_date):
            raise ValueError("参数错误：不能同时传递date、n和start_date、end_date")
        elif date and n:  # 根据date和n获取交易日历
            return self.get_trading_dates_by_date_n(date, n)
        elif start_date and end_date:  # 根据start_date和end_date获取交易日历
            return self.get_trading_dates_by_start_end(start_date, end_date)
        else:
            raise ValueError("参数错误：请传递date、n或start_date、end_date")

    def get_trading_dates_by_date_n(self, date, n):
        """
        校验 date 和 n
        :param date: str--选填, 日期
        :param n: str--必填，根据不同值获取对应的交易日历
        :return: None
        """

        if isinstance(date, datetime.date):
            print(date, type(date))
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        return self.get_dates_in_n(date, n)

    def get_trading_dates_by_start_end(self, start_date, end_date):
        """
        根据start_date和end_date获取交易日历
        :param start_date: str（datetime.date, datetime.datetime）--选填, 开始日期
        :param end_date: str（datetime.date, datetime.datetime）--选填, 结束日期
        """

        # 校验日期类型
        if self.check_date_type(start_date, end_date):
            cn_holidays = holidays.CN()  # 创建中国节假日对象
            # 如果校验通过，则根据start_date和end_date获取交易日历
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            dates = []
            current_date = start_date
            while current_date <= end_date:
                if current_date not in cn_holidays and current_date.weekday() < 5:
                    dates.append(current_date)
                current_date += datetime.timedelta(days=1)
            return dates

    def check_date_type(self, _start_date, _end_date):
        """
        判断start_date和end_date是否为str，datetime.date, datetime.datetime三种类型，
        其中，如果是str类型，还要判断是否是datetime.date, datetime.datetime两种类型的字符串.
        params:
            _start_date: 开始日期。
            _end_date: 结束日期。
        Returns:
            True: 如果类型正确，返回 True。
            False: 否则返回 False，并打印错误信息。
        """
        if isinstance(_start_date, (str, datetime.date, datetime.datetime)) and \
                isinstance(_end_date, (str, datetime.date, datetime.datetime)):
            if isinstance(_start_date, str) and not self.general_validate_date(_start_date):
                raise ValueError("start_date 不是有效的日期字符串格式")
            if isinstance(_end_date, str) and not self.general_validate_date(_end_date):
                raise ValueError("end_date 不是有效的日期字符串格式")
            return True
        else:
            raise ValueError("start_date 或 end_date 类型错误，请传入 str，datetime.date 或 datetime.datetime 类型")

    def get_dates_in_n(self, _date, _n):
        """
        获取选定日期, 根据n值获取对应的交易日历。

        Args:
            _date: 选定的日期，可以是 datetime.date 或 datetime.datetime 对象。
            _n: 时间段，可以是 'week'、'month' 或 'year'。

        Returns:
            一个包含所有日期的列表，类型为 datetime.date。
        """

        cn_holidays = holidays.CN()  # 创建中国节假日对象
        if _n == "0":  # 判断选定日期是否为节假日
            # 判断当前日期是否为节假日
            if _date in cn_holidays:
                return True
            else:
                return False
        elif _n == "1":  # 选定日期未来最近一个交易日日期
            # 获取当前日期未来最近的一个工作日
            next_trading_day = _date + BDay(1)
            # 判断是否为节假日(因为next_trading_day的值为选定日期的下一个 工作日，所以不需要再判断是否为周末)
            if next_trading_day in cn_holidays:
                while next_trading_day in cn_holidays:
                    next_trading_day += BDay(1)  # 往后加一天
            return next_trading_day.date()
        elif _n == "2":
            # 获取选定日期的前一个日期
            yesterday = _date - datetime.timedelta(days=1)
            # 判断是否为周末
            weekday = yesterday.weekday()

            if weekday >= 5:
                while yesterday.weekday() >= 5:
                    yesterday = yesterday - datetime.timedelta(days=1)  # 往前加一天
            # 判断是否为节假日
            if yesterday in cn_holidays:
                while yesterday in cn_holidays:
                    yesterday += BDay(1)  # 往后加一天
            return yesterday
        elif _n == '3':
            # 获取当前周的开始日期和结束日期
            start_date, end_date = self.get_current_week(_date)
            dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        elif _n == '4':
            # 获取当前月的开始日期和结束日期
            start_date = _date.replace(day=1)
            end_date = _date.replace(day=1, month=_date.month + 1) - datetime.timedelta(days=1)
            dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        elif _n == '5':
            # 获取当前年的开始日期和结束日期
            start_date = _date.replace(month=1, day=1)
            end_date = _date.replace(month=12, day=31)
            dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        elif _n == '6':
            current_date = _date
            # 判断是否为周末
            weekday = current_date.weekday()
            if weekday >= 5:
                while current_date.weekday() >= 5:
                    current_date = current_date - datetime.timedelta(days=1)  # 往前加一天
            # 判断是否为节假日
            if current_date in cn_holidays:
                while current_date in cn_holidays:
                    current_date += BDay(1)  # 往后加一天
            dates = [current_date]
        else:
            raise ValueError("n 参数错误，取值范围应该在 [0, 1, 2, 3, 4, 5, 6]")

        # 将周末和节假日排除
        dates = [date_obj for date_obj in dates if date_obj.weekday() < 5 and date_obj not in cn_holidays]

        return dates

    @staticmethod
    def get_current_week(date_data):
        """
        获取选定日期的当周。

        Args:
            date_data: 选定的日期，可以是 datetime.date 或 datetime.datetime 对象。

        Returns:
            一个元组，包含当前周的开始日期和结束日期，类型为 datetime.date。
        """

        # 获取星期几 (0-6, 0代表星期一)
        weekday = date_data.weekday()

        # 计算当周的开始日期和结束日期
        start_date = date_data - datetime.timedelta(days=weekday)
        end_date = start_date + datetime.timedelta(days=6)

        return start_date, end_date

    """ get_margin_ratio 期货保证金 """

    def get_margin_ratio(self, order_book_id=None, commodity=None, date=datetime.datetime.now(), exchange=None):
        """
        获取期货保证金信息接口
        :param order_book_id: str--选填（和commodity二选一），合约代码
        :param commodity: str--选填（和order_book_id二选一），合约品种,如果入参为品种，则返回该品种条件下所有合约的保证金list
        :param date: datetime--必填（默认今天)，日期
        :param exchange: str--必填，交易所
        :return:
        """

        """ 校验数据 """
        # 校验order_book_id和commodity
        self.get_margin_ratio_validate_order_book_id_commodity(order_book_id, commodity)

        # 校验exchange
        self.get_margin_ratio_validate_exchange(exchange)

        # 校验date
        self.get_margin_ratio_validate_date(date)

        """ 处理数据 """
        # 根据date筛选数据
        self.get_margin_ratio_data_by_date(date)

        # 根据exchange筛选数据
        self.get_margin_ratio_data_by_exchange(exchange)

        return self.get_margin_ratio_data[["order_book_id", "commodity", "date", "exchange"]]

    def get_margin_ratio_validate_exchange(self, exchange):
        """ 校验exchange """

        self.general_validate_params_required(exchange, "exchange")  # 校验必填参数

        if not isinstance(exchange, str):
            raise ValueError("exchange should be str")

    def get_margin_ratio_validate_order_book_id_commodity(self, order_book_id, commodity):
        """ 校验order_book_id和commodity """

        ''' 对order_book_ids和commodity_type进行校验 '''
        self.general_validate_either_or("order_book_id", order_book_id, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_id:
            self.get_margin_ratio_data = self._general_filter_data_by_field(self.get_margin_ratio_data, "order_book_id",
                                                                            order_book_id)
        if commodity:
            self.get_margin_ratio_data = self._general_filter_data_by_field(self.get_margin_ratio_data, "commodity",
                                                                            commodity)

    def get_margin_ratio_validate_date(self, date):
        """ 校验date """

        if isinstance(date, (str, datetime.date, datetime.datetime)):
            if isinstance(date, str) and not self.general_validate_date(date):
                raise ValueError("date 不是有效的日期字符串格式")
            return True
        else:
            raise ValueError("date 类型错误，请传入 str，datetime.date 或 datetime.datetime 类型")

    def get_margin_ratio_data_by_date(self, date):
        """
        根据date筛选数据
        """

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.get_margin_ratio_data = self.get_margin_ratio_data[self.get_margin_ratio_data["date"] == date]

    def get_margin_ratio_data_by_exchange(self, exchange):
        """
        根据exchange筛选数据
        """

        self.get_margin_ratio_data = self.get_margin_ratio_data[self.get_margin_ratio_data["exchange"] == exchange]

    """ get_fee 期货交割手续费 """

    def get_fee(self, order_book_id=None, commodity=None, date=datetime.datetime.now(), exchange=None):
        """
        获取期货交割手续费信息接口
        :param order_book_id: str--选填（和commodity二选一），合约代码
        :param commodity: str--选填（和order_book_id二选一），合约品种,如果入参为品种，则返回该品种条件下所有合约的交割手续费list
        :param date: datetime--必填（默认今天)，日期
        :param exchange: str--必填，交易所
        :return:
        """

        """ 校验数据 """
        # 校验order_book_id和commodity
        self.get_fee_validate_order_book_id_commodity(order_book_id, commodity)

        # 校验exchange
        self.get_fee_validate_exchange(exchange)

        # 校验date
        self.get_fee_validate_date(date)

        """ 处理数据 """
        # 根据date筛选数据
        self.get_fee_data_by_date(date)

        # 根据exchange筛选数据
        self.get_fee_data_by_exchange(exchange)

        return self.get_fee_data[["order_book_id", "commodity", "date", "exchange"]]

    def get_fee_validate_exchange(self, exchange):
        """ 校验exchange """
        # 是否必填
        self.general_validate_params_required(exchange, "exchange")

        if not isinstance(exchange, str):
            raise ValueError("exchange should be str")

    def get_fee_validate_order_book_id_commodity(self, order_book_id, commodity):
        """ 校验order_book_id和commodity """

        ''' 对order_book_ids和commodity_type进行校验 '''
        self.general_validate_either_or("order_book_id", order_book_id, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_id:
            self.get_fee_data = self._general_filter_data_by_field(self.get_fee_data, "order_book_id",
                                                                   order_book_id)
        if commodity:
            self.get_fee_data = self._general_filter_data_by_field(self.get_fee_data, "commodity",
                                                                   commodity)

    def get_fee_validate_date(self, date):
        """ 校验date """

        if isinstance(date, (str, datetime.date, datetime.datetime)):
            if isinstance(date, str) and not self.general_validate_date(date):
                raise ValueError("date 不是有效的日期字符串格式")
            return True
        else:
            raise ValueError("date 类型错误，请传入 str，datetime.date 或 datetime.datetime 类型")

    def get_fee_data_by_date(self, date):
        """
        根据date筛选数据
        """

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.get_fee_data = self.get_fee_data[self.get_fee_data["date"] == date]

    def get_fee_data_by_exchange(self, exchange):
        """
        根据exchange筛选数据
        """

        self.get_fee_data = self.get_fee_data[self.get_fee_data["exchange"] == exchange]

    """ get_limit_position 期货限仓数据 """

    def get_limit_position(self, order_book_ids=None, commodity=None, date=datetime.date.today()):
        """
        获取期货限仓数据接口
        :param order_book_ids: str or list--选填（和commodity二选一），合约代码
        :param commodity: str or list--选填（和order_book_ids二选一），合约品种
        :param date: datetime.date--选填（默认今天)，日期
        :return:

        """
        """ 校验数据 """
        # 校验order_book_ids和commodity
        self.get_limit_position_validate_order_book_ids_commodity(order_book_ids, commodity)

        # 校验date
        self.get_limit_position_validate_date(date)

        """ 处理数据 """
        # 根据date筛选数据
        self.get_limit_position_data_by_date(date)

        return self.get_limit_position_data

    def get_limit_position_validate_order_book_ids_commodity(self, order_book_ids, commodity):
        """ 对order_book_ids和commodity_type进行校验 """
        self.general_validate_either_or("order_book_ids", order_book_ids, "commodity", commodity)

        ''' 根据order_book_ids和commodity_type进行筛选 '''
        # 因为前面已经对数据进行校验了，所以直接根据不同的参数进行筛选即可
        if order_book_ids:
            self.get_limit_position_data = self._general_filter_data_by_field(self.get_limit_position_data,
                                                                              "order_book_ids",
                                                                              order_book_ids)
        if commodity:
            self.get_limit_position_data = self._general_filter_data_by_field(self.get_limit_position_data,
                                                                              "commodity",
                                                                              commodity)

    def get_limit_position_validate_date(self, date):
        """ 校验date """

        if isinstance(date, (str, datetime.date, datetime.datetime)):
            if isinstance(date, str) and not self.general_validate_date(date):
                raise ValueError("date 不是有效的日期字符串格式")
            return True
        else:
            raise ValueError("date 类型错误，请传入 str，datetime.date 或 datetime.datetime 类型")

    def get_limit_position_data_by_date(self, date):
        """
        根据date筛选数据
        """

        if isinstance(date, str):
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.get_limit_position_data = self.get_limit_position_data[self.get_limit_position_data["date"] == date]

    """ get_active_contract 主力/次主力合约 """

    def get_active_contract(self, code=None, begin_date=None, start_date=datetime.date.today(),
                            end_date=datetime.date.today(), asset_type=None,
                            fields=None, source="3"):
        """
        获取主力/次主力合约信息接口
        :param code: str or str list--必填，品种
        :param begin_date: datetime--必填，指定日期
        :param start_date: date--必填，默认当天
        :param end_date: date--必填，默认当天
        :param asset_type: str--必填，active指主力；next_active次主力
        :param fields: str or str list--选填，返回字段，默认全部
        :param source: str--选填，数据源，默认研究所, 3个来源可选：1-数据中台, 2-米筐, 3-研究所

        :return:
        """

        """ 校验参数 """
        # 校验必填参数
        self.get_active_contract_validate_required_params(code, begin_date, start_date, end_date, asset_type)

        # 校验日期参数类型
        self.get_active_contract_validate_date_type(begin_date, start_date, end_date)

        """ 筛选数据 """

        # 根据code筛选数据
        self.get_active_contract_validate_code(code)

        # 根据日期数据筛选数据
        self.get_active_contract_filter_by_date(begin_date, start_date, end_date)

        # 根据asset_type筛选数据
        self.get_active_contract_filter_by_asset_type(asset_type)

        # 根据fields筛选数据
        self.get_active_contract_filter_data_by_fields(fields)

        # 根据source筛选数据
        self.get_active_contract_data_by_source(source)

        return self.get_active_contract_data

    def get_active_contract_validate_required_params(self, code, begin_date, start_date, end_date, asset_type):
        """ 校验参数是否必填 """

        params_dict = {
            "code": code,
            "begin_date": begin_date,
            "start_date": start_date,
            "end_date": end_date,
            "asset_type": asset_type
        }
        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)  # 校验必填参数

    def get_active_contract_validate_code(self, code):
        """ 校验code 类型 """
        self.general_validate_field_str_or_list(code, "code")
        self.get_active_contract_data = self.get_active_contract_data[
            self.get_active_contract_data["code"].isin(code)] if isinstance(code, list) else \
            self.get_active_contract_data[self.get_active_contract_data["code"] == code]

    def get_active_contract_validate_date_type(self, begin_date, start_date, end_date):
        """
        校验日期数据的类型
        """
        # 校验start_date 和 end_date 是否为datetime.date类型或者可以转换成该类型的str
        if isinstance(start_date, (str, datetime.date)) and isinstance(end_date, (str, datetime.date)):
            if isinstance(start_date, str) and not self.general_validate_date_str_is_date_type(start_date):
                raise ValueError("start_date 类型错误，请传入 datetime.date 类型")
            if isinstance(end_date, str) and not self.general_validate_date_str_is_date_type(end_date):
                raise ValueError("end_date 类型错误，请传入 datetime.date 类型")
        else:
            raise ValueError("start_date 或 end_date 类型错误，请传入datetime.date 类型")

        # 校验begin_date 是否为datetime.datetime类型或者为可以转换为该类型的字符串
        if isinstance(begin_date, (str, datetime.datetime)):
            if isinstance(begin_date, str) and not self.general_validate_date_str_is_datetime_type(begin_date):
                raise ValueError("begin_date 类型错误，请传入 datetime.datetime 类型")
        else:
            raise ValueError("begin_date 类型错误，请传入 datetime.datetime 类型")

    def get_active_contract_filter_by_date(self, begin_date, start_date, end_date):
        """
        根据日期筛选数据
        """

        if start_date > end_date:
            raise ValueError("start_date should be earlier than end_date")

        # 根据start_date 和 end_date 筛选数据
        start_date = self.general_date_str_to_date(start_date)
        end_date = self.general_date_str_to_date(end_date)
        self.get_active_contract_data = self.get_active_contract_data[
            (self.get_active_contract_data["date"] >= start_date) & (self.get_active_contract_data["date"] <= end_date)]

        return self.get_active_contract_data

    def get_active_contract_filter_by_asset_type(self, asset_type):
        """
        根据asset_type筛选数据
        """

        self.get_active_contract_data = self.general_filter_data_by_field(self.get_active_contract_data,
                                                                          "active_type",
                                                                          asset_type)

    def get_active_contract_filter_data_by_fields(self, fields):
        """
        根据fields筛选数据
        """

        if isinstance(fields, (str, list)):
            self.get_active_contract_data = self.get_active_contract_data[fields] if isinstance(fields, str) else \
                self.get_active_contract_data[[field for field in fields]]

    @staticmethod
    def get_active_contract_data_by_source(source):
        """
        根据数据源筛选数据
        """

        if not isinstance(source, str):
            raise ValueError("source 类型错误，请传入 str 类型")

        if source == "1":
            print("数据中台")
        elif source == "2":
            print("米筐")
        elif source == "3":
            print("研究所")
        else:
            raise ValueError("source 参数错误，取值范围应该在 [1, 2, 3]")

    """ get_basic_data 库存/基差/现货价格-数据（日频） """

    def get_basic_data(self, order_book_id, asset_type, start_date, end_date):
        """
        获取库存/基差/现货价格-数据（日频）接口
        :param order_book_id: str--必填，合约代码
        :param asset_type: str--必填，枚举值：库存、基差、现货
        :param start_date: str, datetime.date, datetime.datetime, pandasTimestamp--必填，开始日期
        :param end_date: str, datetime.date, datetime.datetime, pandasTimestamp--必填，结束日期
        """

        """ 校验参数 """

        # 校验必填参数
        self.get_basic_data_validate_required_params(order_book_id, asset_type, start_date, end_date)

        # 校验order_book_id 类型
        self.get_basic_data_validate_order_book_id(order_book_id)

        # 校验asset_type 类型
        self.get_basic_data_validate_asset_type(asset_type)

        # 校验start_date 和 end_date 类型
        self.get_basic_data_validate_date(start_date, end_date)

        return None

    def get_basic_data_validate_required_params(self, order_book_id, asset_type, start_date, end_date):
        params_dict = {
            "order_book_id": order_book_id,
            "asset_type": asset_type,
            "start_date": start_date,
            "end_date": end_date
        }
        for key, value in params_dict.items():
            self.general_validate_params_required(value, key)  # 校验必填参数

    def get_basic_data_validate_order_book_id(self, order_book_id):
        """
        校验order_book_id 类型
        """

        self.general_validate_param_is_str("order_book_id", order_book_id)

    def get_basic_data_validate_asset_type(self, asset_type):
        """
        校验asset_type 类型
        """

        self.general_validate_param_is_str("asset_type", asset_type)

    def get_basic_data_validate_date(self, start_date, end_date):
        """
        校验start_date 和 end_date 类型
        """
        error_msg = "start_date 或 end_date 类型错误，datetime.date, datetime.datetime, pandasTimestamp类型或者可以转换成该类型的str"

        # 校验start_date 和 end_date 是否为datetime.date, datetime.datetime, pandasTimestamp类型或者可以转换成该类型的str
        if isinstance(start_date, (str, datetime.date, datetime.datetime, pd.Timestamp)) and isinstance(end_date, (
                str, datetime.date, datetime.datetime, pd.Timestamp)):
            if isinstance(start_date, str) and not self.general_validate_date(start_date):
                raise ValueError(error_msg)
            if isinstance(end_date, str) and not self.general_validate_date(end_date):
                raise ValueError(error_msg)
        else:
            raise ValueError(error_msg)
