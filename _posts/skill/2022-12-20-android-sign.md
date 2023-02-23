---
layout: post
title: 实现android或jar包签名
category: 工具
tags:  java android
keywords: java Android 签名 jarsigner keytool  signapk.jar
description: android studio自带有签名工具, 抛开使用自动工具,命令行以及java后台实现签名apk


---

### 



#### 涉及工具

> jarsigner keytool  signapk.jar  jarsigner



#### signapk.jar 签名

``` powershell
 # 
 java -jar signapk.jar xxx.pem xxx.pk8 app.apk app_signed.apk
 
 
 
```





#### 生成签名

``` powershell
# 生成签名,生成好的签名文件保存在目录 mykey.keystore
keytool -genkey -alias isaalias -keyalg RSA -validity 20 -keystore mykey.keystore

#或
keytool -genkey -dname cn=foo,ou=bar,o=company,c=CH -alias myProduct -keypass testtest -storepass testtest -validity 10 -keystore mykey.keystore

# 给apk签名
jarsigner -keystore mykey.keystore CpuDeviceInfo.apk isaalias



```

