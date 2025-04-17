# ps1脚本转成exe并且注册windows系统服务，



国外查毒网站

 * https://www.virustotal.com/

   > 上传文件上去,用全球很多种(70多个)杀毒软件过一遍，有没有毒查出来



### 准备一个.ps1 脚本





## 1.  .Ps1 脚本进行加密混淆

> 如果外发的脚本不能让别人知道内容,（版权保护需要混淆）(如果不重要脚本可以跳过此步骤)
>
> Invoke-Obfuscation 是交互式操作,需要进去一步步做命令



[参考地址(重要)](https://www.cnblogs.com/henry666/p/17032456.html)

此地址文章说token  all ，全编码encoding 混淆可以过360 查木马报毒,但火绒过不了： https://developer.aliyun.com/article/1215505

``` shell

# github https://github.com/danielbohannon/Invoke-Obfuscation.git
# 安装命令
Install-Module -Name Invoke-Obfuscation

# 查看命令个参数含义
Invoke-Obfuscation -h

# 进入代码加载模块
cd Invoke-Obfuscation
Import-Module .\Invoke-Obfuscation.psd1

# 执行如下命令加载模块进入命令界面,(此时界面展示六种加密方式)
Invoke-Obfuscation

# 设置要操作的脚本
set scriptpath D:\softs\shell2\Monitor-USBDevice1.ps1

# 加密脚本: 选择encoding加密方式(encoding)->随后选择AES算法(5)->再回到主页(back)
encoding
5
back
# 选择混淆：选择string进行字符串混肴(string)-> 有3种加密方式,选第二种(2)
string
2


# 查看加密选项-(可以看到加密前和加密后的脚本内容对比, 以及采用了何种加密方法和完整的加密命令)
show options

# 输出脚本-(如果不填路径地址输出加密后的脚本文件至工具所在目录)
out D:\softs\shell2\Monitor-USBDevice1-after.ps1

# 退出
exit

# 经验证 混淆后脚本取参娶不到(因为$args 被混淆成别的名字了)
```







 





## 2.  ps1脚本转exe

#### 安装

```` shell
#windows进入 powershell执行
# Powershell安装 ps2exe,脚本转exe
#转命令： https://github.com/MScholtes/PS2EXE
Install-Module -Name ps2exe


# 将混淆加密后的脚本打包成exe文件
# 此命令此参数日志输出全藏起来了,打开应用之后在后台偷偷运行,(具体命令安自己需要做)
ps2exe ./tools/Monitor-USBDevice2.ps1 ./tools/XcComTool.exe -title 'Xc串口固定工具' -version '1.0.0.0' -requireAdmin -noConsole -noOutput -noError

# 注意,打包后的exe是可以提取出脚本文件的,所以安全起见混淆一下,提取方式如下,(Output.exe是打包后的exe文件)
Output.exe -extract:C:\Output.ps1

ps2exe ./install_service.ps1 ./install_service.exe -title 'Xc串口安装服务' -version '1.0.0.3' -requireAdmin -noConsole -noOutput -noError

ps2exe ./uninstall_service.ps1 ./uninstall_service.exe -title 'Xc串口卸载服务' -version '1.0.0.3' -requireAdmin -noConsole -noOutput -noError
````

参数含义
-requireAdmin 声明需要管理员权限

-noConsole  不需要打开cmd控制台

-noOutput 不需要输出正常

-noError 不需要输出日志





以上内容根据需要配置，







转成注册表开机启动





## 3. 注册windows服务



> WinSw 工具注册, nssm 注册两种， 



#### **总结：两种方式优缺点**

1. nssm：优点：简单方便，健壮性。缺点第一次使用步骤多
2. WinSW: 优点：简单易操作，快速搭建。缺点：没有可视化界面和其他功能，健壮性不够
3. 推荐使用第一种



参考文档(https://baijiahao.baidu.com/s?id=1819409954321590358&wfr=spider&for=pc)

### nginx 注册



参考nginx的配置 配置普通命令 XcComToolService.xml 配置 

``` xml

<!-- 将exe注册成windows系统服务 -->
<service>    
 <id>nginx</id>    
  <name>nginx</name>    
  <description>nginx</description>    
  <executable>D:\program\nginx-1.8.0\nginx.exe</executable>    
  <logpath>D:\program\nginx-1.8.0\logs\</logpath>    
  <logmode>roll</logmode>    
  <depend></depend>    
  <startargument>-p D:\program\nginx-1.8.0</startargument>    
  <stopargument>-p D:\program\nginx-1.8.0 -s stop</stopargument>    
</service>   
```

或者普通命令

``` xml
<!-- 将XcComToolService.exe注册成windows系统服务 -->
<service>
    <!-- 服务的唯一标识符 -->
    <id>XcComToolService</id>
    <!-- 服务在服务管理器中显示的名称 -->
    <name>XcComToolService</name>
    <!-- 服务的描述信息 -->
    <description>Xc串口工具,固定插入的设备为指定的COM口.</description>
    <!-- 要作为服务运行的可执行文件的完整路径 -->
    <executable>XcComTool.exe</executable>
    <!-- 可选：传递给可执行文件的启动参数,不传默认6,参数范围【3~256】 -->
    <arguments>6</arguments>
    <!-- 服务的工作目录 -->
    <!-- <workingdirectory>C:\Path\To\Your\App</workingdirectory> -->
    <!-- 日志文件的路径 -->
    <logpath>.\logs</logpath>
    <!-- 日志模式，roll 表示滚动日志 -->
    <logmode>roll</logmode>
    <!-- 服务的启动模式，auto 表示开机自启 -->
    <startmode>auto</startmode>
    <!-- 设置服务为延迟启动 -->
    <delayedAutoStart>true</delayedAutoStart>
    <!-- 服务失败时的重启策略 -->
    <onfailure action="restart" delay="10 sec"/>
    <onfailure action="restart" delay="20 sec" count="2"/>
</service>
```





下载 WinSw.exe 改名为 XcComToolService.exe



安装命令: 

``` shell

XcComToolService.exe stop

XcComToolService.exe uninstall

XcComToolService.exe install

XcComToolService.exe start

```



#### 附一下自己调的 winsw.exe管理脚本

> 一下脚本内容

``` bash


@chcp 936 >nul
@echo off
rem 获取当前批处理文件所在的目录
set "currentDir=%~dp0"
rem 进入当前批处理文件所在的目录
cd /d "%currentDir%"
rem 拼接 myapp-service.exe 的完整路径
set "serviceExePath=%currentDir%tools\XcComToolService.exe"

:menu
cls
echo 请选择操作(需要以管理员身份运行):
echo 1. 安装服务
echo 2. 安装服务(并启动)
echo 3. 启动服务
echo 4. 停止服务
echo 5. 卸载服务
echo 6. 查看服务状态
echo 0. 退出
set /p choice=请输入选项编号: 

if "%choice%"=="1" (
    "%serviceExePath%" install
    pause
    goto menu
) else if "%choice%"=="2" (
    "%serviceExePath%" install
    "%serviceExePath%" start
    pause
    goto menu
) else if "%choice%"=="3" (
    "%serviceExePath%" start
    pause
    goto menu
) else if "%choice%"=="4" (
    "%serviceExePath%" stop
    pause
    goto menu
) else if "%choice%"=="5" (
    "%serviceExePath%" uninstall
    pause
    goto menu
) else if "%choice%"=="6" (
    "%serviceExePath%" status
    pause
    goto menu
) else if "%choice%"=="0" (
    exit
) else (
    echo 无效的选项，请重新输入。
    pause
    goto menu
)
```

