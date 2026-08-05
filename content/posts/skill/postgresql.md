---
title: "PostgreSQL 数据库使用指南"
date: 2017-06-23
postSlug: "skill/postgresql"
categories:
  - "技术"
tags:
  - PostgreSQL
  - "数据库"
  - SQL
description: "PostgreSQL 数据库安装、数据类型、常用命令、性能诊断和运维速查"
keywords: "postgresql, sql, 数据库, docker, 性能诊断, pg_stat_activity, pg_stat_statements"
featured: false
---

mysql 与 postgreSql 数据库简单使用,命令对比
## 安装与连接
### docker安装
``` 
docker run --name postgres -e POSTGRES_PASSWORD=xxxxxx -p 5433:5432 -v /home/zx/postgres/data:/var/lib/postgresql/data -d postgres
```
###  连接
 * docker进入连接
   1. 安装好后进入docker
      > docker exec -it postgres /bin/bash
   2. 进入镜像后登录psql,然后输入密码
      > psql -h localhost -U postgres -p 5432
   3. 如有需要修改密码
      > alter user postgres with password '123456';
* navicat 连接
  > 填写好账号密码，不详细介绍了
* pgadmin 连接
  > 免费且开源的web应用， 支持所有的postgreSQL功能，没有安装，不演示
  
## 数据类型与基本概念
> 
[参考菜鸟文档](https://www.runoob.com/postgresql/postgresql-data-type.html)
### 数值类型
数值类型由 2 字节、4 字节或 8 字节的整数以及 4 字节或 8 字节的浮点数和可选精度的十进制数组成。
下表列出了可用的数值类型。
| 名字             | 存储长度 | 描述                 | 范围                                         |
| :--------------- | :------- | :------------------- | :------------------------------------------- |
| smallint         | 2 字节   | 小范围整数           | -32768 到 +32767                             |
| integer          | 4 字节   | 常用的整数           | -2147483648 到 +2147483647                   |
| bigint           | 8 字节   | 大范围整数           | -9223372036854775808 到 +9223372036854775807 |
| decimal          | 可变长   | 用户指定的精度，精确 | 小数点前 131072 位；小数点后 16383 位        |
| numeric          | 可变长   | 用户指定的精度，精确 | 小数点前 131072 位；小数点后 16383 位        |
| real             | 4 字节   | 可变精度，不精确     | 6 位十进制数字精度                           |
| double precision | 8 字节   | 可变精度，不精确     | 15 位十进制数字精度                          |
| smallserial      | 2 字节   | 自增的小范围整数     | 1 到 32767                                   |
| serial           | 4 字节   | 自增整数             | 1 到 2147483647                              |
| bigserial        | 8 字节   | 自增的大范围整数     | 1 到 9223372036854775807                     |
------
### 货币类型
money 类型存储带有固定小数精度的货币金额。
numeric、int 和 bigint 类型的值可以转换为 money，不建议使用浮点数来处理处理货币类型，因为存在舍入错误的可能性。
| 名字  | 存储容量 | 描述     | 范围                                           |
| :---- | :------- | :------- | :--------------------------------------------- |
| money | 8 字节   | 货币金额 | -92233720368547758.08 到 +92233720368547758.07 |
------
### 字符类型
下表列出了 PostgreSQL 所支持的字符类型：
| 序号 | 名字 & 描述                                          |
| :--- | :--------------------------------------------------- |
| 1    | **character varying(n), varchar(n)**变长，有长度限制 |
| 2    | **character(n), char(n)**f定长,不足补空白            |
| 3    | **text**变长，无长度限制                             |
------
### 日期/时间类型
下表列出了 PostgreSQL 支持的日期和时间类型。
| 名字                                      | 存储空间 | 描述                     | 最低值        | 最高值        | 分辨率         |
| :---------------------------------------- | :------- | :----------------------- | :------------ | :------------ | :------------- |
| timestamp [ (*p*) ] [ without time zone ] | 8 字节   | 日期和时间(无时区)       | 4713 BC       | 294276 AD     | 1 毫秒 / 14 位 |
| timestamp [ (*p*) ] with time zone        | 8 字节   | 日期和时间，有时区       | 4713 BC       | 294276 AD     | 1 毫秒 / 14 位 |
| date                                      | 4 字节   | 只用于日期               | 4713 BC       | 5874897 AD    | 1 天           |
| time [ (*p*) ] [ without time zone ]      | 8 字节   | 只用于一日内时间         | 00:00:00      | 24:00:00      | 1 毫秒 / 14 位 |
| time [ (*p*) ] with time zone             | 12 字节  | 只用于一日内时间，带时区 | 00:00:00+1459 | 24:00:00-1459 | 1 毫秒 / 14 位 |
| interval [ *fields* ] [ (*p*) ]           | 12 字节  | 时间间隔                 | -178000000 年 | 178000000 年  | 1 毫秒 / 14 位 |
### 布尔类型
PostgreSQL 支持标准的 boolean 数据类型。
boolean 有"true"(真)或"false"(假)两个状态， 第三种"unknown"(未知)状态，用 NULL 表示。
| 名称    | 存储格式 | 描述       |
| :------ | :------- | :--------- |
| boolean | 1 字节   | true/false |
### 几何类型
几何数据类型表示二维的平面物体。
下表列出了 PostgreSQL 支持的几何类型。
最基本的类型：点。它是其它类型的基础。
| 名字    | 存储空间    | 说明                   | 表现形式               |
| :------ | :---------- | :--------------------- | :--------------------- |
| point   | 16 字节     | 平面中的点             | (x,y)                  |
| line    | 32 字节     | (无穷)直线(未完全实现) | ((x1,y1),(x2,y2))      |
| lseg    | 32 字节     | (有限)线段             | ((x1,y1),(x2,y2))      |
| box     | 32 字节     | 矩形                   | ((x1,y1),(x2,y2))      |
| path    | 16+16n 字节 | 闭合路径(与多边形类似) | ((x1,y1),...)          |
| path    | 16+16n 字节 | 开放路径               | [(x1,y1),...]          |
| polygon | 40+16n 字节 | 多边形(与闭合路径相似) | ((x1,y1),...)          |
| circle  | 24 字节     | 圆                     | <(x,y),r> (圆心和半径) |
### 网络地址类型
PostgreSQL 提供用于存储 IPv4 、IPv6 、MAC 地址的数据类型。
用这些数据类型存储网络地址比用纯文本类型好， 因为这些类型提供输入错误检查和特殊的操作和功能。
| 名字    | 存储空间     | 描述                    |
| :------ | :----------- | :---------------------- |
| cidr    | 7 或 19 字节 | IPv4 或 IPv6 网络       |
| inet    | 7 或 19 字节 | IPv4 或 IPv6 主机和网络 |
| macaddr | 6 字节       | MAC 地址                |
在对 inet 或 cidr 数据类型进行排序的时候， IPv4 地址总是排在 IPv6 地址前面，包括那些封装或者是映射在 IPv6 地址里的 IPv4 地址， 比如 ::10.2.3.4 或 ::ffff:10.4.3.2。
### 位串类型
位串就是一串 1 和 0 的字符串
### 文本搜索类型
全文检索即通过自然语言文档的集合来找到那些匹配一个查询的检索。
PostgreSQL 提供了两种数据类型用于支持全文检索：
### UUID 类型
uuid 数据类型用来存储 RFC 4122，ISO/IEF 9834-8:2005 以及相关标准定义的通用唯一标识符（UUID）。 （一些系统认为这个数据类型为全球唯一标识符，或GUID。） 这个标识符是一个由算法产生的 128 位标识符，使它不可能在已知使用相同算法的模块中和其他方式产生的标识符相同。 因此，对分布式系统而言，这种标识符比序列能更好的提供唯一性保证，因为序列只能在单一数据库中保证唯一。
UUID 被写成一个小写十六进制数字的序列，由分字符分成几组， 特别是一组8位数字+3组4位数字+一组12位数字，总共 32 个数字代表 128 位， 一个这种标准的 UUID 例子如下：
```
a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
```
### XML 类型
xml 数据类型可以用于存储XML数据。 将 XML 数据存到 text 类型中的优势在于它能够为结构良好性来检查输入值， 并且还支持函数对其进行类型安全性检查。 要使用这个数据类型，编译时必须使用 **configure --with-libxml**。
### JSON 类型
json 数据类型可以用来存储 JSON（JavaScript Object Notation）数据， 这样的数据也可以存储为 text，但是 json 数据类型更有利于检查每个存储的数值是可用的 JSON 值。
此外还有相关的函数来处理 json 数据：
{% raw %}
| 实例                                     | 实例结果            |
| :--------------------------------------- | :------------------ |
| array_to_json('{{1,5},{99,100}}'::int[]) | [[1,5],[99,100]]    |
| row_to_json(row(1,'foo'))                | {"f1":1,"f2":"foo"} |
{% endraw %}
### 数组类型
PostgreSQL 允许将字段定义成变长的多维数组。
数组类型可以是任何基本类型或用户定义类型，枚举类型或复合类型。
### 复合类型
复合类型表示一行或者一条记录的结构； 它实际上只是一个字段名和它们的数据类型的列表。PostgreSQL 允许像简单数据类型那样使用复合类型。比如，一个表的某个字段可以声明为一个复合类型。
# PostgreSql 常用命令
	命令都是以"\"开头  \help
### 查询登录  
	psql -h 192.168.0.1 -U username -d dbname 
	mysql -h 192.168.0.1 -uusername -ppassword
### 基本命令（第一行postSql 后面跟着  mysql ）
#### 查询所有数据库	
	\l	或者	\list
	show databases
#### 数据库切换到 database
	\c  database
	use database
#### 列出当前数据库下的数据表
	\d
	show tables
#### 列出指定表的所有字段
	\d tablename
	show columns from tablename
#### 查看指定表的基本情况
	describe tablename
	\d+ tablename
#### 退出登录
	\q
# 库，表，事务，视图等增删改查
### 数据库
```sql
-- 创建
CREATE DATABASE dbname;
createdb -h localhost -p 5432 -U postgres test01
-- 列表 使用 \l 用于查看已经存在的数据库
使用 \l 用于查看已经存在的数据库
-- 切换 \c + 数据库名 来进入数据库
\c test01
-- 删除 DROP DATABASE [ IF EXISTS ] name
DROP DATABASE test01;
dropdb -h localhost -p 5432 -U postgres test01
```
### 模式
``` sql
-- 创建
create schema myschema;
-- 创建2
CREATE SCHEMA myschema.mytable (
	...
);
-- 删除
DROP SCHEMA myschema;
-- 删除一个模式以及其中包含的所有对象
DROP SCHEMA myschema CASCADE;
```
### 表格
```sql
-- 创建
CREATE TABLE company(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL
);
CREATE TABLE IF NOT EXISTS `table1`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `title` VARCHAR(100) NOT NULL,
   `author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 列表  \d
\d
-- 添加字段  
-- ALTER TABLE table_name ADD column_name datatype;
ALTER TABLE company ADD icon text;
-- 删除
drop table company;
```
### 视图
> 与mysql一致
``` sql
-- 创建
CREATE VIEW COMPANY_VIEW AS
SELECT ID, NAME, AGE FROM  COMPANY;
-- 删除
DROP VIEW COMPANY_VIEW
```
### 事务
> 遵循acid原则， 与mysql基本没变
``` sql
BEGIN
commit
ROLLBACK
```
### 约束
* 非空	not null  指示某列不能存储 NULL 值。
  > 建表时候字段添加 NOT NULL
* 唯一   unique   确保某列的值都是唯一的。
  > 建表字段添加   UNIQUE
* 主键   primary key NOT NULL 和 UNIQUE 的结合。确保某列（或两个列多个列的结合）有唯一标识，有助于更容易更快速地找到表中的一个特定的记录。
  > 建表主键字段添加   primary key
* 外键   foreign key 保证一个表中的数据匹配另一个表中的值的参照完整性。
  > 一对多，多表上对一表的字段添加  references  表名(字段)
* 检查    check 保证列中的值符合指定的条件。
  > 建表时候字段添加，eg：字段检查，年龄必须大于18 ，age        REAL   CHECK(age > 18)
* 排他约束    exclusion 保证如果将任何两行的指定列或表达式使用指定操作符进行比较，至少其中一个操作符比较将会返回 false 或空值。
  > 
``` sql
-- 添加约束
ALTER TABLE table_name ADD CONSTRAINT some_name;
-- 删除约束
ALTER TABLE table_name DROP CONSTRAINT some_name;
```

## 性能诊断与日常运维速查

下面的 SQL 用于排查连接、锁、慢 SQL、索引、缓存和复制状态。执行前先确认数据库版本：

```sql
SELECT version();
```

本文大部分查询适用于 PostgreSQL 14 及以上版本。其中 `pg_stat_io` 从 PostgreSQL 16 开始提供，`query_id` 从 PostgreSQL 14 开始出现在 `pg_stat_activity` 中。普通用户只能看到自己会话的完整 SQL；排查全库时通常需要超级用户或 `pg_read_all_stats` 角色。

统计视图中的数据一般从数据库启动或上次重置统计时开始累计，不能只根据一次查询结果直接做删除索引、扩容或终止会话等操作。

### MySQL `SHOW PROCESSLIST` 的 PostgreSQL 等价查询

MySQL 使用 `SHOW PROCESSLIST` 查看当前连接、正在执行的 SQL、状态和耗时。PostgreSQL 对应的数据主要来自 `pg_stat_activity`。

#### 基础会话查询

```sql
SELECT
  pid AS id,
  usename AS "user",
  datname AS db,
  COALESCE(client_addr::text, 'local') AS host,
  application_name,
  state,
  wait_event_type,
  wait_event,
  CASE
    WHEN state = 'active' THEN clock_timestamp() - query_start
  END AS exec_time,
  query
FROM pg_stat_activity
WHERE backend_type = 'client backend'
  AND pid <> pg_backend_pid()
ORDER BY exec_time DESC NULLS LAST;
```

`client_addr` 才是客户端地址，`application_name` 表示客户端程序上报的名称。这里使用 `clock_timestamp()` 计算实时耗时；`now()` 在同一个事务中保持为事务开始时间，不适合观察持续增长的耗时。

#### 完整会话查询

```sql
SELECT
  pid AS session_id,
  usename AS db_user,
  datname AS database_name,
  client_addr,
  client_port,
  application_name,
  backend_start,
  xact_start,
  query_start,
  state_change,
  state,
  wait_event_type,
  wait_event,
  CASE
    WHEN state = 'active' THEN clock_timestamp() - query_start
  END AS sql_cost_time,
  CASE
    WHEN xact_start IS NOT NULL THEN clock_timestamp() - xact_start
  END AS tx_cost_time,
  query_id,
  query,
  backend_xid,
  backend_xmin
FROM pg_stat_activity
WHERE backend_type = 'client backend'
  AND pid <> pg_backend_pid()
ORDER BY query_start ASC NULLS LAST;
```

`wait_event_type` 和 `wait_event` 非空不一定代表异常，例如空闲连接可能等待客户端输入。应结合 `state`、执行时长和阻塞关系一起判断。

#### 只看正在执行的 SQL

```sql
SELECT
  pid,
  usename,
  datname,
  client_addr,
  clock_timestamp() - query_start AS run_time,
  wait_event_type,
  wait_event,
  query
FROM pg_stat_activity
WHERE backend_type = 'client backend'
  AND state = 'active'
  AND pid <> pg_backend_pid()
ORDER BY run_time DESC;
```

#### 取消 SQL 或终止会话

```sql
-- 只取消当前正在执行的 SQL，会话仍然保留
SELECT pg_cancel_backend(12345);

-- 强制断开会话，未提交事务会回滚
SELECT pg_terminate_backend(12345);
```

先通过 `pg_stat_activity` 核对 PID、用户、数据库、事务和 SQL，再执行取消或终止操作。不要终止自己的当前会话，也不要在未确认业务影响时批量终止连接。操作其他用户的会话需要超级用户、目标角色成员身份或 `pg_signal_backend` 权限；超级用户后端只能由超级用户操作。

### 锁等待与阻塞关系

#### 查看谁被谁阻塞

`pg_blocking_pids()` 能处理关系锁、事务锁和其他类型的阻塞，比只按 `relation` 连接两份 `pg_locks` 更准确。

```sql
WITH blocked_sessions AS (
  SELECT
    activity.*,
    unnest(pg_blocking_pids(activity.pid)) AS blocking_pid
  FROM pg_stat_activity AS activity
  WHERE cardinality(pg_blocking_pids(activity.pid)) > 0
)
SELECT
  blocked.pid AS blocked_pid,
  blocked.usename AS blocked_user,
  blocked.query AS blocked_sql,
  clock_timestamp() - blocked.query_start AS blocked_duration,
  blocker.pid AS blocking_pid,
  blocker.usename AS blocking_user,
  blocker.state AS blocking_state,
  blocker.query AS blocking_sql,
  clock_timestamp() - blocker.xact_start AS blocking_tx_duration
FROM blocked_sessions AS blocked
JOIN pg_stat_activity AS blocker
  ON blocker.pid = blocked.blocking_pid
ORDER BY blocked_duration DESC;
```

阻塞者可能处于 `idle in transaction`，此时它没有正在执行 SQL，但仍持有事务锁。处理前应先确认阻塞者事务是否可以提交或回滚，而不是直接终止被阻塞的一方。

#### 查看全库锁清单

```sql
SELECT
  locks.pid,
  activity.usename,
  activity.datname,
  locks.locktype,
  locks.relation::regclass AS relation,
  locks.page,
  locks.tuple,
  locks.transactionid,
  locks.mode,
  locks.granted,
  activity.state,
  activity.query
FROM pg_locks AS locks
LEFT JOIN pg_stat_activity AS activity
  ON activity.pid = locks.pid
ORDER BY locks.granted, locks.pid;
```

### 慢 SQL 与语句性能统计

`pg_stat_statements` 按归一化 SQL 累计调用次数、总耗时、平均耗时、缓存访问和返回行数。它适合找长期消耗最大的 SQL，不等同于实时慢查询日志。

#### 启用 `pg_stat_statements`

在 `postgresql.conf` 中配置：

```ini
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = 'all'
compute_query_id = 'auto'
```

修改 `shared_preload_libraries` 后需要重启数据库，然后在需要统计的数据库中创建扩展：

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

如果 `shared_preload_libraries` 已包含其他库，应把 `pg_stat_statements` 添加到现有逗号分隔列表中，不要覆盖原配置。

#### 按累计执行耗时排序

```sql
SELECT
  queryid,
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time,
  rows,
  shared_blks_hit,
  shared_blks_read
FROM pg_stat_statements
ORDER BY total_exec_time DESC;
```

#### 按单次最大执行耗时排序

```sql
SELECT
  queryid,
  query,
  calls,
  mean_exec_time,
  max_exec_time,
  total_exec_time,
  rows
FROM pg_stat_statements
ORDER BY max_exec_time DESC;
```

PostgreSQL 13 及以上版本使用 `total_exec_time`、`mean_exec_time` 和 `max_exec_time`；更老版本中的对应字段是 `total_time`、`mean_time` 和 `max_time`。

#### 重置统计数据

```sql
SELECT pg_stat_statements_reset();
```

重置会影响后续趋势对比，应先记录当前数据，并确认监控系统不依赖这段累计窗口。

### 表与索引性能统计

#### 查看全表扫描较多的表

```sql
SELECT
  schemaname,
  relname AS table_name,
  seq_scan,
  seq_tup_read,
  idx_scan,
  n_live_tup,
  n_dead_tup,
  last_analyze,
  last_autoanalyze
FROM pg_stat_user_tables
ORDER BY seq_scan DESC, seq_tup_read DESC;
```

`seq_scan` 高不等于一定缺索引。小表、需要读取大部分数据的查询和并行扫描都可能合理使用顺序扫描。应结合 `seq_tup_read`、业务查询和 `EXPLAIN (ANALYZE, BUFFERS)` 判断。

#### 查看索引使用情况

```sql
SELECT
  schemaname,
  relname AS table_name,
  indexrelname AS index_name,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC, pg_relation_size(indexrelid) DESC;
```

`idx_scan = 0` 只表示索引在当前统计周期内没有被扫描，不能直接认定索引无用。删除前还要确认统计是否刚被重置、索引是否用于主键或唯一约束、低频任务是否依赖它，以及删除后对写入和查询的影响。

#### 查看死元组占比较高的表

```sql
SELECT
  schemaname,
  relname AS table_name,
  n_live_tup,
  n_dead_tup,
  ROUND(
    100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0),
    2
  ) AS dead_ratio,
  last_vacuum,
  last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY dead_ratio DESC NULLS LAST;
```

`n_live_tup` 和 `n_dead_tup` 是估算值。确认表确实需要维护后，可执行：

```sql
VACUUM (ANALYZE, VERBOSE) public.table_name;
```

常规 `VACUUM` 可以回收空间供表内复用，但通常不会把文件空间归还给操作系统。`VACUUM FULL` 会重写表并持有排他锁，不应在生产高峰直接执行。

### I/O 与缓存命中情况

#### 数据库级缓存命中率

```sql
SELECT
  datname,
  blks_hit AS cache_hit,
  blks_read,
  ROUND(
    100.0 * blks_hit / NULLIF(blks_hit + blks_read, 0),
    2
  ) AS cache_hit_ratio
FROM pg_stat_database
WHERE datname IS NOT NULL
ORDER BY cache_hit_ratio ASC NULLS LAST;
```

`blks_read` 表示 PostgreSQL 请求读取的块，其中一部分仍可能由操作系统缓存提供，因此它不完全等同于物理磁盘读取。缓存命中率也没有适用于所有业务的固定阈值；分析时应结合工作集大小、延迟、磁盘吞吐和具体 SQL。

#### 语句级缓存命中率

```sql
SELECT
  queryid,
  calls,
  shared_blks_hit,
  shared_blks_read,
  ROUND(
    100.0 * shared_blks_hit
      / NULLIF(shared_blks_hit + shared_blks_read, 0),
    2
  ) AS cache_hit_ratio,
  query
FROM pg_stat_statements
ORDER BY shared_blks_read DESC;
```

#### PostgreSQL 16+ 的 I/O 统计

```sql
SELECT
  backend_type,
  object,
  context,
  reads,
  read_time,
  writes,
  write_time,
  hits,
  evictions,
  stats_reset
FROM pg_stat_io
ORDER BY COALESCE(reads, 0) + COALESCE(writes, 0) DESC;
```

`read_time` 和 `write_time` 依赖 `track_io_timing`。开启该配置会增加少量计时开销：

```sql
SHOW track_io_timing;
```

### 连接、事务、WAL 与复制状态

#### 当前连接数

```sql
SELECT
  count(*) AS total_conn,
  count(*) FILTER (WHERE state = 'active') AS active_conn,
  count(*) FILTER (WHERE state LIKE 'idle%') AS idle_conn
FROM pg_stat_activity
WHERE backend_type = 'client backend';

SHOW max_connections;
```

连接数接近 `max_connections` 时，不应只提高上限。还要检查连接池配置、空闲连接、单连接内存开销和系统资源。

#### 长时间空闲事务

```sql
SELECT
  pid,
  usename,
  datname,
  client_addr,
  clock_timestamp() - xact_start AS tx_duration,
  state_change,
  query
FROM pg_stat_activity
WHERE backend_type = 'client backend'
  AND state = 'idle in transaction'
  AND xact_start IS NOT NULL
ORDER BY tx_duration DESC;
```

长时间 `idle in transaction` 会长期保留事务快照和锁，阻碍垃圾回收。应优先修复应用事务边界，并按业务情况评估 `idle_in_transaction_session_timeout`。

#### WAL 写入统计

`pg_stat_wal` 从 PostgreSQL 14 开始提供：

```sql
SELECT
  wal_records,
  wal_fpi,
  wal_bytes,
  wal_buffers_full,
  stats_reset
FROM pg_stat_wal;
```

#### 流复制状态

在主库查询：

```sql
SELECT
  pid,
  usename,
  application_name,
  client_addr,
  state,
  sync_state,
  sent_lsn,
  write_lsn,
  flush_lsn,
  replay_lsn,
  write_lag,
  flush_lag,
  replay_lag
FROM pg_stat_replication;
```

延迟字段可能为 `NULL`，并且不能单独代表备用库落后多少数据；还应结合 LSN 差值、WAL 生成速度和备用库状态判断。

### 使用 `EXPLAIN` 分析慢 SQL

```sql
-- 只生成估算执行计划，不实际执行 SQL
EXPLAIN SELECT * FROM t WHERE id = 1;

-- 实际执行并显示真实行数与各节点耗时
EXPLAIN (ANALYZE) SELECT * FROM t WHERE id = 1;

-- 同时显示缓存、I/O、配置和更完整的节点信息
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS)
SELECT * FROM t WHERE id = 1;
```

`EXPLAIN ANALYZE` 会真正执行 SQL，慢查询可能继续消耗大量资源。对 `INSERT`、`UPDATE`、`DELETE` 等写操作使用时还会修改数据；即使包在可回滚事务中，也要注意序列等副作用不一定回滚。生产环境执行前必须确认影响。

分析执行计划时重点关注：估算行数与实际行数偏差、顺序扫描范围、循环次数、排序是否落盘、连接方式、缓存读取，以及最耗时的执行节点。

### 常用容量与配置查询

#### 查看数据库大小

```sql
SELECT
  datname,
  pg_size_pretty(pg_database_size(datname)) AS db_size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

#### 查看表总大小（包含索引和 TOAST）

```sql
SELECT
  schemaname,
  relname AS table_name,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

#### 查看常用配置参数

```sql
SHOW work_mem;
SHOW shared_buffers;
SHOW maintenance_work_mem;
SHOW max_connections;
```

`work_mem` 可能被单个查询中的多个排序或哈希节点分别使用，也可能被多个并发会话同时使用，因此不能简单按 `work_mem × max_connections` 估算，也不应只为一条慢 SQL 全局调大。

### 官方参考文档

- [PostgreSQL 当前版本：监控数据库活动](https://www.postgresql.org/docs/current/monitoring.html)
- [`pg_stat_activity`、`pg_stat_io` 等统计视图](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [`pg_stat_statements` 扩展](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [`EXPLAIN` 执行计划](https://www.postgresql.org/docs/current/using-explain.html)
- [服务端信号函数与连接终止](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL)
