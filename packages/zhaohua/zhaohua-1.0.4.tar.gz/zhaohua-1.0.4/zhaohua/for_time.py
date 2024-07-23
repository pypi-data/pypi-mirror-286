#########################################################################################################
# get_time() 功能:获取当前时间并按照指定格式返回。

# 参数:time_format(str): 指定时间格式的字符串。
# 可选值有：
# - "full": 返回完整的日期和时间，格式为'YYYY-MM-DD HH:MM:SS'。
# - "day"或"date": 返回日期，格式为'YYYY-MM-DD'。
# - 其他值: 返回时间，格式为'HH:MM:SS'。


# 示例:
# >> > get_time() 返回:'2024-07-22 14:23:45'
# >> > get_time("day") 返回:'2024-07-22'
# >> > get_time("time") 返回:'14:23:45'
#########################################################################################################

import time


def get_time(time_format="full"):
    """
    获取当前时间并按照指定格式返回。

    参数:
        time_format (str): 指定时间格式的字符串。可选值有：
            - "full": 返回完整的日期和时间，格式为 'YYYY-MM-DD HH:MM:SS'。
            - "day" 或 "date": 返回日期，格式为 'YYYY-MM-DD'。
            - 其他值: 返回时间，格式为 'HH:MM:SS'。
    """
    # 获取当前时间
    t = time.localtime()

    if time_format == "full":
        # 格式化时间
        s = time.strftime('%Y-%m-%d %H:%M:%S', t)
    elif time_format == "day" or time_format == "date":
        # 格式化时间
        s = time.strftime('%Y-%m-%d', t)
    else:
        # 格式化时间
        s = time.strftime('%H:%M:%S', t)

    # 将格式化后的时间返回
    return s
