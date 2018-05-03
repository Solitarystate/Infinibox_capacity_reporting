import json
import requests
import pymysql
import datetime


url = 'http://<infinidatstorageipaddress or hostname>/api/rest/pools'
auth = ('adminaccount', 'password.')

resp = requests.get(url=url, auth=auth).json()



for item in resp['result']:
	poolname = item['name']
	Totalcapacity = item['physical_capacity']
	Totalusedcapacity = item['allocated_physical_space']
	Totalfreecapacity = item['free_physical_space']
	Totalvirtualcapacity = item['virtual_capacity']
	Totalfreevirtualcapacity = item['free_virtual_space']

today = datetime.date.today()
datestr = str(today.year)+"/"+str(today.month)+"/"+str(today.day)


connection = pymysql.connect(host='localhost', user='root', password='', db='Storage')

for item in resp['result']:
	data = (item['name'], item['physical_capacity'], item['allocated_physical_space'], item['free_physical_space'], item['free_virtual_space'], datestr)
	print(data)
	cursor = connection.cursor()
	sql = 'INSERT INTO STORAGE.storageibox (`Poolname`, `Totalcapacity`, `Totalusedcapacity`, `Totalfreecapacity`, `Totalvirtualcapacity`, `Date`) VALUES (%s, %s, %s, %s, %s, %s)'
	print(sql)
	cursor.execute(sql, data)
	connection.commit()

	
connection.close()
