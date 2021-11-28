---
layout: post
title: 常用代码片段
category: 技术 
tags:  mysql mybatis springboot
keywords: mysql mybatis springboot 
description: 记录几条经常要用又容易忘记的代码片段


---



### mysql 



* 添加索引

  ``` mysql
  # 添加唯一索引
  alter table t_device_record add UNIQUE uq_fieldid(file_id) 
  
  ```

* 



### mybatis



* 批量插入

  ``` mysql
  
  <insert id="insertBatch"  parameterType="java.util.List" useGeneratedKeys="true" keyProperty="id">
      insert into t_device_record (id, title, user_id)
      values
      <foreach collection="datas" item="item" index="index"  separator=","  >
        (
          #{item.id,jdbcType=BIGINT}, #{item.title,jdbcType=VARCHAR}, #{item.userId,jdbcType=BIGINT}
        )
      </foreach>
    </insert>
  ```

  

* in 查询

  ``` mysql
  <select id="getByFileIds" parameterType="java.util.List" resultMap="BaseResultMap">
      select
      <include refid="Base_Column_List" />
      from t_device_record
      where file_id in  (
        <foreach collection="fileIds" item="fileId" index="index"  separator=","  >
          #{fileId}
        </foreach>
      )
    </select>
  ```

  

* 批量插入或修改 (on duplicate key)

  ``` 
  <insert id="insertBatch"  parameterType="java.util.List" useGeneratedKeys="true" keyProperty="id">
      insert into t_device_record (id, title, user_id)
      values
      <foreach collection="datas" item="item" index="index"  separator=","  >
        (
          #{item.id,jdbcType=BIGINT}, #{item.title,jdbcType=VARCHAR}, #{item.userId,jdbcType=BIGINT}
        )
      </foreach>
      on duplicate key update
      id = VALUES(id),
      title = VALUES(title)
  </insert>
  
  
  ```

  



### java



* stream流获取list中某属性集合

  ``` java
  //获取属性列表
  List<Long> fileIds = items.stream().map(FeedbackAnalyzeItemOutVo::getFileId).collect(Collectors.toList());
  //获取属性列表
  ```

  



