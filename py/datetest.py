import time
# 日期转时间戳
a1 = "2020/5/8"
# 先转换为时间数组
timeArray = time.strptime(a1, "%Y/%m/%d")
#
# 转换为时间戳
timeStamp = int(time.mktime(timeArray))
print(timeStamp)

bug_submit_date = sheet.cell(r, 0).value
#
# # 格式转换 - 转为 /
# a2 = "2019/5/10 23:40:00"
# # 先转换为时间数组,然后转换为其他格式
# timeArray = time.strptime(a2, "%Y/%m/%d %H:%M:%S")
# otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
# print(otherStyleTime)

# bug_submit_date = datetime.strptime(bug_submit_date, '%Y/%m/%d')  # 日期类型的
# bug_submit_date = datetime.date(datetime.strptime(bug_submit_date, '%Y/%m/%d'))  # 日期类型的