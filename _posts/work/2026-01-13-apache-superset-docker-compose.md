



## 安装docker-compose版本 apache-superset记录

> bi看板,  Superset 4.0.2版本



* Docker-compose.yml

``` yml
# docker-compose.yml
# 注：version 字段可保留（无害），但新版 Compose 已不强制要求

services:
  superset:
    image: apache/superset:4.0.2
    container_name: superset_app
    restart: unless-stopped
    ports:
      - "8088:8088"
    environment:
      # 必填：密钥（请确保 .env 中提供）
      SUPERSET_SECRET_KEY: "${SUPERSET_SECRET_KEY}"

      # 外部 PostgreSQL 元数据数据库
      SUPERSET_METADATA_DB_URL: "postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

      # 外部 Redis（用于 Celery Broker，db=1）
      SUPERSET_REDIS_URL: "redis://:${REDIS_PASS}@${REDIS_HOST}:${REDIS_PORT}/1"

      # 可选配置
      SUPERSET_TIMEZONE: "Asia/Shanghai"
    # ⚠️ 关键修改：删除 command 行！使用镜像默认入口
    # 容器会自动启动 Web 服务，初始化需手动执行一次
    volumes:
      - superset_home:/home/superset

volumes:
  superset_home:


```



* .env

  >  虽然配置了外面的redis和数据库,但是没有用到

``` shell

# .env
SUPERSET_SECRET_KEY=your-very-long-secret-key-change-in-prod

# PostgreSQL
DB_HOST=172.16.10.107
DB_PORT=5432
DB_USER=superset_meta
DB_PASS=xxxxxx
DB_NAME=superset_meta

# Redis（含密码）
REDIS_HOST=172.16.10.107
REDIS_PORT=6379
REDIS_PASS=xxx

```





### 启动

``` shell

# 启动
docker-compose up -d

# 安装表
# 1. 升级数据库（创建表结构）
docker exec -it superset_app superset db upgrade

# 2. 创建管理员用户（关键！用 flask fab）
#docker exec -it superset_app flask fab create-admin

# 3. 初始化权限和角色
#docker exec -it superset_app superset init


# 2. 创建角色-执行下面命令创建
docker exec -it superset_app flask fab create-admin

# 2.1 初始化用户权限
docker exec -it superset_app superset init

# 3. 查看帮助
docker exec -it superset_app flask fab --help

# 4.查看用户
docker exec -it superset_app flask fab list-users

```

