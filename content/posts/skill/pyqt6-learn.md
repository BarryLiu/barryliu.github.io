---
title: "PyQt6 环境配置与 PyCharm 集成"
date: 2025-04-07
postSlug: "skill/pyqt6-learn"
categories:
  - "技术"
tags:
  - PyQt6
  - Python
  - GUI
  - PyCharm
description: "PyQt6/PyQt5 在 PyCharm 中的环境配置，包括 Designer 和 pyuic 工具集成"
keywords: "PyQt6, PyQt5, PyCharm, Designer, pyuic"
featured: false
---

![image-20250407174600656](/posts-assets/skill/assets/image-20250407174600656.png)
## 配置环境
> pip安装好pyqt5或pyqt6后
>
> pycharm进入设置->外部工具->点击添加
### PyCharm 配置 Designer
> 选择程序: `D:\softs\python3.13.0_32bit\Lib\site-packages\qt5_applications\Qt\bin\designer.exe`
>
> 实参：`$FileName$`
>
> 工作目录: `$ProjectFileDir$`
### PyCharm 配置 pyuic
> 选择程序: `E:\codetest\python\PyQtTest1\venv\Scripts\python.exe`
>
> 实参：`-m PyQt6.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py`
>
> 工作目录: `$FileDir$`
