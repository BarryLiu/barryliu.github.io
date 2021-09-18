---
layout: post
title: 简单使用PHP笔记
category: 技术
tags:  php thinkphp composer 
keywords: php thinkphp composer 
description: 简单使用php

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

