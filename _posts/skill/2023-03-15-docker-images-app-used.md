---
layout: post
title: docker 应用推荐
category: docker
tags:  docker
keywords: docker
description: docker images ，

---



网上有很多优秀的可玩性高的 docker image，





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
