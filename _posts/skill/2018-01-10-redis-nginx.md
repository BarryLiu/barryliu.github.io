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
	