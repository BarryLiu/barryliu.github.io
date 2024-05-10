## 192.168.110.218 服务器mysql 备份


> 服务器上mysql数据库没有备份机制, 如果服务器忽然出问题数据不好恢复, 



##### 1. root权限进入服务器备份目录

``` shell
mkdir back
cd back

# 目录路径
/root/back
```



##### 2. 添加数据库脚本(根据日期备份)

> 需要添加重要数据库备份安装脚本规则再添加 
>
> 需要保留固定份数数据后期再调 ~

``` bash
#!/bin/bash
echo "start"
# 生成固定日期
if [ ! -d ./$(date "+%F") ]; then
    mkdir ./$(date "+%F")
fi
mysqldump -uxcheng -pxchengtech bom_auth > ./$(date "+%F")/bom_auth-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech bom_real > ./$(date "+%F")/bom_real-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech mealcpmsdb > ./$(date "+%F")/mealcpmsdb-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech sign_db > ./$(date "+%F")/sign_db-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech xcheng_mrp > ./$(date "+%F")/xcheng_mrp-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech xcheng_pdm > ./$(date "+%F")/xcheng_pdm-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech xcheng_rms > ./$(date "+%F")/xcheng_rms-$(date +%Y%m%d_%H%M%S).sql;
mysqldump -uxcheng -pxchengtech xxl-job > ./$(date "+%F")/xxl-job-$(date +%Y%m%d_%H%M%S).sql;

echo '导出完成!请尽快下载数据异地备份以保安全！'

```



##### 3. 授予执行权限

``` shell
chmod u+x /root/back/backscript.sh
```



##### 4. 执行

``` shell
/root/back/backscript.sh
```

![image-20240201165455903](.\assets\image-20240201165455903.png)



##### 5. 定时执行 

>  工作活儿多， 先干活儿， 后面再调 待续 ~~~



* 使用jenkins执行
  1. 新建自由风格项目

​		![image-20240229173723986](.\assets\image-20240229173723986.png)



 2. 配置自动执行时间与执行脚本

    ![image-20240229175117589](.\assets\image-20240229175117589.png)

	2. 执行任务,完成









##### 6. 异地备份

>  暂时还没找到公司公共文件目录，待续!!!

