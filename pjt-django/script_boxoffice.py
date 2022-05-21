# kobis API
from datetime import datetime


KOBIS_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/soap/boxoffice'
KOBIS_API = '98217f55c5f31d1fc019c4a3c2ebe0a6'

kobis_params = {
    'key': KOBIS_API, 
    'targetDt': '',
    'weekGb': 0,
    'itemPerPage': 3,
    'repNationCd': 'K', 
}

from datetime import datetime, timedelta 
# 시작일,종료일 설정 
start = "2021-08-01" 
last = "2021-08-04" 

# 시작일, 종료일 datetime 으로 변환 
start_date = datetime.strptime(start, "%Y-%m-%d") 
last_date = datetime.strptime(last, "%Y-%m-%d") 

# 종료일 까지 반복 
while start_date <= last_date: 
  dates = start_date.strftime("%Y-%m-%d") 
  print(dates) 
# 하루 더하기 
  start_date += timedelta(days=1)
