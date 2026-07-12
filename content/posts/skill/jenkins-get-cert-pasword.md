---
title: "jenkins 获取凭证私钥和密码"
date: 2024-10-31
postSlug: "skill/jenkins-get-cert-pasword"
categories:
  - skill
tags: []
description: "Jenkins ==> 系统管理 ==> 脚本命令行"
featured: false
---

## jenkins 获取凭证私钥和密码

Jenkins ==> 系统管理 ==> 脚本命令行

![jenkins-console](/posts-assets/skill/assets/jenkins-console.png)

输入下面命令

```java
com.cloudbees.plugins.credentials.SystemCredentialsProvider.getInstance().getCredentials().forEach{
    it.properties.each { prop, val ->
          println(prop + ' = "' + val + '"')
        }
    println("-----------------------")
  }


```

点运行 OK
