---
layout: post
title: 计算系统用户增长率和留存率
category: 技术
tags:  概率 增长率 留存率 mysql
keywords: mysql rate
description: 2018-01-10-redis-nginx.md
---


* content
{:toc}
mysql 系统统计计算



## 计算留存率,增长率
	计算留存率,增长率等以日为单位,每天定时计算,计算数据统计到表


### 思路

1. 前提：t_client(用户表), 表中有, create_time,first_active_time,last_active_time,字段,保证last_active_time是正确的(定时每日计算昨天最后活跃时间)
2. 公式: 用户增长率 = (今天总活跃数/昨天活跃总数)*100%,昨日留存率= (今天总活跃数/昨天活跃总数) *100%,每天留存率=.....(这个有点小逻辑,自己看sql)
3. .... (以代码为准)

### 新建存储每天统计表

``` sql 
	-- 统计留存率  
	-- DROP TABLE  IF EXISTS t_retention_rate	;  
	CREATE TABLE t_retention_rate(  
	  id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,  
		client_count  BIGINT(20) NOT NULL,					-- 客户端总数
		active_count BIGINT(20) NOT NULL,					-- 客户端活跃总数
		register_nums BIGINT(20) NOT NULL,					-- 客户端当天注册总数
		active_nums BIGINT(20) NOT NULL,					-- 客户端当天活跃总数
		register_rage  decimal(18,5) DEFAULT NULL,			-- 客户端当天注册增长率
      														-- (今天总活跃数/昨天活跃总数)*100%
		active_rage  decimal(18,5) DEFAULT NULL,			-- 客户端当天活跃增长率
      														-- (今天总活跃数/昨天活跃总数)*100%
		
	  stat_time timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',  	--计算时间
	  create_time timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',  -- 创建时间
	
	  
	  nums INT(11) NOT NULL,  								-- 客户端当天新活跃数 不包括昨天注册今天再活跃
	  days_ago_1 decimal(18,5) DEFAULT NULL,  				-- 一天前留存率
	  days_ago_2 decimal(18,5) DEFAULT NULL,  				-- 两天前留存率
	  days_ago_3 decimal(18,5) DEFAULT NULL,  				-- ........
	  days_ago_4 decimal(18,5) DEFAULT NULL,    
	  days_ago_5 decimal(18,5) DEFAULT NULL,  
	  days_ago_6 decimal(18,5) DEFAULT NULL,  
	  days_ago_7 decimal(18,5) DEFAULT NULL,  
	  days_ago_8 decimal(18,5) DEFAULT NULL,   
	  days_ago_9 decimal(18,5) DEFAULT NULL,  
	  days_ago_10 decimal(18,5) DEFAULT NULL,  
	  days_ago_11 decimal(18,5) DEFAULT NULL,  
	  days_ago_12 decimal(18,5) DEFAULT NULL,   
	  days_ago_13 decimal(18,5) DEFAULT NULL, 
	  days_ago_14 decimal(18,5) DEFAULT NULL,   
	 
	  PRIMARY KEY (id)  ,UNIQUE (stat_time)
	)ENGINE=MYISAM DEFAULT CHARSET=utf8;  
```

### 每天进行计算

``` sql

DROP PROCEDURE  IF EXISTS  proc_retention_rate_by_day;

CREATE PROCEDURE proc_retention_rate_by_day(in today varchar(20))
BEGIN
-- 今天的日期
-- declare today date default curdate();
declare yesterday date default date_sub(today, interval 1 day);
declare anteayerDay date default date_sub(today, interval 2 day);


-- 今天计算昨天几个基础数据
DECLARE clientCount BIGINT DEFAULT (SELECT IFNULL(count(1),0) from t_client where create_time < today );-- 不见得是凌晨执行,所以要把今天的数据过滤掉
DECLARE activeCount BIGINT DEFAULT (SELECT IFNULL(count(1),0) from t_client where create_time < today and first_active_time is not null );
DECLARE registerNums BIGINT DEFAULT (SELECT IFNULL(count(1),0) from t_client where create_time < today and create_time between yesterday and today);
DECLARE activeNums BIGINT DEFAULT (SELECT IFNULL(count(1),0) from t_client where create_time < today and last_active_time between yesterday and today );
DECLARE nums_ BIGINT DEFAULT (SELECT IFNULL(count(1),0) from t_client  where create_time < today and first_active_time between yesterday and today );


-- 当天注册增长率,前一天总留存率,如果前一天没有数据默认是1，再计算,不然是0的话被除数为0查不出数据影响查询
DECLARE anteayerDayClientCount BIGINT DEFAULT (SELECT IFNULL(sum(client_count),1) from t_retention_rate where stat_time = anteayerDay );
DECLARE registerRage decimal(18,5) DEFAULT (registerNums/anteayerDayClientCount);

DECLARE anteayerDayActiveCount BIGINT DEFAULT (SELECT IFNULL(sum(client_count),1) from t_retention_rate where stat_time = anteayerDay );
--  DECLARE activeRage Double(5,5) DEFAULT (cast((activeNums/anteayerDayActiveCount) as decimal(18,5)));
DECLARE activeRage decimal(18,5) DEFAULT  (activeNums/anteayerDayActiveCount) ;


-- SELECT anteayerDayClientCount,anteayerDayActiveCount, registerNums,activeNums,registerRage,activeRage,nums_;

-- 统计昨天DRU(就是昨天一天的注册人数)
insert into t_retention_rate(client_count,active_count,register_nums,active_nums,register_rage,active_rage, nums, stat_time, create_time)
			select clientCount,activeCount,registerNums,activeNums,registerRage,activeRage, nums_ , yesterday, now() ;
 
-- 修改之前的留存,所有数据向后面一个字段变一天, A,B,C --->   C=B;B=A;A=新计算
update t_retention_rate set days_ago_14 =  days_ago_13;
update t_retention_rate set days_ago_13 =  days_ago_12; 
update t_retention_rate set days_ago_12 =  days_ago_11;
update t_retention_rate set days_ago_11 =  days_ago_10;
update t_retention_rate set days_ago_10 =  days_ago_9;
update t_retention_rate set days_ago_9 =  days_ago_8;
update t_retention_rate set days_ago_8 =  days_ago_7;
update t_retention_rate set days_ago_7 =  days_ago_6;
update t_retention_rate set days_ago_6 =  days_ago_5;
update t_retention_rate set days_ago_5 =  days_ago_4;
update t_retention_rate set days_ago_4 =  days_ago_3;
update t_retention_rate set days_ago_3 =  days_ago_2;
update t_retention_rate set days_ago_2 =  days_ago_1; 

-- 修改前天(anteayerDay)的留存  公式: 前天留存率= 前天活跃/大前天总注册
-- 下面的修改语句能够支持到很多天前的数据昨日概率,
update t_retention_rate set days_ago_1 = (
	select(
		IFNULL(
			cast(
				(select count(0) from t_client where (last_active_time between yesterday and today) and  (first_active_time between stat_time and date_sub(stat_time, interval -1 day) )) -- 找到昨天计算要注册的那一天
				/ 
				(SELECT t.nums from  (select IFNULL(sum(nums) ,0) as nums from t_retention_rate where stat_time =  date_sub(stat_time, interval 1 day)  LIMIT 1) as t ) # 修改的这一条数据的前一天新活跃的量
			 as decimal(18,2))  
			,0)
	)
) where stat_time = anteayerDay; 

END
-- CALL proc_retention_rate_by_day('2018-03-19');
```



​	