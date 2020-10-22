from py import utils
import json
tablehead = ['提交日期', '项目', '软件类', '测试版本', '描述',
                 '严重等级', '优先级', '难度', '关闭情况', '关闭日期',
                 '关闭版本', '原因分析', '问题图片', '中间情况', '开发者',
                 '备注', '回归次数', '重开次数', '提交者索引']
jsonstr = utils.checkexcel_data("./excel_upload/template.xlsx", tablehead)
jsonobj = json.loads(jsonstr)
print(type(jsonobj))
print(jsonobj['code'])