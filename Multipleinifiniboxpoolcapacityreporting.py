import json
import requests
import pymysql
import datetime
import re

#######################################################################################################################################
##This script connects to the infinidat infinibox storage using readonly credentials and makes api get calls for the pool information##
##which is then stored in a mysql database(in this case the mysqldb is hosted on the same server as the script runs). You will notice##
##3 URLs, one for each storage array. If you have a new storage array all you need to do is create another variable lets say of this ##
##script it will be urld, since urlc is the previous one. Then you can add the api link for the pools into it as a string. Do not    ## 
##forget to add the urld into the list urllist variable mentioned in line 22(in this script).                                        ##
##This script automatically pulls the storage array name from your url and adds into the database column. This script also collects  ##
##the current date as of when you run the script and also enters into the database.                                                  ##
##You are free to copy this script and modify it or enhance it.Please share your enhancements so it can help others and myself learn ##
#######################################################################################################################################

urla = 'http://<ibox1ipaddress or hostname>/api/rest/pools'
urlb = 'http://<ibox2ipaddress or hostname>/api/rest/pools'
urlc = 'http://<ibox3ipaddress or hostname>/api/rest/pools'

urllist = [urla, urlb, urlc]
auth = ('<username>', '<password>')

for url in urllist:
	resp = requests.get(url=url, auth=auth).json()

	for item in resp['result']:
		poolname = item['name']
		Totalcapacity = item['physical_capacity']
		Totalusedcapacity = item['allocated_physical_space']
		Totalfreecapacity = item['free_physical_space']
		Totalvirtualcapacity = item['virtual_capacity']
		Totalfreevirtualcapacity = item['free_virtual_space']

	
		pattern = re.compile(r'\.*[a-z]*\d\d')
		matches = pattern.finditer(url)
		for match in matches:
			ArrayName = match.group(0)

	today = datetime.date.today()
	datestr = str(today.year)+"/"+str(today.month)+"/"+str(today.day)


	connection = pymysql.connect(host='localhost', user='root', password='', db='Storage')

	for item in resp['result']:
		data = (item['name'], item['physical_capacity'], item['allocated_physical_space'], item['free_physical_space'], item['free_virtual_space'], datestr, ArrayName)
		#print(data)
		cursor = connection.cursor()
		sql = 'INSERT INTO STORAGE.storageibox (`Poolname`, `Totalcapacity`, `Totalusedcapacity`, `Totalfreecapacity`, `Totalvirtualcapacity`, `Date`, `ArrayName`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
		#print(sql)
		cursor.execute(sql, data)
		connection.commit()

		
	connection.close()
