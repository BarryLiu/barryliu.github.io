
## jenkins 获取凭证私钥和密码

Jenkins ==> 系统管理 ==> 脚本命令行

![../../images/skill/jenkins-console.png](jenkins-console.png)

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

