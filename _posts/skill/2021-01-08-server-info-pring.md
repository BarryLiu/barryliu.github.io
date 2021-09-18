---
layout: post
title: 简单python笔记
category: 技术
tags:  linux python psutil
keywords: psutil python
description: 简单python psutil工具了解 

---



### 控制台实时打印服务器状态

> server_running_info_app.py 监控这台服务器
>
> server_running8080_info_app.py  监控8080端口

#### 效果

server_running_info_app.py 

![psutil_print1](/images\skill\psutil_print1.png)



server_running8080_info_app.py 

![psutil_print2](/images\skill\psutil_print2.png)

#### 代码  



* # server_running_info_app.py

``` python
#!/usr/bin/env python
#conding:UTF-8

import time
import os
import commands
import psutil

def getTime():
	time_local=time.strftime('%X')
	return str(time_local)

def getCpu():
	cpu_use=str(psutil.cpu_percent(1))
	return cpu_use

def getMem():
	mem_use_result=str(psutil.virtual_memory().percent)
	return mem_use_result

def getNet():
	#network_t1=psutil.net_io_counters(pernic=True).items()[1][1][0]		#eth1
	#network_r1=psutil.net_io_counters(pernic=True).items()[1][1][1]		#eth1
	network_t1=psutil.net_io_counters(pernic=True).items()[1][1][0]	#eth0
	network_r1=psutil.net_io_counters(pernic=True).items()[1][1][1]	#eth0
	time.sleep(0.5)
	#network_t2=psutil.net_io_counters(pernic=True).items()[1][1][0]		#eth1
        #network_r2=psutil.net_io_counters(pernic=True).items()[1][1][1]		#eth1
	network_t2=psutil.net_io_counters(pernic=True).items()[1][1][0]	#eth0
        network_r2=psutil.net_io_counters(pernic=True).items()[1][1][1]	#eth0
	network_t=round((float(network_t2)-float(network_t1))/1024*2,2)
	network_r=round((float(network_r2)-float(network_r1))/1024*2,2)
	return(network_r,network_t)
	
def getTcpNum():
	(status,tcp_ESTABLISHED)=commands.getstatusoutput("netstat -anp|grep '172.17.27.207'|grep 'ESTABLISHED'|grep 'java'|grep -v grep|wc -l")
	(status,tcp_TIME_WAIT)=commands.getstatusoutput("netstat -anp|grep '172.17.27.207'|grep 'TIME_WAIT'|grep 'java'|grep -v grep|wc -l")
	return(tcp_ESTABLISHED,tcp_TIME_WAIT)

def main():
	#print("Time"+"\t"+"Cpu"+"\t"+"Memory"+"\t"+"Net_in(KB/s)\t"+"Net_out(KB/s)\t"+"Tcp(es)\t"+"Tcp(wait)")
	print("%8s\t%8s\t%8s\t%8s\t%8s\t%8s\t%8s" %("Time","Cpu(%)","Memory(%)","Net_in(Kb/s)","Net_out(Kb/s)","Tcp(es)","Tcp(wait)"))
	while 1:
		#print(str(getTime()).center(8," ") getCpu().center(8," "))
		print("%8s\t%8s\t%8s\t%8s\t%8s\t%8s\t%8s" %(getTime(),getCpu(),getMem(),getNet()[0],getNet()[1],getTcpNum()[0],getTcpNum()[1]))
	

if __name__=='__main__':
	main()



```



* #server_running8080_info_app.py 

``` python
#!/usr/bin/env python
#conding:UTF-8

import time
import os
import commands
import psutil

def getTime():
	time_local=time.strftime('%X')
	return str(time_local)

def getCpu():
	cpu_use=str(psutil.cpu_percent(1))
	return cpu_use

def getMem():
	mem_use_result=str(psutil.virtual_memory().percent)
	return mem_use_result

def getNet():
	#network_t1=psutil.net_io_counters(pernic=True).items()[1][1][0]		#eth1
	#network_r1=psutil.net_io_counters(pernic=True).items()[1][1][1]		#eth1
	network_t1=psutil.net_io_counters(pernic=True).items()[1][1][0]	#eth0
	network_r1=psutil.net_io_counters(pernic=True).items()[1][1][1]	#eth0
	time.sleep(0.5)
	#network_t2=psutil.net_io_counters(pernic=True).items()[1][1][0]		#eth1
        #network_r2=psutil.net_io_counters(pernic=True).items()[1][1][1]		#eth1
	network_t2=psutil.net_io_counters(pernic=True).items()[1][1][0]	#eth0
        network_r2=psutil.net_io_counters(pernic=True).items()[1][1][1]	#eth0
	network_t=round((float(network_t2)-float(network_t1))/1024*2,2)
	network_r=round((float(network_r2)-float(network_r1))/1024*2,2)
	return(network_r,network_t)
	
def getTcpNum():
	(status,tcp_ESTABLISHED)=commands.getstatusoutput("netstat -anp|grep '172.17.27.207:8080'|grep 'ESTABLISHED'|grep -v grep|wc -l")
	(status,tcp_TIME_WAIT)=commands.getstatusoutput("netstat -anp|grep '172.17.27.207:8080'|grep 'TIME_WAIT'|grep -v grep|wc -l")
	return(tcp_ESTABLISHED,tcp_TIME_WAIT)

def main():
	#print("Time"+"\t"+"Cpu"+"\t"+"Memory"+"\t"+"Net_in(KB/s)\t"+"Net_out(KB/s)\t"+"Tcp(es)\t"+"Tcp(wait)")
	print("%8s\t%8s\t%8s\t%8s\t%8s\t%8s\t%8s" %("Time","Cpu(%)","Memory(%)","Net_in(Kb/s)","Net_out(Kb/s)","Tcp(es)","Tcp(wait)"))
	while 1:
		#print(str(getTime()).center(8," ") getCpu().center(8," "))
		print("%8s\t%8s\t%8s\t%8s\t%8s\t%8s\t%8s" %(getTime(),getCpu(),getMem(),getNet()[0],getNet()[1],getTcpNum()[0],getTcpNum()[1]))
	

if __name__=='__main__':
	main()

```

