from datetime import datetime

def is_legal_date(strdate):
    try:
        datetime.strptime(strdate, "%Y/%m/%d")
        return True
    except:
        return False

a = '2019.10.15'
a = a.strip()
# a = '2019/3/15'
print(is_legal_date(a))