---
layout: post
title:  
date:   2024-10-09 15:14:54
categories: java docker
tags: java docker



---





#### 问题场景


>Springboot项目中,某个功能需要使用到外部文件, ftp,smb等协议共享出的内容, 



#### 尝试方向

1. java程序集成smb功能的 jar包实现, (jcifs,或者  Apache Commons VFS) ,理论最好的方式

   > 结果都没调通，并且需要修改为这些jar包中的类去调用,（入侵性强,并且需要改代码）没调通不详细写过程了

2.  用运行的ubuntu挂载远程到磁盘, 然后将挂载的内容mount映射到docker里面,(就像本地文件一样开发调试) (不足之处,与宿主机绑定不好动态扩容缩容)

   > 最终采用

3. 挂载到docker-compose.yml里面，和上面第二种方式一样,挂载时间长了有发现远程挂载的容易掉(第二种第三种都有此问题)，挂载方式

   > 按照下面挂载方式,挂载,使用

   ``` yaml
   
   version : '3.8'
   services:
     pdm-backend:
       image: pdm-backend
       build:
         context: .
         dockerfile: Dockerfile
       ports:
         - "23453:23453"
       restart: unless-stopped # 除非用户明确地停止了容器，否则总是重启容器，即使宿主机重启 (no(默认),on-failure,always,unless-stopped)
       volumes:
         - smb-share:/192.168.110.94/SW-Version
   volumes:
     smb-share:
       driver: local
       driver_opts:
         type: cifs
         o: username=yingjing.liu,password=Dream@123@@,vers=2.1,addr=192.168.110.94,r
         device: "//192.168.110.94/SW-Version"
   networks:
     proxynetwork:
       external: true
   
   ```

   



#### 以下是上面第二种方式的实现



1. 到docker容器部署的主机上挂载，下面sql语句种的  **/mnt/smb_mount** 要替换成挂载的docker-compose.yml 文件夹下的 files文件夹下，用docker挂载

``` shell

# 创建挂载文件夹
# mkdir /mnt/smb_mount

# 挂载网络磁盘 -o ro, 为只读方式打开
# mount -t cifs -o ro, //192.168.110.94/SW-Version /mnt/smb_mount -o username=yourname,password=yourpassword

# 移除网络磁盘
# umount /mnt/smb_mount

```

2.  docker-compose配置添加映射

   

   ``` yaml
   
   version : '3.8'
   services:
     pdm-backend:
       image: pdm-backend
       build:
         context: .
         dockerfile: Dockerfile
       ports:
         - "23453:23453"
       restart: unless-stopped # 除非用户明确地停止了容器，否则总是重启容器，即使宿主机重启 (no(默认),on-failure,always,unless-stopped)
       volumes:
         - ./files:/192.168.110.94/SW-Version
   networks:
     proxynetwork:
       external: true
   
   
   ```

   







#### 长时间后挂载的盘容易掉问题解决

> 可能网络抖动或者文件服务器重启,会导致挂载的盘掉了， 找了很多都没找到重连机制，都是只有启动的时候映射上去, 现新增下面脚本,到jenkons种配置定时频率调用，监听到这个镜像没有这个任务



``` shell

#!/bin/bash

# 镜像名称容器名称与内部挂载目录
image_name="pdm-backend"
container_name="pdm-pdm-backend-1"
target_path="/192.168.110.94/SW-Version"


# 判断是否运行,没运行不需要判断是否挂载
#!/bin/bash

running_count=$(docker ps --format '{{.Image}}' | grep -c $image_name)
if [ $running_count -gt 0 ]; then
    echo "The image $image_name has at least one container running."
else
    echo "The image $image_name has no containers running."
    echo "The shell is exit(没有容器运行,shell脚本退出)..."
    exit 1
fi


# 判断是否挂载
mount_info=$(docker inspect --format='{{ json .Mounts }}' $container_name | jq)
is_mounted=$(echo $mount_info | jq -e --arg path $target_path '.[] | select(.Destination == $path)')
if [ -n "$is_mounted" ]; then
#if echo $mount_info | jq -e --arg path $target_path '.[] | select(.Destination == $path)' >/dev/null; then
       	echo "The path $target_path is mounted. 无需重启"
else
	echo "The path $target_path is not mounted. 立即重启"
	# 没有挂载,重启docker-compose让其重启后自动挂载
	# echo "重启程序已重新挂载"
	docker-compose -f /home/dell/.jenkins/workspace/xc-pdm-backend/docker-compose.yml -p pdm stop pdm-backend
	docker-compose -f /home/dell/.jenkins/workspace/xc-pdm-backend/docker-compose.yml -p pdm up pdm-backend -d 
	echo '重启成功'	
fi
```





### jenkins配置定时触发任务

新建jenkins Item -> 在构建触发器中勾选 [Build periodically]  -> 勾选后再设置为需要的触发时间 eg: 0 * * * *  (每小时触发一次)



并且到shell命令中增加配置

``` shell
echo '监听mounts开始'

chmod 777 /home/dell/shell/lisenPdmMount.sh
/home/dell/shell/lisenPdmMount.sh

echo '监听mounts结束'
```

