---
layout: post
title: Python SQLAlchemy与Alembic数据库迁移笔记
category: 技术
tags: python sqlalchemy alembic database
keywords: python sqlalchemy alembic 数据库迁移 ORM
description: 记录Python下SQLAlchemy ORM框架和Alembic数据库迁移工具的使用知识点
---

# Python SQLAlchemy与Alembic数据库迁移

## 前言

SQLAlchemy 是 Python 中最流行的 ORM 框架之一，提供了完整的 SQL 能力和企业级持久化模式。Alembic 是 SQLAlchemy 作者开发的数据库迁移工具，轻量级且功能强大，类似于 Django 的 migration 或 Ruby on Rails 的 migrations。

## 一、SQLAlchemy 基础

### 1.1 安装

```bash
pip install sqlalchemy
# 或安装带异步支持的版本
pip install sqlalchemy[asyncio]
```

### 1.2 连接数据库

```python
from sqlalchemy import create_engine

# SQLite
engine = create_engine('sqlite:///example.db')

# MySQL
engine = create_engine('mysql+pymysql://user:password@localhost:3306/dbname')

# PostgreSQL
engine = create_engine('postgresql://user:password@localhost:5432/dbname')

# 连接池配置
engine = create_engine(
    'mysql+pymysql://user:password@localhost:3306/dbname',
    pool_size=10,          # 连接池大小
    max_overflow=5,        # 超过pool_size后允许的最大连接数
    pool_timeout=30,       # 获取连接超时时间
    pool_recycle=3600,     # 连接回收时间
    echo=True              # 打印SQL日志
)
```

### 1.3 定义模型

```python
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    email = Column(String(100), unique=True, nullable=False, comment='邮箱')
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    posts = relationship('Post', back_populates='author')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    author = relationship('User', back_populates='posts')
```

### 1.4 Session 操作

```python
from sqlalchemy.orm import sessionmaker, Session

# 创建Session工厂
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 使用上下文管理器
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# CRUD 操作示例
def create_user(db: Session, username: str, email: str, password: str):
    user = User(username=username, email=email, password_hash=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, **kwargs):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
```

### 1.5 查询进阶

```python
from sqlalchemy import or_, and_, func, desc

# 条件查询
users = db.query(User).filter(User.username.like('%test%')).all()

# 多条件组合
users = db.query(User).filter(
    and_(
        User.username.like('%test%'),
        or_(User.email.endswith('@gmail.com'), User.email.endswith('@qq.com'))
    )
).all()

# 排序和分页
users = db.query(User).order_by(desc(User.created_at)).offset(10).limit(10).all()

# 聚合查询
from sqlalchemy import func
result = db.query(
    User.username,
    func.count(Post.id).label('post_count')
).join(Post).group_by(User.id).all()

# 关联查询（JOIN）
posts = db.query(Post).join(User).filter(User.username == 'admin').all()

# 使用 outerjoin
posts = db.query(Post).outerjoin(User).all()

# 子查询
subq = db.query(Post.user_id, func.count('*').label('count')).group_by(Post.user_id).subquery()
result = db.query(User, subq.c.count).outerjoin(subq, User.id == subq.c.user_id).all()
```

## 二、Alembic 数据库迁移

### 2.1 安装与初始化

```bash
pip install alembic

# 在项目根目录初始化
cd your_project
alembic init alembic
```

初始化后会生成以下结构：

```
your_project/
├── alembic/
│   ├── versions/          # 迁移脚本存放目录
│   ├── env.py            # Alembic 环境配置
│   ├── script.py.mako    # 迁移脚本模板
│   └── README
├── alembic.ini           # Alembic 配置文件
└── your_models.py
```

### 2.2 配置 alembic.ini

修改 `alembic.ini` 文件中的数据库连接：

```ini
# alembic.ini
[alembic]
# 迁移脚本存放目录
script_location = alembic

# 数据库连接字符串
sqlalchemy.url = mysql+pymysql://user:password@localhost:3306/dbname

# 也可以使用环境变量
# sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]
# 迁移脚本生成后执行的钩子（如格式化代码）
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -q
```

### 2.3 配置 env.py

修改 `alembic/env.py`，导入你的模型：

```python
# alembic/env.py
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 导入你的 Base 和模型
import sys
sys.path.insert(0, '.')
from models import Base  # 替换为你的模型路径

# this is the Alembic Config object
config = context.config

# 设置 target_metadata 为你的 Base.metadata
target_metadata = Base.metadata

# 其他配置保持不变...
```

### 2.4 常用迁移命令

```bash
# 生成迁移脚本（自动检测模型变化）
alembic revision --autogenerate -m "initial tables"

# 手动创建空白迁移脚本
alembic revision -m "add user table"

# 查看当前数据库版本
alembic current

# 查看迁移历史
alembic history

# 升级到最新版本
alembic upgrade head

# 升级到指定版本
alembic upgrade <revision_id>

# 降级一个版本
alembic downgrade -1

# 降级到指定版本
alembic downgrade <revision_id>

# 降级到初始状态
alembic downgrade base

# 查看将要执行的SQL（不实际执行）
alembic upgrade head --sql

# 标记当前版本（不执行迁移）
alembic stamp head
```

### 2.5 迁移脚本示例

自动生成的迁移脚本示例：

```python
# alembic/versions/123456789abc_initial_tables.py
"""initial tables

Revision ID: 123456789abc
Revises: 
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123456789abc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 创建 users 表
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # 创建索引
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade():
    # 删除索引
    op.drop_index(op.f('ix_users_username'), table_name='users')
    # 删除表
    op.drop_table('users')
```

### 2.6 手动迁移操作

```python
# 添加列
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')

# 删除列
def upgrade():
    op.drop_column('users', 'phone')

# 修改列
def upgrade():
    op.alter_column('users', 'username',
        existing_type=sa.String(50),
        type_=sa.String(100),
        existing_nullable=False
    )

# 添加外键
def upgrade():
    op.create_foreign_key(
        'fk_posts_user_id', 
        'posts', 'users', 
        ['user_id'], ['id']
    )

def downgrade():
    op.drop_constraint('fk_posts_user_id', 'posts', type_='foreignkey')

# 执行原生SQL
def upgrade():
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")

# 批量操作（适合SQLite等不支持某些操作的数据库）
def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(20)))
        batch_op.alter_column('username', type_=sa.String(100))
```

## 三、最佳实践

### 3.1 项目结构推荐

```
project/
├── app/
│   ├── __init__.py
│   ├── database.py      # 数据库连接和Session
│   ├── models/          # 模型定义
│   │   ├── __init__.py
│   │   ├── base.py      # Base定义
│   │   ├── user.py
│   │   └── post.py
│   └── schemas/         # Pydantic 模型
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── ...
├── alembic.ini
└── main.py
```

### 3.2 异步支持

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# 异步操作示例
async def get_users_async():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()
```

### 3.3 迁移注意事项

1. **生产环境谨慎使用 autogenerate**
   - 自动生成可能遗漏某些变更或产生意外的修改
   - 建议人工审核每个迁移脚本

2. **测试迁移的上下兼容性**
   - 确保 downgrade 能正确回滚
   - 在测试环境先验证迁移

3. **大数据表迁移策略**
   - 添加列时使用 `server_default` 避免锁表
   - 考虑分批更新数据

```python
# 安全添加非空列（大数据表）
def upgrade():
    op.add_column('users', sa.Column('status', sa.String(20), server_default='active'))
    # 后续再分批更新后移除默认值
```

## 四、常见问题

### 4.1 迁移版本冲突

当多人开发时可能出现版本冲突：

```bash
# 合并多个头版本
alembic merge -m "merge branches" head1 head2
```

### 4.2 模型导入问题

确保 `env.py` 中正确导入所有模型：

```python
# 方式1：显式导入每个模型
from models import Base, User, Post

# 方式2：在 Base 导入后，导入所有模型模块
from models.base import Base
import models.user  # noqa
import models.post  # noqa
```

### 4.3 SQLite 外键约束

SQLite 默认不启用外键约束，需要在 `env.py` 中配置：

```python
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        # 启用外键约束（SQLite）
        connection.execute(sa.text('PRAGMA foreign_keys=ON'))
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

## 五、参考资源

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Alembic 官方文档](https://alembic.sqlalchemy.org/)
- [FastAPI 与 SQLAlchemy 集成](https://fastapi.tiangolo.com/tutorial/sql-databases/)
