#数据库查询结果，用json返回
import json
import pymysql

conn = pymysql.Connect(host='localhost', user='root', passwd='123456', db='bugcount', port=3306, charset='utf8')
cur = conn.cursor()
cur.execute("select * from bugcount.user")
print('共有', cur.rowcount, '条数据')

data = {}
users = []
results = cur.fetchall()
print('????????result=', results)
print('????????????????????type = ', type(results))
for r in results:
    print(r[0], end=' ')
    print(r[1], end=' ')
    print(r[2], end=' ')
    print("---")
    person = {}
    person['a'] = r[0]
    person['b'] = r[1]
    person['c'] = r[2]
    users.append(person)
    print('????users==', type(users))

cur.close()
conn.close()
data['code'] = 0
data['msg'] = '成功'
data['users'] = users
print('??????????????????????users[]=', users)
print('??????????????????????users type[]=', type(users))

jsonStr = json.dumps(data)
print(jsonStr)
