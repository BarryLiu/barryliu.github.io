---
layout: post
title: tomcat数据库连接
category: 技术
tags: tomcat
keywords:  tomcat、jdbc
description: 
---


Tomcat 是一个小型的轻量级应用服务器，在中小型系统和并发访问用户不是很多的场合下被普遍使用，是开发和调试JSP 程序的首选。对于一个初学者来说，可以这样认为，当在一台机器上配置好Apache 服务器，可利用它响应对HTML 页面的访问请求。实际上Tomcat 部分是Apache 服务器的扩展，但它是独立运行的，所以当你运行tomcat 时，它实际上作为一个与Apache 独立的进程单独运行的。







## 有的时候看到这个代码不知道 其实是tomcat连接,次连接直接连接tomcat 下的   conf目录下context.xml 文件中的配置

```java
 Connection dbConn = null;
		 if(LOCAL_CALL) {
			 dbConn = getConnectionForLocalCall();
		 } else {
			 try {
				 Context initCtx = new InitialContext();
				 if (initCtx == null)
					 throw new Exception("不能获取Context!");
				 Context ctx = (Context) initCtx.lookup("java:comp/env");
				 Object obj = (Object) ctx.lookup("jdbc/sqlserver");//获取连接池对象
				 DataSource ds = (javax.sql.DataSource) obj; //类型转换
				 dbConn = ds.getConnection();
				 // System.out.println("连接池连接成功!");
			 } catch (Exception e) {
				 e.printStackTrace();
			 }
		 }
		 return dbConn;
```

## tomcat 下conf/context.xml 配置下
```xml 
<Resource name="jdbc/sqlserver" 
	auth="Container" 
	type="javax.sql.DataSource" 
	driverClassName="com.microsoft.sqlserver.jdbc.SQLServerDriver" 
	url="jdbc:sqlserver://localhost:1433;DatabaseName=OTA" 
	username="sa" 
	password="Wheatek!"
	maxActive="1000" 
	maxIdle="30" 
	maxWait="500"
	removeAbandoned="true" removeAbandonedTimeout="60" 
	logAbandoned="true"/>
```


# 普通jdbc 连接

```JAVA
  哈哈哈 百度去

```


# tomcat更改端口号 

-------
## 找到 tomcat 下的server.xml文件 (更改3个端口)
	1.<Server port="8005" shutdown="SHUTDOWN">	//8005

	2.<Connector port="8080" protocol="HTTP/1.1"
	           connectionTimeout="20000"
	           redirectPort="8443" /> 			//8080
	           
	3. <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" /> //8009 


# tomcat启动问题
> 有的时候需要给其配置jdk路径可以直接在tomcat下的 	startup.bat里面写

-------
编辑 startup.bat
写在第一行：eg
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_25 
set CATALINA_HOME=D:\Program Files\apache-tomcat-7.0.40-band-test
​    


# 进入tomcat端口直接进入项目   
> tomcat 配置  server.xml下面找到   最下面找到配置给其配contextpath

----------
	<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"  
	           prefix="localhost_access_log." suffix=".txt" pattern="common" rotatable="true" resolveHosts="false"/>
		 
		 <Context path="" docBase="E:\program\apache-tomcat-7.0.62-project-8082\webapps\project_manager" debug="0" reloadable="true"/>	
		<!-- <Context path="/pagt" docBase="D:\Program Files\apache-tomcat-7.0.62_push\webapps\pagt" debug="0" reloadable="true"/> -->

# TOMCAT 部署项目 页面刷新 有时正常显示 有时候报404 
	问题解决办法 ,tomcat目录work 文件夹下 将对应的项目对应的文件夹删除掉

# tomcat部署项目如何去掉项目名称

###直接在server.xml中<Host></Host>间加了一句<Context path="" docBase="/fts" debug="0" reloadable="true"/>,其中docBase="/test"中的/test是项目名字



# 把项目放到tomcat6\webapps下面

修改Host

<Host name="www.test.com"  debug="0" appBase="webapps" unpackWARs="true" autoDeploy="true" xmlValidation="false" xmlNamespaceAware="false"> 

<Context path="/" docBase="/test"  debug="0" reloadable="true"></Context> 

</Host> 

这样就可以通过域名www.test.com访问test为项目名的项目了。

如果主机中绑定多个域名，直接加host即可。


jvisualvm

http://jiajun.iteye.com/blog/810150


# tomcat session失效设置
```

	session失效时间设置  
	一、java代码  
	request.getSession().setMaxInactiveInterval(1800);/*秒为单位*/    
	二、web.xml  
	<session-config>   <!--分钟为单位-->  
	    <session-timeout>30</session-timeout>  
	</session-config>  
	  
	三、web服务器resin.conf，tomcat，  
	<session-config>   <!--分钟为单位-->  
	    <session-timeout>30</session-timeout>  
	    <enable-url-rewriting>false</enable-url-rewriting>  
	</session-config>  
	
	
# Tomcat配置远程调试端口
>当我们需要定位生产环境问题，而日志又不清晰的情况下，我们可以借助Tomcat提供的远程调试
```
	// Linxu系统: apach/bin/startup.sh开始处中增加如下内容： 
	declare -x CATALINA_OPTS="-server -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8081"


	// Windows系统: apach/bin/startup.bat开始处中增加如下内容：
	SET CATALINA_OPTS=-server -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8081


#修改tomcat 内存

## 前台程序修改
	修改catalina.bat 文件,加入 JAVA_OPTS=-Xms256m -Xmx512m 


## 后台修改
	win+r >  regedit 找到 tomcat的注册表信息
	HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Apache Software Foundation\Procrun 2.0\TomcatName 修改里面的
	参考：http://blog.csdn.net/lfsf802/article/details/46700553


![注册表修改](http://owpmx0n2u.bkt.clouddn.com/regedit_tomcat.png)