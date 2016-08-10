---
layout: post
title: tomcat数据库连接
category: 技术
tags: Essay
keywords:  tomcat、jdbc
description: 
---

#很久没有写博客了,没有心情写,也懒得写,今天加班没事做忽然想把自己想写的记一下

##有的时候看到这个代码不知道 其实是tomcat连接,次连接直接连接tomcat 下的   conf目录下context.xml 文件中的配置

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


#tomcat更改端口号 

-------
##找到 tomcat 下的server.xml文件 (更改3个端口)
	1.<Server port="8005" shutdown="SHUTDOWN">	//8005
		
	2.<Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" /> 			//8080
               
    3. <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" /> //8009 
   
   
#tomcat启动问题
>有的时候需要给其配置jdk路径可以直接在tomcat下的 	startup.bat里面写

-------
编辑 startup.bat
写在第一行：eg
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_25 
set CATALINA_HOME=D:\Program Files\apache-tomcat-7.0.40-band-test
    


