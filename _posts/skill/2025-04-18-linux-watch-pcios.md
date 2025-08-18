## Linux 查看性能命令记录



### 1. `top`

`top` 命令能够实时显示系统中各个进程的资源占用情况，像 CPU、内存等。你可以通过该命令快速找出占用大量资源的进程。

bash



```bash
top
```

在 `top` 界面，按 `q` 键可退出。





### 2. `htop`

`htop` 是 `top` 命令的增强版，提供了更直观、更丰富的交互界面。要是系统中没有安装 `htop`，可以使用包管理器进行安装（如 `apt-get install htop` 或 `yum install htop`）。

bash



```bash
htop
```

同样按 `q` 键可退出 `htop` 界面。







### 3. `vmstat`

`vmstat` 命令用于显示虚拟内存统计信息，包含进程、内存、交换区、IO、CPU 等方面的统计数据。

bash











```bash
vmstat 1 5  # 每隔1秒输出一次，共输出5次
```

### 4. `iostat`

`iostat` 命令主要用于查看磁盘 I/O 性能，能显示磁盘的读写速率、I/O 等待时间等信息。若系统未安装 `iostat`，可使用包管理器安装（如 `apt-get install sysstat`）。

bash











```bash
iostat -x 1 5  # 每隔1秒输出一次扩展的磁盘I/O信息，共输出5次
```

### 5. `netstat`

`netstat` 命令可以查看网络连接、路由表、网络接口统计等信息。

bash











```bash
netstat -tuln  # 显示所有监听的TCP和UDP端口
```

### 6. `ss`

`ss` 是 `netstat` 的替代品，它的速度更快，功能也更强大。

bash











```bash
ss -tuln  # 显示所有监听的TCP和UDP端口
```

### 7. `free`

`free` 命令用于查看系统内存使用情况，包含物理内存、交换内存的使用和空闲情况。

bash











```bash
free -h  # 以人类可读的格式显示内存使用情况
```

### 8. `sar`

`sar` 命令可以收集、报告和保存系统活动信息，涵盖 CPU、内存、磁盘 I/O、网络等多个方面。若系统未安装 `sar`，可使用包管理器安装（如 `apt-get install sysstat`）。

bash











```bash
sar -u 1 5  # 每隔1秒输出一次CPU使用情况，共输出5次
```

这些命令能帮助你全面了解 Linux 系统的性能状况，你可以根据具体需求选择合适的命令。

查看显卡

在 Linux 系统中，有多种命令可以用来查看显卡信息，下面为你详细介绍：

### 9. `lspci`

`lspci` 命令可以列出所有的 PCI 设备，显卡通常也是通过 PCI 总线连接到系统的，所以可以使用这个命令来查看显卡信息。

bash











```bash
lspci | grep -i vga
```

上述命令会筛选出所有与 VGA（视频图形阵列，代表显卡）相关的设备信息。如果想查看更详细的显卡信息，可以使用以下命令：

bash











```bash
lspci -v -s $(lspci | grep -i vga | cut -d " " -f 1)
```

这个命令会先找出 VGA 设备的 PCI 地址，然后显示该设备的详细信息。

### 10. `lshw`

`lshw` 命令可以提供硬件的详细信息，包括显卡。不过使用该命令需要 root 权限。

bash











```bash
sudo lshw -C display
```

该命令会显示显卡的详细信息，如制造商、型号、显存大小等。

### 11. `glxinfo`

`glxinfo` 命令主要用于显示 OpenGL 相关的信息，而 OpenGL 是一种用于渲染 2D、3D 矢量图形的跨语言、跨平台的应用程序编程接口，很多显卡都支持它。使用前需要确保系统已经安装了 `mesa-utils` 包。

bash



```bash
glxinfo | grep "OpenGL renderer"
```





该命令会输出显卡的 OpenGL 渲染器信息，从中可以得知显卡的型号







### 12. `nvidia-smi`（针对 NVIDIA 显卡）

如果你使用的是 NVIDIA 显卡，`nvidia-smi` 是一个非常实用的工具，它可以显示 NVIDIA 显卡的状态信息，如显存使用情况、温度、风扇转速等。

bash



```bash
nvidia-smi
```

 

如果系统提示找不到该命令，说明你可能没有安装 NVIDIA 驱动或驱动版本不支持该命令，需要安装或更新 NVIDIA 驱动。

### 13. `amdgpu-pro-clock`（针对 AMD 显卡）

对于 AMD 显卡，可以使用 `amdgpu-pro-clock` 命令来查看显卡的时钟频率等信息。不过这个命令需要安装 AMD 显卡驱动才能使用。

bash



```bash
amdgpu-pro-clock
```





通过这些命令，你可以全面了解显卡的型号、性能等相关信息。