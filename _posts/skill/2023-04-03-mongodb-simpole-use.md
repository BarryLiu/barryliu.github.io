---
layout: post
title: mongo db 简单使用
category: 技术
tags: MongoDb
keywords: mongoDb,docker
description: mongoDb,docker安装mongodb, MongoDB增删改查,用户管理


---

> 





use martin1;


db.test.insert({name:'bob',age:12})


db.dropDatabase();

db.getUsers() 

db.system.users.find()



### 安装

* 软件安装(省略)

* docker安装

  * docker命令

    ``` shell
     docker run -p 27017:27017 -v /data/mongo:/data/db --name mongodb -d mongo
     
     # 需要账号密码登陆,可以先用上面命令创建应用,添加好高权限账号后删除容器并用下面命令重启
     docker run -p 27017:27017 -v /data/mongo:/data/db --name mongodb -d mongo --auth
     
     
     docker run -p 27017:27017 -v D:/myDocker/mongodb/db:/data/db -v  D:/myDocker/mongodb/bin:/usr/bin --name mongodb -d mongo
     
    ```
    
    

### 内置角色

* root  # 超级管理员
* readWrite # 对某个非系统库读写权限
* read  #  对某个非系统库读权限
* readWriteAnyDatabase   # 对所有系统库读写权限
* readAnyDatabase # 对所有系统库读权限



### 可视化工具

* navicat Premium
* MongoDB Compass
  * 地址： https://www.mongodb.com/try/download/shell

​			

### 用户与权限操作



``` shell
# 创建mongodb用户
use admin;

db.createUser({
    user: 'admin',
    pwd: 'Aa123456',
    roles: [{
        role: "userAdminAnyDatabase",
        db: "admin"
    }]
});

```







### 简单crud操作



``` shell

show dbs;

db.version()

use testmg;

创建集合
db.createCollection('test1')

删除集合
db.test1.drop();

# 写入一行
db.test1.save({name:'bob',age:13})
# 写入一行
db.test1.insert({name:'bob2',age:13})
# 写入多行,会返回对应的id
db.test1.insertMany([{name:'bob3',age:13},{name:'bob4',age:13}])

# 循环插入
for (var i=0;i<=100;i++){
	db.test2.insert({name:'a',age:15,idx:i})
}
db.test2.find()

# 查询
db.test1.find();
# 带条件查询
db.test1.find({name:'bob'})

# 大于小于查询, $gt,$lt,$lte,$gte,$ne
db.test2.find({idx:{$gt:50}})
# 多条件查询
db.test2.find({$and:[{idx:{$gt:50}},{idx:{$lt:60}}])
db.test2.find({$or:[{idx:{$gt:50}},{idx:{$lt:60}}])

# 修改
db.test1.update({name:'bob'},{$set:{age:15}})

# 按条件删除
db.test1.remove({name:'bob2'})

# 删除全部数据
db.test1.remove({})
```





### 统计查询

``` shell
# sort排序: 1 升序,-1,降序
db.test2.find().sort({idx:-1})

#查询总数
db.test2.find().count()

# 分页查询 语法: db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)  -- skip默认数量为0
db.test2.find().limit(10).skip(2) 

# 聚合查询,查询班级中最高分、最低分、平均分,$avg,$max,$min,$sum,$first,$last
db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)
db.test3.aggregate([{'$group':{_id:'$name','avg_score':{'$avg':'$score'}}}])


# 索引，1 为升序索引，降序索引： -1
db.test4.createIndex({"title":1})
## 复合索引
db.test4.createIndex({"title":1,"description":-1})
##查看集合索引
db.col.getIndexes()
##查看集合索引大小
db.col.totalIndexSize()
##删除集合所有索引
db.col.dropIndexes()
##删除集合指定索引
db.col.dropIndex("索引名称")

```



### 索引

``` shell
# 索引，1 为升序索引，降序索引： -1
db.test4.createIndex({"title":1})
## 复合索引
db.test4.createIndex({"title":1,"description":-1})

## 数值索引，多值索引,下面的查询能用到索引
db.test5.insert({name:'bob',tag:['a','b','c']})
db.test5.createIndex({'tag':1})
db.test5.find({'tag':'b'})

##全文索引,全文索引关键字 text,一个表中只有一个全文索引
db.test4.createIndex({"title":'text'})

##其它索引默认 btree类型,
# hash索引(不支持范围查询,不支持多键hash)
db.test4.createIndex({"title":'hashed'})

##地理位置索引
db.test5.insertMany([{loc:[1,1]},{loc:[11,11]},{loc:[21,21]}])
db.test5.createIndex({loc:'2d'})
db.test5.find({loc:{$geoWithin:$box:[[10,10],[12,12]] }})


##查看集合索引
db.col.getIndexes()
##查看集合索引大小
db.col.totalIndexSize()
##删除集合所有索引
db.col.dropIndexes()
##删除集合指定索引
db.col.dropIndex("索引名称")

# 强制使用索引 hint
db.users.find({gender:"M"},{user_name:1,_id:0}).hint({gender:1,user_name:1})

```



### 索引执行计划

> 每个索引占据一定的存储空间，在进行插入，更新和删除操作时也需要对索引进行操作。所以，如果你很少对集合进行读取操作，建议不使用索引。
>
> 由于索引是存储在内存(RAM)中,你应该确保该索引的大小不超过内存的限制。
>
> 如果索引的大小大于内存的限制，MongoDB会删除一些索引，这将导致性能下降。
>
> 
>
> 索引不能被以下的查询使用：
>
> - 正则表达式及非操作符，如 $nin, $not, 等。
> - 算术运算符，如 $mod, 等。
> - $where 子句
>
> 
>
> 最大范围
>
> - 集合中索引不能超过64个
> - 索引名的长度不能超过128个字符
> - 一个复合索引最多可以有31个字段

``` shell

# explain

# 执行计划explain， 各个查询后面加 .explain()
db.test5.find().explain()
db.test5.find().explain(queryPlanner) #默认
db.test5.find().explain(’executionStats‘) #详细分布执行计划
db.test5.find().explain(’allPlansExecution‘) #所有执行计划,或者 db.test5.find().explain(true) 


## 执行计划分析
executionStats -> totalDocsExamined # 扫描文档数,越少越好
executionStats -> executionTimeMillis # 执行时间
executionStats -> executionStages -> stage: # 是否用索引, COLLSCAN:全表扫描, FEATCH:走索引

# 查看是否开启慢查询: 未开启:0,已开启:1
db.getProfilingLevel()

# 设置开启慢查询,并且查询超过100毫秒归类慢查询
db.setProfilingLevel(1, 100)
# 关闭慢查询
db.setProfilingLevel(0)

# 查询慢查询
db.system.profile.find().limit(1)


```





### 监控

> mongostat ,mongotop,db.serverStatus()

``` shell 

db.serverStatus()



```

