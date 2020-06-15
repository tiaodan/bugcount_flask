import datetime

start_time_str = '2020-06-01'
end_time_str = '2020-06-30'
dateDiffrent = 7
#减法sub

print('开始时间', start_time_str)
start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d')
end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d')
print('开始时间', start_time)

delta = datetime.timedelta(days=6)
n_days = start_time + delta

datesub = (end_time - start_time).days # 起始 终止时间相减
print('时间差，=', datesub)

fortimes = datesub // (dateDiffrent)
print('循环了多少次', fortimes)

# 取余>=0 endTime = endtime_x 都= endtime，如果mod >0 多算一段时间 mod=0 不用多算一段时间
# if datesub % dateDiffrent = 0:
    # pass
date_submit_date = list()
date_submit_date.append(start_time_str)

for i in range(0, fortimes):  # 包左不包右
    # 是起始时间就不 -1
    # 是终止时间就 替换从endtime_x
    print(f'当前第{i}次循环')

    delta = datetime.timedelta(days=dateDiffrent * (i + 1) - 1)
    bug_submit_time_str = datetime.datetime.strftime((start_time + delta), '%Y-%m-%d')
    date_submit_date.append(bug_submit_time_str)
    print(date_submit_date)

days = list()
print('这段时间内的时间应该是', n_days.strftime('%Y-%m-%d'))