import json

result = ((23, 'root', 'pass', '118@123.com', '118@123.com', None, None, None), (28, 'admin1', '1a1dc91c907325c69271ddf0c944bc72', None, None, None, None, None), (29, 'admin0', '62f04a011fbb80030bb0a13701c20b41', None, None, None, None, None))
print('长度', len(result))
dict_convert_jsonData = 'ssss'
for row in result:
    print('循环了1次')
    # 封装成这种格式{'key','value'},{'key','value'},
    dataDict = {}

    keys = ['userid', 'username', 'password', 'user_remark', 'user_email', 'user_level', 'create_time', 'session']
    values = [row[0], str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7])]
    print('values==', values)

    data_dict = dict(zip(keys, values))
    print(data_dict)
    print(type(data_dict))
    data_dict_str = str(data_dict) + ',12321'
    # dict_convert_jsonData
    print('ssssssssssssss', dict_convert_jsonData)
    print('拼接字符串', data_dict_str)



#去除原始数据最后一个逗号，
print('jsonOriginalData', dict_convert_jsonData)

#拼接字符串完后，再转成json
dict_convert_jsonData = json.dumps(data_dict)
# print('==========', c+d)