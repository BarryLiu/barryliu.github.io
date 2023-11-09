---
layout: post
title: 数据库基本语句
category: 技术
tags:  PostgreSql
keywords: sql
description: postgreSql 
---

mysql 与 postgreSql 数据库简单使用,命令对比



# 安装与连接



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

  







# 数据类型与基本概率

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

| 实例                                     | 实例结果            |
| :--------------------------------------- | :------------------ |
| array_to_json('{{1,5},{99,100}}'::int[]) | [[1,5],[99,100]]    |
| row_to_json(row(1,'foo'))                | {"f1":1,"f2":"foo"} |



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



