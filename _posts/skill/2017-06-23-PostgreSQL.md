---
layout: post
title: 数据库基本语句
category: SQL
tags:  PostgreSql
keywords: sql
description: postgreSql 
---

#PostgreSql 常用命令
	命令都是以"\"开头  \help

#查询登录  
	psql -h 192.168.0.1 -U username -d dbname 
	mysql -h 192.168.0.1 -uusername -ppassword

#基本命令（第一行postSql 后面跟着  mysql ）
##查询所有数据库	
	\l	或者	\list
	show databases

##数据库切换到 database
	\c  database
	use database

##列出当前数据库下的数据表
	\d
	show tables

##列出指定表的所有字段
	\d tablename
	show columns from tablename
##查看指定表的基本情况
	describe tablename
	\d+ tablename

##退出登录
	\q
	quit 或者\q