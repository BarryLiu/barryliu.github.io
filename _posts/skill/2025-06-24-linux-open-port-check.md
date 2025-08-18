# 记录测试服务器开端口成功与否验证



> 服务器在it运维部门那边管控, 申请开通后，发现搭的程序不能访问，快速验证端口是否开放





#### 普通局域网服务器

> 普通服务器到局域网it一般不设限制，直接能访问, 自己有ssh权限可自行开端口，有下面两种做法



* 关闭防火墙

  >  关闭后整个服务器没有防火墙，任意启动的软件使用的端口都暴露出来，广域网不安全，局域网相对安全（局域网基本就那么几十几百人，没人特意扫你这个软件端口破解,别人电脑被黑除外），

* 防火墙开放端口

  > 开启着防火墙，需要某些端口对外开放，开放端口，程序能够被访问



#### 云服务器

> 对于到外面买的云服务器（例如阿里云，百度云，腾讯云，华为云等），除了程序需要开端口，云服务器上也要开端口，都开放了之后程序方可访问







#### 开启后快速测试

> 网上有找一些网络命令，感觉都不是很明确, 最直接的是直接起一个服务并客户端去访问，能通表示可以了， 起一个服务需要编写复杂程序，
>
> 下面快速启动简单程序测试



* tcp

  ``` shell
  # linux 基本都有python，直接python启动一个端口， 外面访问
  python3 -m http.server [具体端口] 
  eg: python3 -m http.server 8000
  
  # 验证
  curl http://ip:端口
  # 或着浏览器访问验证
  
  ```

  

* udp

  > udp的协议是没有tcp那种三次握手，简单写个服务，客户端发送消息看服务器输出方式查看

  ``` python
  # 新建udpserver.py 文件
  import socket
  
  UDP_IP = "0.0.0.0"
  UDP_PORT = 23456  #端口改为具体先要的端口
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((UDP_IP, UDP_PORT))
  
  print(f"Listening on UDP port {UDP_PORT}...")
  
  while True:
      data, addr = sock.recvfrom(1024)  # 缓冲区大小
      print(f"Received message: {data} from {addr}")
  
  
  ```

  验证

  ``` shell
  # linux上执行此命令发送数据后查看服务器日志输出
  
   echo "Hello, UDP!" | nc -uvz 47.xx.xxx.104 23456
  ```

  