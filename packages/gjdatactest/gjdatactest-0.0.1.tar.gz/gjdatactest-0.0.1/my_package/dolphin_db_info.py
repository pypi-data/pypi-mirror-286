# 此文件用于存放dolphinDB的相关信息，包括登录信息、数据库和表信息等。

""" 本地dolphindb数据库相关信息 """
# dolphindb -host localhost -port 8848 -user "admin" -password "123456"

# 登录信息
HOST = "localhost"  # 主机名或IP地址
PORT = 8848  # 端口号
USER_ID = "admin"  # 用户名
PASSWORD = "123456"  # 密码

# 数据库、表信息
''' get_price 行情数据接口所在的数据库和表 '''
get_price_db_path = "dfs://firstdb"  # 数据库路径
get_price_db_table_name = "get_price_tb"  # 表名

''' get_instruments 合约基础信息接口所在的数据库和表 '''
get_instruments_db_path = "dfs://firstdb"  # 数据库路径
get_instruments_db_table_name = "get_instruments_tb"  # 表名

''' get_trading_dates 交易日历接口所在的数据库和表 '''
get_trading_dates_db_path = "dfs://firstdb"   # 数据库路径
get_trading_dates_db_table_name = "get_trading_dates_tb"  # 表名

''' get_margin_ratio 期货保证金接口所在的数据库和表 '''
get_margin_ratio_db_path = "dfs://firstdb"  # 数据库路径
get_margin_ratio_db_table_name = "get_margin_ratio_tb"  # 表名

''' get_fee 期货交割手续费接口所在的数据库和表 '''
get_fee_db_path = "dfs://firstdb"  # 数据库路径
get_fee_db_table_name = "get_fee_tb"  # 表名

''' get_limit_position 期货限仓数据接口所在的数据库和表 '''
get_limit_position_db_path = "dfs://firstdb"  # 数据库路径
get_limit_position_db_table_name = "get_limit_position_tb"  # 表名

''' get_active_contract 主力/次主力合约接口所在的数据库和表 '''
get_active_contract_db_path = "dfs://firstdb"  # 数据库路径
get_active_contract_db_table_name = "get_active_contract_tb"  # 表名


""" 公司dolphindb数据库相关信息 """

# 登录信息
# COMPANY_HOST = "10.74.56.101"  # 主机名或IP地址
COMPANY_HOST = "10.66.200.248"  # 主机名或IP地址
# COMPANY_PORT = 24793  # 端口号
COMPANY_PORT = 8901  # 端口号
COMPANY_USER_ID = "sys_asset_zdgl"  # 用户名
COMPANY_PASSWORD = "zdgl@1qaz2wsx"  # 密码

''' 行情数据所在数据库和表 '''
# 历史期货行情数据 L1-tick数据
history_future_tick_db_path = "dfs://tick"  # 数据库路径
history_future_tick_db_table_name = "ctp_future_tick"  # 表名

# 历史期货行情 L1-分钟k线
history_future_min_db_path = "dfs://minutek"  # 数据库路径
history_future_min_db_table_name = "ctp_future_mink"  # 表名

# 历史期货行情 L1-日k线
history_future_day_db_path = "dfs://dayk"  # 数据库路径
history_future_day_db_table_name = "ctp_future_dayk"  # 表名

# 历史期权行情数据 tick数据
history_option_tick_db_path = "dfs:tick"  # 数据库路径
history_option_tick_db_table_name = "ctp_option_tick"  # 表名

# 历史期权行情数据 分钟k线
history_option_min_db_path = "dfs:minutek"   # 数据库路径
history_option_min_db_table_name = "ctp_option_mink"  # 表名

# 历史期权行情数据 5分钟k线
history_option_5min_db_path = "dfs:minutek"  # 数据库路径
history_option_5min_db_table_name = "ctp_future_mink5"  # 表名

# 历史期权行情数据 15分钟k线
history_option_15min_db_path = "dfs:minutek"  # 数据库路径
history_option_15min_db_table_name = "ctp_future_mink15"  # 表名

# 历史期权行情数据 日k线
history_option_day_db_path = "dfs:dayk"  # 数据库路径
history_option_day_db_table_name = "ctp_option_dayk"  # 表名

""" 基础信息 """

# 交易参数
trading_params_db_path = "dfs://basicinfo"  # 数据库路径
trading_params_db_table_name = "b_calendar"  # 表名

# 期货-合约信息
future_contract_db_path = "dfs://basicinfo"  # 数据库路径
future_contract_db_table_name = "t_fuinstrument"  # 表名

# 期权-合约信息
option_contract_db_path = "dfs://basicinfo"  # 数据库路径
option_contract_db_table_name = "t_optinstrument"  # 表名

# 交易日历
trading_dates_db_path = "dfs://basicinfo"  # 数据库路径
trading_dates_db_table_name = "b_calenday"  # 表名