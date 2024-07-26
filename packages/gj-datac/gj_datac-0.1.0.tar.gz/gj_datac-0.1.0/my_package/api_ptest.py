# 此文件用于从data_api.py中导入所有函数，并进行测试

import datetime

from data_api_class import GJDataC

gj_data_c_obj = GJDataC()

# print("\n================================= get_price 分割线 ==========================\n")

# get_price_result = gj_data_c_obj.get_price(order_book_ids=['AC001', 'AC002'], start_date='2019-01-01 09:10:00',
#                                  end_date='2019-01-31 09:10:00', asset_type='option',
#                                  frequency="tick")

# # 调用get_price方法，行情数据
# 期货
# get_price_result = gj_data_c_obj.get_price(order_book_ids=["A1001", "C1001"], asset_type='future',
#                                            # start_date='2019-01-01 09:10:00', end_date=datetime.datetime.now(),
#                                            start_date='2010-01-04 09:01:00', end_date='2010-01-15 14:56:00',
#                                            frequency="tick", fields=["order_book_ids", "datetime", "exchange_id"])

# 期权
# get_price_result = gj_data_c_obj.get_price(order_book_ids=["M1711P2600", "M1803P3050"], asset_type='option',
#                                         #    start_date='2019-01-01 09:10:00', end_date=datetime.datetime.now(),
#                                            start_date='2018-01-02 00:00:00', end_date='2018-02-08 14:56:00',
#                                            frequency="1d", fields=["order_book_ids", "datetime", "exchange_id"])
# print("\n get_price返回的行情数据: \n", get_price_result)
# get_price_result.to_csv("~/first_folder/Task/GJDatacAPI/future_min_data.csv")

# print("\n================================= get_instruments 分割线 ================================\n")
# # 调用get_instruments方法，合约基础信息
# # get_instruments_result = get_price_api.get_instruments(order_book_ids=['AC001', 'AC002'], asset_type='option',
# # get_instruments_result = get_price_api.get_instruments(order_book_ids="AC001", asset_type='option',
# #                                          fields=["open", "close"])
# # get_instruments_result = get_price_api.get_instruments(commodity=['FA', 'AC'], asset_type='future')
# get_instruments_result = gj_data_c_obj.get_instruments(order_book_ids=['AC001', 'AC002'], asset_type='future')
# print("\n get_instruments返回的合约基础信息: \n", get_instruments_result)
#
print("\n================================= get_trading_dates 分割线 ============================\n")
get_trading_dates_result = gj_data_c_obj.get_trading_dates(date='2024-07-15', n="3")
# get_trading_dates_result = gj_data_c_obj.get_trading_dates(start_date='2024-07-15', end_date='2024-07-21')
print("get_trading_dates返回的交易日数据\n", get_trading_dates_result)
#
# print("\n=================================== get_margin_ratio 分割线=================================\n")
# # get_margin_ratio_result = gj_data_c_obj.get_margin_ratio(order_book_id=['AC001', 'AC002'], date="2024-07-15 09:10:00",
# # exchange='DCE')
# # get_margin_ratio_result = gj_data_c_obj.get_margin_ratio(order_book_id="AC001", date="2024-07-15", exchange='DCE')
# get_margin_ratio_result = gj_data_c_obj.get_margin_ratio(commodity='AC', date="2019-01-01 13:21:12", exchange='XSHG')
# print("\n get_margin_ratio返回的期货保证金数据: \n", get_margin_ratio_result)
#
# print("\n=================================== get_fee 分割线=================================\n")
# # get_fee_result = gj_data_c_obj.get_fee(order_book_id=['AC001', 'AC002'], date="2024-07-15 09:10:00", exchange='DCE')
# # get_fee_result = gj_data_c_obj.get_fee(order_book_id="AC001", date="2024-07-15", exchange='DCE')
# get_fee_result = gj_data_c_obj.get_fee(commodity='AC', date="2019-01-01 10:22:01", exchange='XSHG')
# print("\n get_fee返回的期货交割手续费数据: \n", get_fee_result)
#
# print("\n=================================== get_limit_position 分割线=================================\n")
# get_limit_position_result = gj_data_c_obj.get_limit_position(commodity='AC', date="2019-01-01 10:22:01")
# print("\n get_limit_position返回的期货交割手续费数据: \n", get_limit_position_result)
#
# print("\n=================================== get_active_contract 分割线=================================\n")
# get_active_contract_result = gj_data_c_obj.get_active_contract(code=['AC', 'CD'], begin_date="2019-01-01 10:22:01",
#                                                                start_date="2019-01-01",
#                                                                end_date="2019-01-31", asset_type='active',
#                                                                # fields="order_book_id")
#                                                                fields=["order_book_id", "code", "active_type", "date"],
#                                                                source="1")
# print("\n get_active_contract 返回的主力/次主力合约数据: \n", get_active_contract_result)
#
# print("\n=================================== get_basic_data 分割线=================================\n")
# get_basic_data_result = gj_data_c_obj.get_basic_data(order_book_id="AC001", asset_type='库存',
#                                                      start_date="2019-01-01", end_date="2019-01-31")
# print("\n get_basic_data 返回的主力/次主力合约数据: \n", get_basic_data_result)
