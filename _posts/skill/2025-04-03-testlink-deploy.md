# 部署testlink程序



> 测试case辅助应用，php+apache老程序
>
> 程序源码
>
> https://github.com/TestLinkOpenSourceTRMS/testlink-code



参考文档: 

https://cloud.tencent.com/developer/article/1111844

https://blog.csdn.net/zhulianseu/article/details/127792116



修改ldap配置

``` 
$tlCfg->authentication['ldap'] = array();
$tlCfg->authentication['ldap'][1]['ldap_server'] = '192.168.1.191';
$tlCfg->authentication['ldap'][1]['ldap_port'] = '389';
$tlCfg->authentication['ldap'][1]['ldap_version'] = '3'; // could be '2' in some cases
$tlCfg->authentication['ldap'][1]['ldap_root_dn'] = 'DC=xchengtech,DC=com';
$tlCfg->authentication['ldap'][1]['ldap_bind_dn'] = 'CN=scm,CN=Users,DC=xxxx,DC=com'; // Left empty for anonymous LDAP binding  pdm@xchengtech.com
$tlCfg->authentication['ldap'][1]['ldap_bind_passwd'] = 'Aa111111'; // Left empty for anonymous LDAP binding
$tlCfg->authentication['ldap'][1]['ldap_tls'] = false; // true -> use tls



```





* 配置ldap域控有问题

如果公司it有限制，域控ldap一直不通过,可以通过改dns方式



``` shell
# vim /etc/hosts

192.168.1.191   xxxx.com
```





数据库配置好LDAP后