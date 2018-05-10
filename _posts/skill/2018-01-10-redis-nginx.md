---
layout: post
title: redis 以及nginx
category: 技术
tags:  redis nginx
keywords: redis nginx
description: redis缓存,nginx反向代理,动静分离
---


* content
{:toc}
redis缓存,nginx反向代理,动静分离



![startnginx](_posts/skill/startnginx.png)



## redis命令
	启动:	redis-server redis.conf
	关闭：redis-cli  shutdown 有密码先登录auth登录直接敲  shutdown
	登录(如有密码): auth 密码 
### 设置
	requirepass 设置密码
	db
	
	
## nginx 
	
### nginx -s reload  ：修改配置后重新加载生效
nginx -s reopen  ：重新打开日志文件
nginx -t -c /path/to/nginx.conf 测试nginx配置文件是否正确

### 关闭nginx：
nginx -s stop  :快速停止nginx
         quit  ：完整有序的停止nginx

### 其他的停止nginx 方式：

ps -ef | grep nginx

kill -QUIT 主进程号     ：从容停止Nginx
kill -TERM 主进程号     ：快速停止Nginx
pkill -9 nginx          ：强制停止Nginx



# 启动nginx:
nginx -c /path/to/nginx.conf

# 平滑重启nginx：
kill -HUP 主进程号