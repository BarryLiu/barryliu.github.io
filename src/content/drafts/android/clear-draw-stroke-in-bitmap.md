---
title: "Android View双缓冲绘制时清除Bitmap上的内容的方法"
date: 2015-07-22
postSlug: "android/clear-draw-stroke-in-bitmap"
categories:
  - Android
tags:
  - Android
description: "Android View双缓冲绘制时清除Bitmap上的内容的方法"
keywords: "Android,双缓冲,Bitmap"
featured: false
draft: true
---

&emsp;&emsp;在做手写的过程中，使用双缓冲可以提高手写的效率，具体做法是将笔迹画在Bitmap上，在onDraw方法中显示Bitmap，而不是直接在onDraw方法中用canvas画。在采用这种机制做手写功能时，可以通过如下方式清除Bitmap上的笔迹内容：
	
	canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR);
