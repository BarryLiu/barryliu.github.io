---
layout: post
title: docker 应用推荐
category: docker
tags:  docker
keywords: docker
description: docker images ，

---



网上有很多优秀的可玩性高的 docker image，



[各种docker镜像部署](https://blog.csdn.net/qq905855661/article/details/123965291)



### 桌面导航  [linuxserver/heimdall](https://hub.docker.com/r/linuxserver/heimdall)

> 桌面导航

``` shell
# 下载
docker pull linuxserver/heimdall

# 运行
 docker run -d --name=my_nav_80_heimdall --restart=always -p 80:80  linuxserver/heimdall
# 官方命令
docker run -d \
  --name=heimdall \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 80:80 \
  -p 443:443 \
  -v /path/to/appdata/config:/config \
  --restart unless-stopped \
  lscr.io/linuxserver/heimdall:latest



```



#### 相册 [Lychee](https://hub.docker.com/r/lycheeorg/lychee)

> 相册  
>
> 同类型相册
>
> lychee 、 轻量级，快，能播放视频，功能少
>
> Photoprism 、新起之秀，不过该有的都有了：人脸识别、地图，主题等 ,github starts 18w+
>
> Piwigo 、老牌软件 Piwigo ,有客户端app
>
> LibrePhotos 、和PhotoPrism差不多，无中文 （不推荐）
>
> Photoview = 、新起之秀，也有人脸识别等功能，在不断更新中，汉化不是很完整 、

``` shell
# 下载
docker pull lycheeorg/lychee
# 运行
docker run -it -d -p 90:80  lycheeorg/lychee

# 官方命令
docker run -d \
--name=lychee \
-v /host_path/lychee/conf:/conf \
-v /host_path/lychee/uploads:/uploads \
-v /host_path/lychee/sym:/sym \
-e PUID=1000 \
-e PGID=1000 \
-e PHP_TZ=America/New_York \
-e DB_CONNECTION=mysql \
-e DB_HOST=mariadb \
-e DB_PORT=3306 \
-e DB_DATABASE=lychee \
-e DB_USERNAME=user \
-e DB_PASSWORD=password \
-p 90:80 \
--net network_name \
--link db_name \
lycheeorg/lychee

```



### 漫画 lanraragi_cn 

> 漫画的镜像，分别是 Mango、Komga、Ubooquity、LANraragi、HappyPanda X [参考](https://xsinger.me/diy/1610.html) 
>
> tachidesk 



#### 视频 Jellyfin 和 Nextcloud

> jellyfin

``` shell 

# 启动jellyfin容器
docker run -d --restart=always \
--name=jellyfin \
-p 8096:8096 -p 8920:8920 \
-v /home/dockerspace/jellyfin/config:/config -v /home/dockerspace/jellyfin/media:/media \
linuxserver/jellyfin:latest


```





####  rabbitmq 

> RabbitMQ是由erlang语言开发，基于AMQP（Advanced Message Queue 高级消息队列协议）协议实现的消息队列，它是一种应用程序之间的通信方法，消息队列在分布式系统开发中应用非常广泛。

[参考页面](https://huaweicloud.csdn.net/638db4f8dacf622b8df8ccb9.html?spm=1001.2101.3001.6650.6&utm_medium=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~activity-6-127265712-blog-124470698.235^v32^pc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~activity-6-127265712-blog-124470698.235^v32^pc_relevant_default_base3&utm_relevant_index=11)

``` shell
# 运行 rabitmq, 15672(UI页面通信口)、5672(client端通信口)、25672(server间内部通信口)、61613(stomp 消息传输)、1883(MQTT消息队列遥测传输)。
docker run -d --name rabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:management

```



#### Nacos

> nacos 需要创建数据库,并配置数据库连接



[参考页面](https://blog.csdn.net/xtldcn/article/details/128867700)

[参考页面2](https://blog.csdn.net/ruoshuiyx/article/details/128325474?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-1-128325474-blog-128867700.235^v32^pc_relevant_default_base3&spm=1001.2101.3001.4242.2&utm_relevant_index=4)

``` sql
# 1.nacos提供执行的sql
# 宿主机的mysql新建nacos的数据库，并执行脚本 sql脚本地址如下：
https://github.com/alibaba/nacos/blob/master/config/src/main/resources/META-INF/nacos-db.sql

# 2.需要进行创建一个nacos数据库，并执行对应的数据库语句：

/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info   */
/******************************************/
CREATE TABLE `config_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) DEFAULT NULL,
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  `c_desc` varchar(256) DEFAULT NULL,
  `c_use` varchar(64) DEFAULT NULL,
  `effect` varchar(64) DEFAULT NULL,
  `type` varchar(64) DEFAULT NULL,
  `c_schema` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfo_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_aggr   */
/******************************************/
CREATE TABLE `config_info_aggr` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) NOT NULL COMMENT 'group_id',
  `datum_id` varchar(255) NOT NULL COMMENT 'datum_id',
  `content` longtext NOT NULL COMMENT '内容',
  `gmt_modified` datetime NOT NULL COMMENT '修改时间',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfoaggr_datagrouptenantdatum` (`data_id`,`group_id`,`tenant_id`,`datum_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='增加租户字段';
 
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_beta   */
/******************************************/
CREATE TABLE `config_info_beta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL COMMENT 'content',
  `beta_ips` varchar(1024) DEFAULT NULL COMMENT 'betaIps',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfobeta_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info_beta';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info_tag   */
/******************************************/
CREATE TABLE `config_info_tag` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `tenant_id` varchar(128) DEFAULT '' COMMENT 'tenant_id',
  `tag_id` varchar(128) NOT NULL COMMENT 'tag_id',
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(20) DEFAULT NULL COMMENT 'source ip',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfotag_datagrouptenanttag` (`data_id`,`group_id`,`tenant_id`,`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info_tag';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_tags_relation   */
/******************************************/
CREATE TABLE `config_tags_relation` (
  `id` bigint(20) NOT NULL COMMENT 'id',
  `tag_name` varchar(128) NOT NULL COMMENT 'tag_name',
  `tag_type` varchar(64) DEFAULT NULL COMMENT 'tag_type',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(128) NOT NULL COMMENT 'group_id',
  `tenant_id` varchar(128) DEFAULT '' COMMENT 'tenant_id',
  `nid` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`nid`),
  UNIQUE KEY `uk_configtagrelation_configidtag` (`id`,`tag_name`,`tag_type`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_tag_relation';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = group_capacity   */
/******************************************/
CREATE TABLE `group_capacity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `group_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'Group ID，空字符表示整个集群',
  `quota` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配额，0表示使用默认值',
  `usage` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用量',
  `max_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个配置大小上限，单位为字节，0表示使用默认值',
  `max_aggr_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '聚合子配置最大个数，，0表示使用默认值',
  `max_aggr_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值',
  `max_history_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大变更历史数量',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='集群、各Group容量信息表';
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = his_config_info   */
/******************************************/
CREATE TABLE `his_config_info` (
  `id` bigint(64) unsigned NOT NULL,
  `nid` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `data_id` varchar(255) NOT NULL,
  `group_id` varchar(128) NOT NULL,
  `app_name` varchar(128) DEFAULT NULL COMMENT 'app_name',
  `content` longtext NOT NULL,
  `md5` varchar(32) DEFAULT NULL,
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00',
  `src_user` text,
  `src_ip` varchar(20) DEFAULT NULL,
  `op_type` char(10) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  PRIMARY KEY (`nid`),
  KEY `idx_gmt_create` (`gmt_create`),
  KEY `idx_gmt_modified` (`gmt_modified`),
  KEY `idx_did` (`data_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='多租户改造';
 
 
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = tenant_capacity   */
/******************************************/
CREATE TABLE `tenant_capacity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `tenant_id` varchar(128) NOT NULL DEFAULT '' COMMENT 'Tenant ID',
  `quota` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配额，0表示使用默认值',
  `usage` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '使用量',
  `max_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个配置大小上限，单位为字节，0表示使用默认值',
  `max_aggr_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '聚合子配置最大个数',
  `max_aggr_size` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值',
  `max_history_count` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '最大变更历史数量',
  `gmt_create` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT '2010-05-05 00:00:00' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='租户容量信息表';
 
 
CREATE TABLE `tenant_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `kp` varchar(128) NOT NULL COMMENT 'kp',
  `tenant_id` varchar(128) default '' COMMENT 'tenant_id',
  `tenant_name` varchar(128) default '' COMMENT 'tenant_name',
  `tenant_desc` varchar(256) DEFAULT NULL COMMENT 'tenant_desc',
  `create_source` varchar(32) DEFAULT NULL COMMENT 'create_source',
  `gmt_create` bigint(20) NOT NULL COMMENT '创建时间',
  `gmt_modified` bigint(20) NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tenant_info_kptenantid` (`kp`,`tenant_id`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='tenant_info';
 
CREATE TABLE users (
    username varchar(50) NOT NULL PRIMARY KEY,
    password varchar(500) NOT NULL,
    enabled boolean NOT NULL
);
 
CREATE TABLE roles (
    username varchar(50) NOT NULL,
    role varchar(50) NOT NULL,
    constraint uk_username_role UNIQUE (username,role)
);
 
CREATE TABLE permissions (
    role varchar(50) NOT NULL,
    resource varchar(512) NOT NULL,
    action varchar(8) NOT NULL,
    constraint uk_role_permission UNIQUE (role,resource,action)
);
 
INSERT INTO users (username, password, enabled) VALUES ('nacos', '$2a$10$EuWPZHzz32dJN7jexM34MOeYirDdFAZm2kuWj7VEOJhhZkDrxfvUu', TRUE);
 
INSERT INTO roles (username, role) VALUES ('nacos', 'ROLE_ADMIN'); 
```







``` shell
# docker pull nacos/nacos-server

mkdir -p /mydata/nacos/logs/                      #新建logs目录
mkdir -p /mydata/nacos/init.d/          
vim /mydata/nacos/init.d/custom.properties        #修改配置文件


# custom.properties配置文件
server.contextPath=/nacos
server.servlet.contextPath=/nacos
server.port=8848

spring.datasource.platform=mysql
db.num=1
db.url.0=jdbc:mysql://xx.xx.xx.x:3306/nacos_config? characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true #这里需要修改端口
db.user=user #用户名
db.password=pass #密码

nacos.cmdb.dumpTaskInterval=3600
nacos.cmdb.eventTaskInterval=10
nacos.cmdb.labelTaskInterval=300
nacos.cmdb.loadDataAtStart=false
management.metrics.export.elastic.enabled=false
management.metrics.export.influx.enabled=false
server.tomcat.accesslog.enabled=true
server.tomcat.accesslog.pattern=%h %l %u %t "%r" %s %b %D %{User-Agent}i
nacos.security.ignore.urls=/,/**/*.css,/**/*.js,/**/*.html,/**/*.map,/**/*.svg,/**/*.png,/**/*.ico,/console-fe/public/**,/v1/auth/login,/v1/console/health/**,/v1/cs/**,/v1/ns/**,/v1/cmdb/**,/actuator/**,/v1/console/server/**
nacos.naming.distro.taskDispatchThreadCount=1
nacos.naming.distro.taskDispatchPeriod=200
nacos.naming.distro.batchSyncKeyCount=1000
nacos.naming.distro.initDataRatio=0.9
nacos.naming.distro.syncRetryDelay=5000
nacos.naming.data.warmup=true
nacos.naming.expireInstance=true 

# 运行
docker  run \
--name nacos -d \
-p 8848:8848 \
--privileged=true \
--restart=always \
-e JVM_XMS=256m \
-e JVM_XMX=256m \
-e MODE=standalone \
-e PREFER_HOST_MODE=hostname \
-v /mydata/nacos/logs:/home/nacos/logs \
-v /mydata/nacos/init.d/custom.properties:/home/nacos/init.d/custom.properties \
nacos/nacos-server 

#最后设置nacos自启动
docker update --restart=always  nacos

```



[参考文档](https://blog.csdn.net/weixin_45941687/article/details/120204230)

``` shell

# 7.正式创建容器
docker run -itd \
--privileged=true \
-e PREFER_HOST_MODE=hostname \
-e MODE=standalone \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=172.11.22.232 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_USER=sqlname \
-e MYSQL_SERVICE_PASSWORD=123456 \
-e MYSQL_SERVICE_DB_NAME=li_nacos \
-e TIME_ZONE='Asia/Shanghai' \
-p 8848:8848 \
-v /data/docker/nacos/logs:/home/nacos/logs \
-v /data/docker/nacos/conf:/home/nacos/conf \
-v /data/docker/nacos/data:/home/nacos/data \
--name nacos \
--restart=always \
nacos/nacos-server:latest


【
细节解析
docker run -d \
--privileged=true \给与权限，使用该参数，container内的root拥有真正的root权限
-e PREFER_HOST_MODE=hostname \ # 
-e MODE=standalone \ # 使用单机模式
-e SPRING_DATASOURCE_PLATFORM=mysql \ # 数据库类型
-e MYSQL_SERVICE_HOST=localhost \ # 数据库地址
-e MYSQL_SERVICE_USER=root \ # 数据库账号
-e MYSQL_SERVICE_PASSWORD=12345678 \ # 数据库密码
-e MYSQL_SERVICE_DB_NAME=nacos_config_name \ # 数据库名称
-e JVM_XMS=256m \ # 程序启动时占用内存大小
-e JVM_XMX=256m \ # 程序运行期间最大可占用的内存大小
-e JVM_XMN=256m \ # 
-p 8848:8848 \ #端口映射
-v /lbs/nacos/logs:/nacos/logs \ #挂载
--name nacos \ #容器名 
--restart=always \ # 自动启动
nacos/nacos-server:latest #镜像名:版本（是最新的版本直接镜像名即可）

学习链接：https://blog.csdn.net/PyongSen/article/details/124627058
】

```

#### nacos 安装包安装

> 使用docker 安装多次失败,安装包方式安装

``` shell
# github代码库 https://github.com/alibaba/nacos/
# 1.下载安装包，并解压

unzip nacos-server-1.0.0.zip
cd nacos/bin 
# 2.执行启动命令[单机启动]
sh startup.sh -m standalone


```





#### Minio

> 类似于阿里云OSS
>
> Minio 是一个基于Apache License v2.0开源协议的对象存储服务，虽然轻量，却拥有着不错的性能。它兼容亚马逊S3云存储服务接口，非常适合于存储大容量非结构化的数据。 
>
> 例如图片、视频、日志文件、备份数据和容器/虚拟机镜像等，而一个对象文件可以是任意大小，从几 kb 到最大 5T 不等。

官方文档：https://docs.min.io/docs/

参考文档: https://blog.csdn.net/BThinker/article/details/125412751

``` shell 

# 拉取镜像
docker pull minio/minio

# 创建存放文件和数据的映射目录
mkdir -p /home/dockerspace/minio/config
mkdir -p /home/dockerspace/minio/data

# 运行命令(账号长度必须大于等于5，密码长度必须大于等于8位(MINIO_ACCESS_KEY|MINIO_SECRET_KEY)) (控制台界面:9090,S3-API规范接口:9000)
# 貌似指定端口没有，它还是用了 9000(api) 和 45347(控制台)端口
docker run -p 9000:9000 -p 9090:9090 \
     --net=host \
     --name minio \
     -d --restart=always \
     -e "MINIO_ROOT_USER=minioadmin" \
     -e "MINIO_ROOT_PASSWORD=minioadmin" \
     -v /home/dockerspace/minio/data:/data \
     -v /home/dockerspace/minio/config:/root/.minio \
     minio/minio server \
     /data 

#访问
http://xxxxx:9090/login



```



#### mysql 

[参考文档](https://blog.csdn.net/qq_41890624/article/details/127849851)

> mysql数据挂载目录

``` shell
# 

docker run -d -p 3306:3306 --privileged=true -v /usr/local/mysql/log:/var/log/mysql -v /usr/local/mysql/data:/var/lib/mysql -v /usr/local/mysql/conf:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=123456 --name mysql mysql:5.7

```



#### redis

[参考文档](https://blog.csdn.net/m0_55070913/article/details/126628271)

> redis安装
>
> 命令分析
>
> -p 6379:6379 端口映射：前表示主机部分，：后表示容器部分。
>
> –name redis 指定该容器名称，查看和进行操作都比较方便。
>
> -v 挂载文件或目录 ：前表示主机部分，：后表示容器部分。
>
> -d redis 表示后台启动redis
>
> redis-server /etc/redis/redis.conf
> 以配置文件启动redis，加载容器内的conf文件，最终找到的是挂载的目录/usr/local/docker/redis.conf
>
> –appendonly yes 开启redis 持久化
>
> –requirepass 123456 设置密码为123456 

``` shell
# 1.下载配置文件并赋予权限,修改为允许所有访问
wget http://download.redis.io/redis-stable/redis.conf
chmod 777 redis.conf
# 2.允许所有访问 ,修改redis.conf 
bind 127.0.0.1 #注释掉，解除本地连接限制
requirepass #设置密码


docker run -p 6379:6379 --name redis -v /usr/local/redis/redis.conf:/etc/redis/redis.conf  -v /usr/local/redis/data:/data -d redis redis-server /etc/redis/redis.conf --appendonly yes -–requirepass 123456

```



#### Harbor 

> docker镜像仓库 
>
> Harbor是一个用于存储和分发Docker镜像的企业级Registry服务器，由vmware开源，在Docker Registry的基础至上添加了一些企业必需的功能特性，例如安全认证、镜像扫描和镜像管理、远程镜像复制等，扩展了开源的Docker Distribution的功能，作为一个企业级的私有Registry服务器，Harbor提供了更好的性能和安全，提升了用户使用Registry分发镜像镜像的效率，Harbor支持安装在多个Registry节点以实现镜像资源夸主机复制、从而实现镜像服务的高可用和镜像数据的安全，另外将镜像全部保存在私有网络的Registry中， 也可以确保代码数据和密码配置等信息仅在公司内部网络中传输，从而保证核心数据的安全性。 

harbor官方网址：https://goharbor.io/

harbor官方github地址：https://github.com/vmware/harbor

参考:https://www.cnblogs.com/gengxiaonuo/p/16840026.html

* 1.github下载对应的离线版

  https://github.com/goharbor/harbor/releases

* 2.上传到安装目录解压

  tar xvf harbor-offline-installer-v2.8.3.tgz 

  cd harbor/

  拷贝harbor.yml.tmpl为harbor.yml：cp harbor.yml.tmpl harbor.yml

  修改 harbor.yml中的 hostname 和port， 如果不需要https则注释https后的内容

* 3.分别执行编译命令

  ./prepare

* 4.执行安装命令

  ./intall.sh

* 5.登陆后台配置,默认账号 admin Harbor12345

* 6.客户端docker配置 信任仓库

  > vim /etc/docker/daemon.json
  >
  > //insecure-registries 节点下添加 仓库地址
  >
  > services docker restart 或者 systemctl restart docker

* 7.登陆

  docker login -u admin -p Harbor12345 192.168.86.20:85

  

  

  















- Apache + PHP7.2
- Frp 作为内网穿透
- Samba 作为本地文件共享
- H5ai 用来做文件索引
- Yellow 作为博客系统
- KodExplorer 作为文件管理器
- Docker
- Portainer 作为 Docker 的图形化管理工具
- Lychee 作为相册
- Jellyfin 作为媒体中心
- Nextcloud 作为网盘



lychee、Shiori、ddns、frp、transmission、qbittorrent、Selfoss、Bitwarden、Heimdall、Navidrome、Mango 等，主要是一些下载工具和相册、书签管理器、外网连接工具、RSS 阅读器、导航页、音乐播放器、漫画阅读器等。
