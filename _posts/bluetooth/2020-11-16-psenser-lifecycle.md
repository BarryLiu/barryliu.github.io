---
layout: post
title:  耳机入耳检测功能
date:   2020-11-16 14:06:05
categories: C/C++ 
tags: 蓝牙耳机 络达 1562 AB156X 开发板 psensor 入耳检测

---





## PSensor 入耳检测

> 光感   ，主要功能是连接上蓝牙耳机，蓝牙设置中打开入耳检测功能能够判断到耳机带上耳朵,从而实现入耳播放音乐, 出耳暂停播放功能。



>  光感工作中会以肉眼不可见的光闪烁，可以用原相机捕捉拍摄下来，它工作是由内部一边向外发送光,一边接受光，通过反射回来的光线判断是否入耳状态

###  硬件上图

* 安装到耳机位置  

![psensor-all](\images\bluetooth\psensor-all.png)

* 拆解

![psensor-fpc2](\images\bluetooth\psensor-fpc2.png)



* 手机打开设置

  ![psensor-conn](\images\bluetooth\psensor-conn.png)





## 代码及功能实现 

> 光感逻辑:   就是一 AppInEarDetTimerHandler 来循环调用， timer里面以一定的间隔继续调用自己，


####  附上代码

``` c

// App_SmartChgCase.c  # AppInEarDetTimerHandler

U32 AppInEarDetTimerHandler(Handler handler, U16 id, void *msg, U32 handler_id)
{
#if defined(WTK_AN101_BOARD)|| defined(WTK_AN102_BOARD) || defined(WTK_AN100_BOARD) || defined(WTK_AN362_BOARD)
    app_psensor_query();
    FW_SetTimer(&g_AppInEarDetTimerHandle, 0, NULL, 0, PSENSOR_TIMER_DURATION);
#endif
    return 0;
}

```



其中  FW_SetTimer 一直调用自己的实例“ g_AppInEarDetTimerHandle ” 以 PSENSOR_TIMER_DURATION 的时间间隔， 而主要光感工作就在 app_psensor_query 内



#### 主要方法 app_psensor_query

* 判断是否入耳逻辑

* 入耳播放
* 出耳暂停







##### 全局变量

``` c
//当前是否入耳状态
static bool is_in_ear = FALSE;
// gsensor是否使用 
static bool en_gsensor = FALSE;
//入耳计数
static int cus_detect_in_ear_count = 0;
```

> 定义全局变量 cus_detect_in_ear_count,判断入耳一次 则加一, 非入耳减一 ， 以 PSENSOR_TIMER_DURATION (500ms) 的频率判断到 前后3次都是入耳状态,这执行入耳播放事件, 
>
> 如几次都判断为非入耳,直到  cus_detect_in_ear_count 小于0 , 则系统执行出耳暂停事件



##### 判断入耳

> 由于psensor 一次或两次判断到是工作并不能保证真实入耳, 所以真实入耳判断 , 真实入耳会因为各种外界情况影响, 如大多女生耳朵小一点，耳机不能塞进去，头发遮挡......  所以需以多次检测值为准



![psensor-work](\images\bluetooth\psensor-work.png)



##### 入耳播放







##### 出耳暂停