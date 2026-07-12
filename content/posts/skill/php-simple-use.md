---
title: "简单使用PHP笔记"
date: 2021-08-23
postSlug: "skill/php-simple-use"
categories:
  - "技术"
tags:
  - php
  - thinkphp
  - composer
description: "简单使用php"
keywords: "php thinkphp composer"
featured: false
---

### 安装环境
### 创建thinkphp项目
> composer create-project topthink/think tp6
#### 引入视图模板引型
> 进入项目目录执行：
>
>  composer require topthink/think-view
assign  全局变量赋值
```
xxx.php
View::assign("name","张三");//传值到前端
xxx.html
获取后端传值: {$name}
```
