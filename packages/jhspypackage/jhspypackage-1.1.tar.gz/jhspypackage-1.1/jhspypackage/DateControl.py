# -*- coding:utf-8 -*-
import datetime
import pandas as pd
from dateutil.parser import parse

def is_valid_timestamp_float(timestamp_str):
    try:
        # 尝试转换为 datetime 对象
        datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        return True
    except ValueError:
        return False
# 时间字符串按小时向上取整
def updating_dateStr_ceil_hors(ipt_time_str):
    """
    引入datetime和math模块。
    定义时间字符串time_str。
    使用strptime函数将字符串转换为datetime对象，并赋值给变量dt。
    判断分钟位是否为零，如果不为零，则将小时数向上取整；否则，保留原小时数。将得到的小时数赋值给变量hour。
    使用replace方法将hour设置为向上取整后的小时数，将minute和second设置为0，得到向上取整1小时后的datetime对象，赋值给变量hour_dt。
    打印hour_dt，即可得到向上取整1小时后的时间。
    """
    time_str = ipt_time_str  # "2020-09-06 22:30:00"
    if is_valid_timestamp_float(time_str):
        dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    if dt.minute != 0:
        dt = dt + datetime.timedelta(hours=1)
    hour_dt = dt.replace(minute=0, second=0)
    # print(hour_dt)
    return str(hour_dt)

def getCSVFileName(mainFilePath, Id_FieldHeader, Id_xuhao):
    CSVFileName = []
    # 关键表头读取
    # path = r"DisasterTable.xlsx"
    path = mainFilePath
    df = pd.read_excel(path)
    # df_ID = df[df['临近流域编号'] == Id_watershed]
    df_ID = df[df[Id_FieldHeader] == Id_xuhao]
    ymdStr = str(df_ID['发生日期'].tolist()[0])[:10]
    hmStr = str(df_ID['发生时间'].tolist()[0])[:8]
    dt = ymdStr + " " + hmStr
    dt_add1r = str(parse(dt) + datetime.timedelta(hours=1))
    dt_sub1r = str(parse(dt) - datetime.timedelta(hours=1))

    # 凉山-2021-07-01 00_00_00灾害实时预警.csv
    # 5134-2021-09-13 00_00_00灾害实时预警.csv
    CSVFileName.append('5134-' + dt_sub1r[:13] + '_00_00灾害实时预警.csv')
    CSVFileName.append('5134-' + dt[:13] + '_00_00灾害实时预警.csv')
    CSVFileName.append('5134-' + dt_add1r[:13] + '_00_00灾害实时预警.csv')

    return CSVFileName
#根据时间节点和范围生成时间序列 hours_range ：以时间节点为中心，前后跨过的小时数；dateTimeNodeStr 格式为 2021-08-08 00:00:00
def make_daytime_list_by_datenode(dateTimeNodeStr, hours_range):
    dtList = []
    rangeTime = hours_range  # 整型
    dt_Str = dateTimeNodeStr
    start_time_node = parse(dt_Str) - datetime.timedelta(hours=rangeTime)
    for i in range(int(rangeTime*2)):
        dtList.append(str(start_time_node))
        start_time_node = start_time_node + datetime.timedelta(hours=1)
    return dtList
#根据时间节点和范围生成时间序列 hours_range ：以时间节点为准，向前跨过的小时数；dateTimeNodeStr 格式为 2021-08-08 00:00:00
def make_before_daytime_list_by_datenode(dateTimeNodeStr, hours_range):
    dtList = []
    rangeTime = hours_range  # 整型
    dt_Str = dateTimeNodeStr
    start_time_node = parse(dt_Str) - datetime.timedelta(hours=rangeTime-1)
    for i in range(int(rangeTime)):
        dtList.append(str(start_time_node))
        start_time_node = start_time_node + datetime.timedelta(hours=1)
    return dtList

def make_before_daytime_list_by_datenode_sudo(dateTimeNodeStr, hours_range, delta_hours):
    dtList = []
    rangeTime = hours_range  # 整型
    dt_Str = dateTimeNodeStr
    start_time_node = parse(dt_Str) - datetime.timedelta(hours=rangeTime-1)
    for i in range(int(rangeTime/delta_hours)):
        dtList.append(str(start_time_node))
        start_time_node = start_time_node + datetime.timedelta(hours=delta_hours)
    return dtList
# 用于GLDAS数据的逐三小时
def make_before_daytime_list_by_datenode_sudo_for_gldas(dateTimeNodeStr, hours_range, delta_hours):
    dtList = []
    rangeTime = hours_range  # 整型
    dt_Str = obtain_three_hours_datanotes(dateTimeNodeStr)
    start_time_node = parse(str(dt_Str)) - datetime.timedelta(hours=rangeTime-delta_hours)
    for i in range(int(rangeTime/delta_hours)):
        dtList.append(str(start_time_node))
        start_time_node = start_time_node + datetime.timedelta(hours=delta_hours)
    return dtList

def make_daytime_list_by_datenode_two_sides_for_gldas(dateTimeNodeStr, hours_range, delta_hours):
    dtList = []
    rangeTime = hours_range  # 整型
    dt_Str = obtain_days_datanotes_for_gldas(dateTimeNodeStr)
    start_time_node = parse(str(dt_Str)) - datetime.timedelta(hours=rangeTime)
    for i in range(int(2*rangeTime/delta_hours)):
        dtList.append(str(start_time_node))
        start_time_node = start_time_node + datetime.timedelta(hours=delta_hours)
    return dtList
# 将小时部分取整为3的倍数
def round_to_nearest_multiple_of_three(hour):
    return 3 * int(hour / 3)
def obtain_three_hours_datanotes(time_str):
    from datetime import datetime, timedelta
    # 定义时间节点
    # time_str = "2021/6/7 0:40:00"
    if is_valid_timestamp_float(time_str):
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # 将小时部分取整为3的倍数
    new_hour = round_to_nearest_multiple_of_three(time_obj.hour)
    # 创建新的时间节点
    new_time_obj = time_obj.replace(hour=new_hour, minute=0, second=0)
    # 检查并调整日期，如果小时部分被取整为24
    if new_time_obj.hour >= 24:
        new_time_obj = new_time_obj + timedelta(days=1)
        new_time_obj = new_time_obj.replace(hour=0)
    # print("原始时间节点:", time_obj)
    # print("取整后的时间节点:", new_time_obj)
    return new_time_obj
# 日期取前一天  "2021/6/7 05:40:00" 变为 "2021/6/7 00:00:00"
def obtain_days_datanotes_for_gldas(time_str):
    from datetime import datetime, timedelta
    # 定义时间节点
    # time_str = "2021/6/7 0:40:00"
    if is_valid_timestamp_float(time_str):
        time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # 创建新的时间节点
    new_time_obj = time_obj.replace(hour=0, minute=0, second=0)
    # # 检查并调整日期，如果小时部分被取整为24
    # if new_time_obj.hour >= 24:
    #     new_time_obj = new_time_obj + timedelta(days=1)
    #     new_time_obj = new_time_obj.replace(hour=0)
    # print("原始时间节点:", time_obj)
    # print("取整后的时间节点:", new_time_obj)
    return new_time_obj

def get_before_daytime_by_datenode(dateTimeNodeStr, hours_range):
    rangeTime = hours_range  # 整型
    dt_Str = dateTimeNodeStr
    start_time_node = parse(dt_Str) - datetime.timedelta(hours=rangeTime-1)
    return str(start_time_node)

#根据时间节点和范围生成时间序列 hours_range ：以时间节点为准，向后跨过的小时数；dateTimeNodeStr 格式为 2021-08-08 00:00:00
def make_after_daytime_list_by_datenode(dateTimeNodeStr, hours_range):
    dtList = []
    rangeTime = hours_range  # 整型
    dt_Str = dateTimeNodeStr
    start_time_node = parse(dt_Str)
    for i in range(int(rangeTime)):
        dtList.append(str(start_time_node))
        start_time_node = start_time_node + datetime.timedelta(hours=1)
    return dtList
def get_after_daytime_by_datenode(dateTimeNodeStr, hours_range):
    rangeTime = hours_range  # 整型
    dt_Str = dateTimeNodeStr
    start_time_node = parse(dt_Str)
    start_time_node = start_time_node + datetime.timedelta(hours=hours_range)
    return str(start_time_node)

# 根据时间生成文件名序列
def make_filename_list_by_datetime(start_time, end_time, filetype, nameprefix):
    """
    根据时间生成文件名序列,输入时间格式为 2020-08-01 22:00:00
    :param: filetype: 生成的文件名后缀
    :return: 返回时间序列的文件名list
    """
    star_ttime = str(start_time)
    end_ttime = str(end_time)
    final = parse(end_ttime)
    dt_add1d = parse(star_ttime)
    filename_list = []

    while not(str(dt_add1d)[:10] == str(final)[:10]):
        # 生成文件名
        tem_filename = nameprefix + str(dt_add1d)[:4]+str(dt_add1d)[5:7]+str(dt_add1d)[8:10]+filetype
        filename_list.append(tem_filename)
        dt_add1d = dt_add1d + datetime.timedelta(days=1)
    return filename_list
def get_timedif_seconds(start_datetime,end_datetime):
    if isinstance(start_datetime, str):
        # 如果是字符串类型,可以先转一下datetime类型
        start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S.%f")
    if isinstance(end_datetime, str):
        # 如果是字符串类型,可以先转一下datetime类型
        end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S.%f")
    time_dif = (end_datetime-start_datetime).seconds
    return time_dif
if __name__ == '__main__':
    # 计时开始
    # start_time = datetime.datetime.now()
    # time.sleep(3)
    # # 计时结束
    # end_time = datetime.datetime.now()
    # time_dif = get_timedif_seconds(start_time, end_time)
    # print("预测耗时：" + str(time_dif) + " s")
    time_str = "2020-09-06 23:30:00"
    updating_dateStr_ceil_hors(time_str )
