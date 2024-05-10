---
layout: post
title:  idea插件-【Jenkins Control】使用
date:   2024-03-06 15:14:54
categories: java
tags: Intellij Idea jetbrains jenkins 插件


---





#### jenkins

> 在实际开发中，我们经常要一边开发一边测试，当然这里说的测试并不是程序员对自己代码的单元测试，而是同组程序员将代码提交后，由测试人员测试；
>
> 或者前后端分离后，经常会修改接口，然后重新部署；更多的就不在介绍了，好处自然多，但是每次提交代码后还得浏览器登录进去点击构建有点麻烦,
>
> 推荐使用 jenkins control 插件



#### jenkins Control

> 在开发工具idea中,提交代码后通过idea直接调用jenkins部署, 



要使用此插件用主要分为以下步骤，

1. jenkins中生成授权token,

   登录jenkins后,点击用户列表找到需要配置的用户点击进去，到进去后的也找到 API Token， 点击添加新Token，生成的token记得保存

   ![image-20240412151146117](http://img.mrlyj.com/img/image-20240412151146117.png?source=picgo)

   

2. idea下载jenkins control插件,参照下图 点击文件->设置-> 插件-> 搜索jenkins control插件->点击安装

​		![image-20240412151449511](http://img.mrlyj.com/img/image-20240412151449511.png?source=picgo)



3. 配置授权token到插件中

​	安装号后查找到插件设置地方，将jenkins一些必要信息配置好, 测试连接成功后就可以正常使用了

![image-20240412151743687](http://img.mrlyj.com/img/image-20240412151743687.png?source=picgo)



#### 使用

> 安装完成后开发工具 右边会出现jenkins图标, 它可以根据jenkins后台配置好的分类试图展示,
>
> 需要编译哪个直接点 build on jenkins 按钮就行,  编译后控制台可见编译内容输出

![image-20240412151902506](http://img.mrlyj.com/img/image-20240412151902506.png?source=picgo)

![image-20240412152041394](http://img.mrlyj.com/img/image-20240412152041394.png?source=picgo)

