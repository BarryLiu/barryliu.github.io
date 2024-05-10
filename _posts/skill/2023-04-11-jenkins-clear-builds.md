



> jenkins使用了很久,硬盘不够用,清理jenkins编译记录



找到服务器上生成记录（.jenkins > jobs 目录下的内容）



![image-20230411170504330](.\assets\image-20230411170504330.png)





1. jenkins后台执行jenkins脚本删除

[参考文档1](https://blog.csdn.net/mp624183768/article/details/108515183)

登录[Jenkins](https://so.csdn.net/so/search?q=Jenkins&spm=1001.2101.3001.7020) -> Manage Jenkins -> Script Console(脚本命令行)执行如下命令

登录后->系统管理->脚本命令行 > 执行脚本 

``` shell

import hudson.tasks.LogRotator
Jenkins.instance.allItems(Job).each { job ->
  println "$job.builds.number $job.name"
  if ( job.isBuildable() && job.supportsLogRotator()) {
    // 注释if所有任务统一设置策略，去掉注释后只更改没有配置策略的任务
    //if ( job.getProperty(BuildDiscarderProperty) == null) {
      job.setLogRotator(new LogRotator (60, 30, 30, 3))
    //}
      job.logRotate() //立马执行Rotate策略
    println "$job.builds.number $job.name 磁盘回收已处理"
  } else { println "$job.name 未修改，已跳过" }
}
return;

```

 

解释说明
LogRotator构造参数分别为：

- daysToKeep: 构建记录将保存的天数
- numToKeep: 最多此数目的构建记录将被保存
- artifactDaysToKeep: 比此早的发布包将被删除，但构建的日志、操作历史、报告等将被保留
- artifactNumToKeep: 最多此数目的构建将保留他们的发布包





![image-20230411165745546](.\assets\image-20230411165745546.png)







2 . 或者使用 指定项目保留几份项目

[参考文档](https://blog.csdn.net/weixin_44024740/article/details/122698707)

``` 

def jobName = "test"   //删除的项目名称
def maxNumber = 65    // 保留的最小编号，意味着小于该编号的构建都将被删除

Jenkins.instance.getItemByFullName(jobName).builds.findAll {
  it.number <= maxNumber
}.each {
  it.delete()
}
```





