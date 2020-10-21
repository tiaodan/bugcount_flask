# str和日期转换
from datetime import datetime
import xlrd
import xlwt
import  pandas
import xlsxwriter
from py import utils

# 日期格式
# datastyle = xlwt.XFStyle()
# # datastyle.num_format_str = 'yyyy-mm-dd'
# datastyle.num_format_str = "yyyy/m/d"
# row=0
# col=1
# value = "2018/8/3"

# utils.checkFileExist("C:\\software\\test.xls")
# utils.get_excel_show_sheetnames("C:\\software\\test.xls")
# utils.get_excel_hide_sheetnames("C:\\software\\test.xls")
# utils.check_excel_tablehead("C:\\software\\test.xls", ['Sheet1'], [])

# book = utils.openexcel_return_workbook("../excel_upload/template.xlsx")
# showsheets = utils.get_excel_show_sheetnames("../excel_upload/template.xlsx", book)
# showsheets = utils.get_excel_show_sheetnames("../excel_upload/template.xlsx")
tablehead = ['提交日期', '项目', '软件类', '测试版本', '描述',
     '严重等级', '优先级', '难度', '关闭情况', '关闭日期',
     '关闭版本', '原因分析', '问题图片', '中间情况', '开发者',
     '备注', '回归次数', '重开次数', '提交者索引']
utils.checkexcel_data('C:\\Users\\root\\Desktop\\工具\\11. Navicat\\fu.xlsx', tablehead)

# print('aaaa\nss\n' + 'sssssss')
# book = xlrd.open_workbook('../excel_upload/template.xlsx')
# sheet = book.sheet_by_name('视频问题')
# print(sheet.cell_value(1, 10))
# if sheet.cell_value(1, 10) == '':
#     print('haaha')
# print(type(sheet.cell_value(0, 1)))
# print(sheet.cell_note_map)
# print(sheet.cell_type(1, 77))
# # print(sheet.cell_xf_index(0, 1))



"""
show_sheetnames = utils.get_excel_show_sheetnames("../excel_upload/template.xlsx")
utils.check_excel_tablehead("../excel_upload/template.xlsx", show_sheetnames, tablehead)
"""
"""
def aa(*a):
    print(a)
    print(type(a))
    print(len(a))
aa('1')
aa()
"""
# # a = ('1808', '1901')
# a = (('1808',), ('C8 3+4G',), ('FH03',), ('JC二期',), ('K项目',), ('K项目-多仓库',), ('K项目-马来',), ('K项目-鹰潭',), ('LJG',), ('WRJ',), ('ZG',), ('大S北向审计日志系统',), ('大S项目',), ('视频问题',))
# a = list(a)
#
# print(a)
# print(type(a[0][0]))
# # a = list(a)
# print(a[0][0])
# print(type(a[0]))
# 写入
# wb = xlwt.Workbook()
# ws = wb.add_sheet('Sheet1')
# ws.write(row, col, value, datastyle)
# wb.save('C:\\software\\test.xls')

# # 读取内容：
# book = xlrd.open_workbook("C:\\software\\test.xls")
# sheet1 = book.sheet_by_name("Sheet1")
# print(sheet1.name)
# print(sheet1.visibility)

# sheet = book.sheet_by_name("Sheet1")
# print('!!!!!!!!!!!!!!!!!!!!excel日期sheet.value', sheet.cell(1, 0).value)
# print('!!!!!!!!!!!!!!!!!!!!excel日期sheet.value.type', type(sheet.cell(1, 0).value))

# book = xlsxwriter.Workbook("C:\\software\\test1.xlsx")
# project_tuple = ['ss', 'vv', 'sxx', '', 22.3]
# for i in project_tuple:
#     # book.add_worksheet("Sheet1")  # 写入哪个Sheet
#     book.add_worksheet(i)
# book.close()



# startTime = "2020-01-09"
# # aa = datetime.strftime(startTime, "%Y/%m/%d").time()
# aa = datetime.strptime(startTime, '%Y-%m-%d').date().strftime("%Y/%#m/%#d")
# print(aa)
# print(type(aa))
# print(datetime.datetime.strftime(startTime, "%Y-%m-%d")
# print(datetime.strftime(startTime, "%Y-%m-%d"))

# import datetime
# timeStamp = 1381419600
# # timeStamp = 43959.0
#
# dateArray = datetime.utcfromtimestamp(timeStamp)
# otherStyleTime = dateArray.strftime("%Y-%m-%d")
# # otherStyletime == "2013-10-10 23:40:00"
# print(otherStyleTime)

# a = xlrd.xldate.xldate_as_datetime(43959.0, 0).strftime("%Y-%m-%d")
# print(a)

# bug_submit_date = 43959.0
# bug_submit_date = datetime.strptime(bug_submit_date, '%Y/%m/%d')
# bug_submit_date.strptime('%Y/%m/%d')

# timeStamp = 43959.0
# # timeStamp = 12345.0
# dateArray = datetime.utcfromtimestamp(timeStamp)
# otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
# # otherStyleTime = dateArray.strftime("%Y-%m-%d")
# # otherStyletime == "2013-10-10 23:40:00"
# print(otherStyleTime)
# print(type(otherStyleTime))
"""
b = datetime.now().strftime('%Y-%m-%d')
print(b)
b = "2020/1/9"
d = datetime.strptime(b, '%Y/%m/%d')
print(d)

e = datetime.date(d)
print(e)
print(f'e的类型{type(e)}')
f = str(e)
print(f)
print(f'ss的类型{type(f)}')

"""
