

### 查看系统架构

打开终端，输入 `uname -m` 命令查看系统架构。如果输出是 `x86_64`，表示是 64 位系统；如果输出是 `i386` 或 `i686`，则表示是 32 位系统



### 查看openssl 架构

```plaintext
file /usr/bin/openssl
```

- 输出结果会包含文件的相关信息。如果是 32 位文件，可能会看到类似`ELF 32 - bit LSB executable`的内容；如果是 64 位文件，则可能看到`ELF 64 - bit LSB executable`的内容。

  

```plaintext
ldd /usr/bin/openssl
```

- 查看输出结果中`libc.so`相关的内容。例如，如果看到`/lib/i386 - linux - gnu/libc.so.6`，这通常表示`openssl`是 32 位的，因为它依赖于 32 位的`C`标准库路径；如果看到`/lib/x86_64 - linux - gnu/libc.so.6`，则`openssl`很可能是 64 位的。







``` 

strings /lib/i386-linux-gnu/libc.so.6 | grep GLIBC
```

* 通过  ldd /usr/bin/openssl 命令获取到的libc.so.6文件 ,执行上面命令可以看到 GLIBC对应的版本



i386/python:3.7.13 是 2.31







## 切换openssl版本

* 卸载 

  apt-get remove openssl

* 下载按照

  ``` shell
  
  wget https://github.com/openssl/openssl/releases/download/OpenSSL_1_1_1s/openssl-1.1.1s.tar.gz
  wget https://github.com/openssl/openssl/releases/download/openssl-3.1.2/openssl-3.1.2.tar.gz
  tar -zxvf openssl-1.1.1s.tar.gz
  
  cd openssl-1.1.1s
  
  ./config -m32 shared --prefix=/usr/local/openssl
  make
  sudo make install
  
  export LD_LIBRARY_PATH=/usr/local/openssl/lib:$LD_LIBRARY_PATH
  
  source /etc/profile
  
  openssl version
  
  ```

  



### 安装 glibc2.38 

https://developer.aliyun.com/article/1540422
