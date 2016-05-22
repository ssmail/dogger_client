import psutil
from time import sleep
import socket
import platform
import MySQLdb
import time

memoryInfo = psutil.virtual_memory().total/1024/1024
available = psutil.virtual_memory().available/1024/1024
percent = psutil.virtual_memory().percent
used = psutil.virtual_memory().used/1024/1024
free = psutil.virtual_memory().free/1024/1024

def save2DB(machineName, osVersion, cpuUsage, memoryUsage, diskUsage, networkUsage):
	db = MySQLdb.connect(user="root", passwd="xxxx", db="dogger", host="192.168.0.107",port=3308)
	db.autocommit(True)
	cur = db.cursor()
	sql = 'insert into machine_info (machine_name,os_version, cpu_usage, memory_usage, disk_usage, network_usage, ioread, iowrite, disk_free, memory_free, memory_used, network_recv, network_sent, version, create_date) value ("{machineName}", "{osVersion}", "{cpuUsage}", "{memoryUsage}", "{diskUsage}", "{networkUsage}",0,0,0,0,0,0,0,0, "{create_date}")'.format(machineName = machineName, osVersion = osVersion, cpuUsage = cpuUsage, memoryUsage = memoryUsage, diskUsage = diskUsage, networkUsage = networkUsage, create_date = ctime())
	print sql
	
	cur.execute(sql)

def save2Temp(machineName, osVersion, cpuUsage, memoryUsage, diskUsage, networkUsage):
	db = MySQLdb.connect(user="root", passwd="hongkf", db="dogger", host="localhost",port=3308)
	db.autocommit(True)
	cur = db.cursor()
	sql = 'update current_info set cpu_usage = {cpuUsage}, memory_usage = {memoryUsage}, network_usage = {networkUsage}, disk_usage={diskUsage}, create_date="{create_date}" where machine_name="{machineName}"'.format(machineName = machineName, osVersion = osVersion, cpuUsage = cpuUsage, memoryUsage = memoryUsage, diskUsage = diskUsage, networkUsage = networkUsage, create_date = ctime())
	
	print sql

	cur.execute(sql)

def ctime():
	return time.strftime(u'%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))

def ttime():
	return time.time()

def getNetworkUsage():
	neti1 = psutil.net_io_counters()[1]
	neto1 = psutil.net_io_counters()[0]
	sleep(1)
	neti2 = psutil.net_io_counters()[1]
	neto2 = psutil.net_io_counters()[0]
	# Calculate the bytes per second
	net = ((neti2+neto2) - (neti1+neto1))/2

	return net

getNetworkUsage()

print "{CPU:10} {Memory:12} {Disk:10} {Network:10}".format(CPU="CPU", Memory="Memory", \
														Disk="Disk", Network = "Network")

machineName = socket.gethostname()
osType = platform.system()

while 1:
	cpuUsage = psutil.cpu_percent(interval = 1)
	MemoryUsagepercent = psutil.virtual_memory().percent
	diskUsage = psutil.disk_usage('/').used/1024/1024
	networkUsage = getNetworkUsage()
	print "{CPU}	   {Memory}%	{Disk}MB		{Network}".format(CPU=cpuUsage, Memory=MemoryUsagepercent, Disk=diskUsage, Network=networkUsage)
	save2Temp(machineName, osType, cpuUsage, MemoryUsagepercent, diskUsage, networkUsage)
	save2DB(machineName, osType, cpuUsage, MemoryUsagepercent, diskUsage, networkUsage)
	sleep(2)


