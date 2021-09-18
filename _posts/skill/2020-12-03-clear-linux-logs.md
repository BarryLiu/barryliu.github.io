du -sh * //查看当前文件夹文件大小

df -hl   //查看查看磁盘使用情况





60.205.***.242

``` shell
## 清除tomcat 应用 log
rm -rf /usr/local/tomcat_homework_8080/logs/*.log
echo "" >  /usr/local/tomcat_zookeeper_8011/logs/catalina.out

rm -rf /usr/local/tomcat_hwexam_8605/logs/*.txt
rm -rf /usr/local/tomcat_hwexam_8605/logs/*.log
rm -rf /usr/local/tomcat_zeus_api_8081/logs/*.log

rm -rf /usr/local/tomcat_zeus_console_8082/logs/*.log
rm -rf /usr/local/tomcat_zeus_mq_8084/logs/*.log

## 清除zookeeper log
rm -rf /usr/local/tomcat_zookeeper_8011/logs/*.log

echo "" >  /usr/local/zookeeper-3.4.11/bin/zookeeper.out

## 清除后台程序配置的log目录中log , homework 下和 pay_console log生成比较多,当前目录还有log生成少就不清了 ,里面error的log都没清理
rm -rf /home/logs/homework/all/*.*.log
rm -rf /home/logs/pay_console/all/*.*.log
rm -rf /home/logs/zeus_api/all/*.*.log


```





60.205.***.239

``` shell

rm -rf /home/logs/homework/all/*.*.log
rm -rf /home/logs/ares_versioning/all/*.*.log
rm -rf /home/logs/zeus_api/all/*.*.log

# 清理springboot项目log
echo "" >  /usr/local/apk-manage-jar/out.log

# /usr/local/stem-boot 下面停用了，没有log,不清了

# bom程序
rm -rf /usr/local/tomcat_bom_9090/logs/*.txt
rm -rf /usr/local/tomcat_bom_9090/logs/*.log

# homework  /usr/local/tomcat_homework_8080/backup 9G备份文件不清了
echo "" >  /usr/local/tomcat_homework_8080/logs/catalina.out
rm -rf /usr/local/tomcat_homework_8080/logs/*.log

rm -rf /usr/local/tomcat_hwexam_8605/logs/*.txt
rm -rf /usr/local/tomcat_hwexam_8605/logs/*.log

# tomcat_zeus_api_8081 和 tomcat_zeus_console_8082 tomcat 备份文件多，log不多，不清了

```



