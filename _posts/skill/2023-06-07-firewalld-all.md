---
layout: post
title: Linux 防火墙使用
category: 技术
tags: Linux
keywords: Linux,防火墙,端口
description: 
---

> 各种服务器开端口已经调试，查看端口开放情况



#### 查看自己外网ip

1. http请求方式

   >  curl cip.cc

2. ifconfig

   > 





#### 端口管理软件



https://blog.csdn.net/qq_35507234/article/details/126422619



iptables 



ufw



firewalld 



1、开启防火墙 
    systemctl start firewalld

2、开放指定端口
      firewall-cmd --zone=public --add-port=1935/tcp --permanent
 命令含义：
--zone #作用域
--add-port=1935/tcp  #添加端口，格式为：端口/通讯协议
--permanent  #永久生效，没有此参数重启后失效

3、重启防火墙
      firewall-cmd --reload

4、查看端口号
netstat -ntlp   //查看当前所有tcp端口·

netstat -ntulp |grep 8080   //查看所有8080端口使用情况



#### 验证端口

telnet ip地址 端口号
