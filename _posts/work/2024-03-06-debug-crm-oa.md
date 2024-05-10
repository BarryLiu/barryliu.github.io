---
layout: post
title:  调试泛微OA系统接口记录
date:   2024-03-06 15:14:54
categories: java
tags: 泛微OA 低代码 CRM

---







##  记录调试泛微OA系统

> 泛微OA是一种企业级办公自动化解决方案，旨在帮助组织提高工作效率、加强协作、优化业务流程。该系统通过集成各种功能和工具，提供了一套全面的办公自动化解决方案,，方便企业中更好的运行管理等操作， 但是公司不会只使用一套系统, 会有很多一些自主研发的系统需要接入泛微OA系统的情况, 下面记录一下开发调试泛微OA系统具体记录



![image-20240306194054413](http://img.mrlyj.com/img/image-20240306194054413.png?source=picgo)



#### 在固定的类型下新建接口

> 注意，接口授权 里面添加用户, 然后选择具体权限,



![image-20240306195302304](http://img.mrlyj.com/img/image-20240306195302304.png?source=picgo)



#### 可在此处查看数据

![image-20240306213937860](http://img.mrlyj.com/img/image-20240306213937860.png?source=picgo)



#### 接口调用

>  泛微后台的文档中会给出详细的各个语言代码下接口调用demo出来，但是里面的demo代码有点冗长，多个接口请求下来代码量上去了，无形中增加了许多维护成本, 下面是根据demo中的逻辑，使用hutool工具封装查询请求



* 发送通用调用请求

  > 账号密码由上图中 【建模引型 】 --> 【接口管理】--> 【Restful接口】--> 【接口授权】 中获得

  ``` java
  	
  	public static String systemid = "xxxx";//账号-系统标识(账号和密码在正式环境和测试环境都是一样)
      public static String d_password = "xxxx@!";//密码
      public static final String url = "http://oa.xxxx.com:xx";// 正式环境客户地址
  
  	/***
       * 调用OA系统分页接口
       * @param url
       * @param pageNo
       * @param pageSize
       * @param mainTable
       * @return
       */
      private List<JSONObject> requestStrPage(String url,Integer pageNo ,Integer pageSize, JSONObject mainTable) {
  
          pageNo = pageNo == null? 1 :pageNo;
          pageSize = pageSize == null ? 10 : pageSize;
  
          String rst = request(url, pageNo, pageSize, mainTable);
  
          JSONObject rstObj = JSONUtil.parseObj(rst);
          String resultStr =  rstObj.getStr("result");
          JSONArray resultArr = JSONUtil.parseArray(resultStr);
  
          List<JSONObject> datas = new ArrayList();
          for (int i = 0; i < resultArr.size(); i++) {
              JSONObject data = resultArr.getJSONObject(i);
              JSONObject t =   data.getBean("mainTable",JSONObject.class);
              datas.add(t);
          }
  
          return datas;
      }
  
  	/**
       * 获取当前日期时间。 YYYY-MM-DD HH:MM:SS
       * @return		当前日期时间
       */
      public static String getCurDateTime() {
          Date newdate = new Date();
          long datetime = newdate.getTime();
          Timestamp timestamp = new Timestamp(datetime);
          return (timestamp.toString()).substring(0, 19);
      }
  
      /**
       * 获取时间戳   格式如：19990101235959
       * @return
       */
      public static String getTimestamp(){
          return getCurDateTime().replace("-", "").replace(":", "").replace(" ", "");
      }
  
  
  	public static String getMD5Str(String plainText){
          //定义一个字节数组
          byte[] secretBytes = null;
          try {
              // 生成一个MD5加密计算摘要
              MessageDigest md = MessageDigest.getInstance("MD5");
              //对字符串进行加密
              md.update(plainText.getBytes());
              //获得加密后的数据
              secretBytes = md.digest();
          } catch (NoSuchAlgorithmException e) {
              //throw new RuntimeException("没有md5这个算法！");
              //throw new RuntimeException(SystemEnv.getHtmlLabelName(517545,userLanguage));
              e.printStackTrace();
              throw new ServiceException("出异常了");
          }
          //将加密后的数据转换为16进制数字
          String md5code = new BigInteger(1, secretBytes).toString(16);
          // 如果生成数字未满32位，需要前面补0
          // 不能把变量放到循环条件，值改变之后会导致条件变化。如果生成30位 只能生成31位md5
          int tempIndex = 32 - md5code.length();
          for (int i = 0; i < tempIndex; i++) {
              md5code = "0" + md5code;
          }
          return md5code;
      }
  
  ```

  

* 具体业务调用代码

  

  ``` java
  
  
  	public static void main(String[] args) {
  		
          //调用
          OaUtil util = new OaUtil();
          util.requestProjects();
      }
  
  
  
  	/**
       * OAtest 测试环境调通
       * 获取表单数据列表(分页)-> 项目信息库 模块 -> 添加(	xchub_project) 接口标识
       * @return
       */
      public List<XPdmInfo> requestProjects() {
          Date curdate = new Date();
          //封装mainTable参数
          JSONObject mainTable = new JSONObject();
          List<JSONObject> resultObjs = requestStrPage(url+"/api/cube/restful/interface/getModeDataPageList/xchub_project",1,10000,mainTable);
  
          List<XPdmInfo> datas = new ArrayList<>();
          for (JSONObject obj : resultObjs) {
  
              XPdmInfo data = new XPdmInfo();
              data.setId(obj.getLong("id").toString());
              data.setName(obj.getStr("xmmc"));       //项目代号
              data.setProductLine(obj.getStr("cpxl"));//cpxl  产品系列 //返回值类型(按名称)
              data.setPlatform(obj.getStr("cppt"));   //cppt 产品平台
              data.setWholeMachinePartNumber(null);       //整机料号
  
              data.setLastSyncTime(curdate);  //最后同步时间
              datas.add(data);
          }
  
          return datas;
      }
  
  ```

  