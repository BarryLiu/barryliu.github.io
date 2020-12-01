---
layout: post
title:  耳机各功能装换
date:   2020-11-30 14:06:05
categories: C/C++ 嵌入式
tags: 蓝牙耳机 络达 1562 AB156X 开发板 状态改变
---







# 耳机与充电盒状态保持Log



## app_SmtChgCse_StateHandler 

> 耳机与耳机盒状态改变回调handler
>
> 位置： App_SmartChgCase.c # app_SmtChgCse_StateHandler 
>
> 功能：注册给系统，由系统维护耳机与耳机盒直接的关系状态变化后回调这里，这里执行自己需要的业务功能
>
> 



#### 耳机之间各功能状态变化

>  耳机盒充电盒之间状态由耳机内络达提供的库里面自己维护, 一共有四种状态。通过自己注册事件给络达提供的库，各个状态变化后由它回调通知应用层。



![bluetooth-status](\images\bluetooth\bluetooth-status.png)



#### 状态介绍

* SMART_CASE_OFF_IND                     0  充满电  耳机在仓内，充电仓通知耳机要断电啦
* SMART_CASE_OUT_OF_CASE_IND  1  出仓  耳机在仓外
* SMART_CASE_LID_CLOSE_IND        2  关仓  耳机在仓内
* SMART_CASE_LID_OPEN_IND         3  开仓  耳机在仓内



#### 调用代码：

1. 编写自定义业务： (App_SmartChgCase.c 文件里面)

   

![bluetooth-status-code0](\images\bluetooth\bluetooth-status-code0.png)



2. 创建对象

   ![bluetooth-status-code1](\images\bluetooth\bluetooth-status-code1.png)



3. 传递给络达库调用 ，(App_ChargeBattery.c)

   ![bluetooth-status-code2](\images\bluetooth\bluetooth-status-code2.png)



### 调用log

>    App_SmartChgCase.c # app_SmtChgCse_SetChargeIn(): 入仓事件  销毁sensor
>
>   App_SmartChgCase.c # app_SmtChgCse_SetChargeOut(): 出仓事件 初始化sensor
>
>   App_SmartChgCase.c # app_SmtChgCse_LidOpen() : 开盖函数,(开盖由状态改变的回调中调用里面逻辑,所以在状态改变之后)
>
>   

*  从关盖状态到开仓取出耳机

![bluetooth-status-log1](\images\bluetooth\bluetooth-status-log1.png)

> 如果将开仓事件的log加到一起：
>

 ![bluetooth-status-log3](\images\bluetooth\bluetooth-status-log3.png)

* 从耳机到仓外放入耳机并合盖

![bluetooth-status-log2](\images\bluetooth\bluetooth-status-log2.png)

> 关盖log也一样，先调用 入仓事件销毁sensor,再进入这里回调状态改变



> 







----



## app_charger_Handler

> 与 app_SmtChgCse_StateHandler 一样，注册到络达库里面，由系统调用
>
> 



### 状态介绍

​	CHARGER_CHARGER_OUT_IND                 出仓  判断到出仓后调用上面ChargeOut 事件        CHARGER_CHARGING_IND    	                 入仓 判断到入仓后调用上面ChargeIn 事件
​    CHARGER_CHARGER_COMPLETE_IND     充满电（）