---
layout: post
title:  记录按键灯效
date:   2020-11-16 14:06:05
categories: C/C++ 
tags: 蓝牙耳机 络达 1562 AB156X 开发板 psensor 入耳检测 按键灯效gi
---



### 服务器运行app





### 所有务器运行app汇总



![img](http://192.168.1.12:8090/download/attachments/9405193/image2018-3-12_16-58-20.png?version=1&modificationDate=1520845101000&api=v2)





![img](http://192.168.1.12:8090/download/attachments/9405196/image2018-3-12_16-59-30.png?version=1&modificationDate=1520845171000&api=v2)

>  上面 MP_002里面没有zookeeper了，MP004里面有





#### 查看服务器状态

python /usr/local/monitor/server_running_info_app.py





#### ECS_MP_004 - 5%J-Xq*f

60.205.182.242(公)    32G

135817

 

* /usr/local/tomcat_zookeeper_8011/
* /usr/local/tomcat_zeus_api_8081  zeus_api     -server -Xms2048m -Xmx2048m

* /usr/local/tomcat_zeus_mq_8084/  zeus_mq    -server -Xms2048m -Xmx2048m
* /usr/local/tomcat_homework_8080  HomeworkManagement  -server -Xms6000m -Xmx6000m
* /usr/local/tomcat_zeus_console_8082 console  		  		-server -Xms2048m -Xmx2048m
* /usr/local/tomcat_hwexam_8605   hw-exam    默认内存
* /usr/sbin/rabbitmq-server   

*  有装过 zabbix-agentd 软件， 不知道有没有使用





#### ECS_MP_003 - qwM0v![U

60.205.181.239(公) 	32G

111111

* /usr/local/tomcat_zeus_api_8081   zeus_api     		 				-server -Xms2048m -Xmx2048m

* /usr/local/tomcat_bom_9090/   BomManagement.war     WKFlow-web

* /usr/local/tomcat_hwexam_8605   hw-exam    默认内存

* /usr/local/tomcat_homework_8080   HomeworkManagement   -server -Xms6000m -Xmx6000m

* /usr/local/tomcat_zeus_console_8082 console  		  		-server -Xms2048m -Xmx2048m

  

* /usr/local/stem-boot/   stem-api-8097   stem-classroom-8098  stem-pay-8096  stem-web-8099    -server -Xms1024m -Xmx6072m

* ares_versioning.jar   好像是王怀写的后台上传安装包工具      -server -Xms2048m -Xmx6072m

* /usr/local/nacos-server-0.9.0  不知道哪个程序使用

*  redis-server 
*  有装过 zabbix-agentd 软件， 不知道有没有使用



#### ECS_MP_002 - 8)Lzn)@u

47.93.33.49(公) 	16G 

828877

>  作业本相关只有dubbokepper ,可以移到 MP_003或者_MP004  ， 7个应用程序

* /usr/local/tomcat_2070/webapps/	Headset-web.war  Visitor-web.war    

* /usr/local/tomcat-8081   dubbokeeper.war
* /usr/local/tomcat_2090/webapps/     Rfid-app.war Rfid-web.war

* java -server -Xms1024m -Xmx6072m -jar lockserver-provider-0.0.1-SNAPSHOT.jar -Dserver.port=8982
* java -server -Xms1024m -Xmx6072m -jar lockserver-mobile-0.0.1-SNAPSHOT.jar -Dserver.port=8980

*  有装过 zabbix-agentd 软件， 不知道有没有使用



#### ECS_MP_001 - XGQ(MxT*

60.205.227.24(公) 

269745

> 内存使用不多，

 







#### ECS_PRE_001  

59.110.163.188(公)   2C 8G	

>   zeus-console 可以关， 	



* /usr/local/tomcat-kmsPlantWeb-1050/ 	AdPlant-app.war   FlangeManage-web.war

* /usr/local/tomcat-adPlantWeb-4050/webapps/   AdPlant-web.war   AdPlant-app.war

* /usr/local/tomcat-kmsPlantApp-1060/   FlangeManage-app.war

* /usr/local/tomcat_zeus_console_8082    zeus-console   (可以关掉)

  







### ECS_CSOS_001

 39.106.205.209 (公) 2C 4G

> 只有一个Nginx ， 不需要考虑内存和核心， 带宽够用就行 



* nginx  









|        | ECS_MP_001               | ECS_MP_002                                                   | ECS_MP_003                                                   | ECS_MP_004                                                   | ECS_PRE_001                                                  |
| ------ | ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 配置   | 60.205.227.24(公)  2C 8G | 47.93.33.49(公) 	16G                                      | 60.205.181.239(公)  8C	32G                                | 60.205.182.242(公)    8C 32G                                 | 59.110.163.188(公)   2C 8G                                   |
| 程序   |                          | Headset-web.war 、 Visitor-web.war，dubbokeeper、Rfid-app.war Rfid-web.war、lockserver-provider-0.0.1-SNAPSHOT.jar，lockserver-mobile-0.0.1-SNAPSHOT.jar | zeus_api， BomManagement ，WKFlow-web、hw-exam 、HomeworkManagement、console、[stem-api-8097 ,  stem-classroom-8098 , stem-pay-8096  ,stem-web-8099]  、ares_versioning、redis-server 、nacos-server-0.9.0 | zookeeper、rabbitmq-server、zeus_api、zeus_mq、HomeworkManagement、console 、rabbitmq-server 、hw-exam 、 | AdPlant-app.war  ， FlangeManage-web.war，FlangeManage-app.war，zeus-console |
| 程序名 |                          | 蓝牙耳机后台， 访客系统后台，资产管理系统后台，库岩岩做过的锁后台， | stem里面的一套程序， bom程序后台，其它的和 MP_004负载均衡的程序 |                                                              | 广告机后台，法兰后台，                                       |
| 能否   |                          | 资产管理系统后台停掉，库岩岩做过的锁停掉                     | 公网的bom停掉，  stem能否停掉 ，或者说把003和004 负载均衡去掉， | hw-exam 停掉 。  HomeworkManagement 、zeus_api、 zeus_mq  内存减半 | zeus-console可以停掉                                         |









# 20240109 启动次序

1. 先启动zookeeper

33.49上



2. 启动应用

60.205.181.239

/usr/local/tomcat_homework_8080/bin/startup.sh

如果启动不了报目录错误,mkdir /data/upQuestions/temp



/usr/local/tomcat_zeus_api_8081/bin/startup.sh

/usr/local/tomcat_zeus_console_8082/bin/startup.sh

