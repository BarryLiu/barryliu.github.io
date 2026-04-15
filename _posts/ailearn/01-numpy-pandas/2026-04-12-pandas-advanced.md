---
layout: post
title: "Pandas 进阶教程 - 数据处理与分组聚合"
date: 2026-04-12
categories: ailearn
tags: [AI, Python, Pandas, 数据处理]
keywords: Pandas, groupby, 数据合并, 数据透视表, 时间序列
description: 深入学习 Pandas 数据处理技术，掌握分组聚合、数据合并、透视表等高级操作
---

* content
{:toc}

> **前置知识**：需要先掌握 [Pandas 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-basic %})。
>
> **本文重点**：分组聚合、数据合并、透视表、时间序列处理。

本文深入讲解 Pandas 的高级数据处理技术，这些是数据分析和机器学习数据预处理的必备技能。

---

## 一、分组聚合 (GroupBy)

### 1.1 基本分组操作

```python
import pandas as pd
import numpy as np

# 创建示例数据
df = pd.DataFrame({
    'department': ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance', 'IT'],
    'employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry'],
    'salary': [12000, 8000, 15000, 13000, 9000, 11000, 14000, 16000],
    'experience': [5, 3, 7, 6, 2, 4, 8, 9],
    'performance': ['A', 'B', 'A', 'A', 'C', 'B', 'A', 'A']
})

print("原始数据:")
print(df)

# 按 department 分组
grouped = df.groupby('department')
print(f"\n分组对象: {grouped}")
print(f"分组大小:\n{grouped.size()}")

# 单列聚合
print(f"\n各部门平均薪资:\n{grouped['salary'].mean()}")
print(f"\n各部门总薪资:\n{grouped['salary'].sum()}")

# 多列聚合
print(f"\n各部门薪资和经验统计:\n{grouped[['salary', 'experience']].mean()}")
```

### 1.2 聚合函数

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'value1': [10, 20, 30, 40, 50, 60],
    'value2': [1, 2, 3, 4, 5, 6]
})

# 内置聚合函数
grouped = df.groupby('category')

print("求和:\n", grouped.sum())
print("\n均值:\n", grouped.mean())
print("\n计数:\n", grouped.count())      # 非缺失值数量
print("\n大小:\n", grouped.size())       # 每组行数
print("\n标准差:\n", grouped.std())
print("\n方差:\n", grouped.var())
print("\n最小值:\n", grouped.min())
print("\n最大值:\n", grouped.max())
print("\n中位数:\n", grouped.median())
print("\n第一个值:\n", grouped.first())
print("\n最后一个值:\n", grouped.last())

# 使用 agg 方法
print("\n自定义聚合:\n", grouped['value1'].agg(['sum', 'mean', 'std']))

# 多列不同聚合
result = grouped.agg({
    'value1': ['sum', 'mean'],
    'value2': ['min', 'max']
})
print("\n多列不同聚合:\n", result)
```

### 1.3 自定义聚合函数

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B', 'B', 'C'],
    'value': [10, 20, 30, 40, 50, 60]
})

grouped = df.groupby('group')

# 自定义函数
def range_func(x):
    return x.max() - x.min()

def cv_func(x):  # 变异系数
    return x.std() / x.mean() if x.mean() != 0 else 0

# 使用 agg
print("范围:\n", grouped['value'].agg(range_func))
print("\n变异系数:\n", grouped['value'].agg(cv_func))

# 多个自定义函数
result = grouped['value'].agg([
    ('总和', 'sum'),
    ('均值', 'mean'),
    ('范围', range_func),
    ('变异系数', cv_func)
])
print("\n多函数聚合:\n", result)

# 使用 lambda
print("\n每组的第90百分位数:")
print(grouped['value'].agg(lambda x: np.percentile(x, 90)))
```

### 1.4 多级分组

```python
import pandas as pd
import numpy as np

# 创建多级分组数据
df = pd.DataFrame({
    'year': [2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023],
    'quarter': ['Q1', 'Q1', 'Q2', 'Q2', 'Q1', 'Q1', 'Q2', 'Q2'],
    'region': ['North', 'South', 'North', 'South', 'North', 'South', 'North', 'South'],
    'sales': [100, 150, 120, 180, 110, 160, 130, 190],
    'profit': [20, 30, 25, 35, 22, 32, 27, 38]
})

print("原始数据:")
print(df)

# 多级分组
grouped = df.groupby(['year', 'quarter'])
print("\n年季度分组求和:\n", grouped[['sales', 'profit']].sum())

# 三级分组
grouped_3 = df.groupby(['year', 'quarter', 'region'])
print("\n三级分组:\n", grouped_3['sales'].sum())

# 按层级聚合
year_group = df.groupby('year')
print("\n按年聚合:\n", year_group[['sales', 'profit']].sum())

# 使用 level 参数
multi_index_df = df.set_index(['year', 'quarter'])
print("\n按索引层级聚合:\n", multi_index_df.groupby(level=0)['sales'].sum())
```

### 1.5 分组变换与过滤

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B', 'B', 'C'],
    'value': [10, 20, 30, 40, 50, 60]
})

# ===== transform - 返回与原数据相同形状 =====
# 标准化（组内Z-score）
df['zscore'] = df.groupby('group')['value'].transform(lambda x: (x - x.mean()) / x.std())
print("组内标准化:\n", df)

# 组内填充缺失值
df_nan = df.copy()
df_nan.loc[1, 'value'] = np.nan
df_nan['value_filled'] = df_nan.groupby('group')['value'].transform(
    lambda x: x.fillna(x.mean())
)
print("\n组内填充:\n", df_nan)

# 组内排名
df['rank'] = df.groupby('group')['value'].rank(method='dense')
print("\n组内排名:\n", df)

# ===== filter - 过滤组 =====
# 只保留元素数>=2的组
filtered = df.groupby('group').filter(lambda x: len(x) >= 2)
print("\n过滤后:\n", filtered)

# 只保留均值>30的组
filtered_mean = df.groupby('group').filter(lambda x: x['value'].mean() > 30)
print("\n均值过滤:\n", filtered_mean)

# ===== apply - 任意变换 =====
# 对每组应用函数
def top_n(df, n=2):
    return df.nlargest(n, 'value')

top2_per_group = df.groupby('group').apply(top_n, n=2)
print("\n每组最大的2个:\n", top2_per_group)
```

---

## 二、数据合并

### 2.1 concat - 拼接

```python
import pandas as pd
import numpy as np

# 创建示例数据
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
df3 = pd.DataFrame({'C': [9, 10], 'D': [11, 12]})

# 垂直拼接（默认）
result = pd.concat([df1, df2])
print("垂直拼接:\n", result)
#    A  B
# 0 1  3
# 1 2  4
# 0 5  7
# 1 6  8

# 重置索引
result = pd.concat([df1, df2], ignore_index=True)
print("\n重置索引:\n", result)

# 水平拼接
result = pd.concat([df1, df3], axis=1)
print("\n水平拼接:\n", result)

# 内连接（只保留共有列）
df4 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df5 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
result = pd.concat([df4, df5], join='inner')
print("\n内连接:\n", result)

# 添加键标识来源
result = pd.concat([df1, df2], keys=['df1', 'df2'])
print("\n带来源标签:\n", result)

# 追加数据（append已弃用，使用concat）
# 旧写法: df1.append(df2)
# 新写法:
result = pd.concat([df1, df2], ignore_index=True)
```

### 2.2 merge - 数据库风格连接

```python
import pandas as pd

# 创建示例数据
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'dept_id': [101, 102, 101, 103, 102]
})

departments = pd.DataFrame({
    'dept_id': [101, 102, 104],
    'dept_name': ['IT', 'HR', 'Finance']
})

print("员工表:\n", employees)
print("\n部门表:\n", departments)

# 内连接（默认）
result = pd.merge(employees, departments, on='dept_id', how='inner')
print("\n内连接:\n", result)

# 左连接
result = pd.merge(employees, departments, on='dept_id', how='left')
print("\n左连接:\n", result)

# 右连接
result = pd.merge(employees, departments, on='dept_id', how='right')
print("\n右连接:\n", result)

# 外连接
result = pd.merge(employees, departments, on='dept_id', how='outer')
print("\n外连接:\n", result)

# 不同列名连接
employees2 = employees.rename(columns={'dept_id': 'department_id'})
departments2 = departments.rename(columns={'dept_id': 'department_id'})
result = pd.merge(employees2, departments2, 
                  left_on='department_id', right_on='department_id')
print("\n不同列名连接:\n", result)

# 多列连接
sales = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'year': [2023, 2023, 2023],
    'sales': [100, 150, 120]
})
targets = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'year': [2023, 2023, 2023],
    'target': [90, 140, 130]
})
result = pd.merge(sales, targets, on=['emp_id', 'year'])
print("\n多列连接:\n", result)

# 后缀处理重复列名
result = pd.merge(sales, targets, on='emp_id', suffixes=('_actual', '_target'))
print("\n后缀处理:\n", result)
```

### 2.3 join - 索引连接

```python
import pandas as pd

# 基于索引的连接
df1 = pd.DataFrame({'A': [1, 2, 3]}, index=['a', 'b', 'c'])
df2 = pd.DataFrame({'B': [4, 5, 6]}, index=['a', 'b', 'd'])

# 默认左连接
result = df1.join(df2)
print("左连接:\n", result)

# 其他连接方式
result = df1.join(df2, how='inner')
print("\n内连接:\n", result)

result = df1.join(df2, how='outer')
print("\n外连接:\n", result)

# 多个DataFrame连接
df3 = pd.DataFrame({'C': [7, 8, 9]}, index=['a', 'b', 'c'])
result = df1.join([df2, df3])
print("\n多表连接:\n", result)

# 指定列连接
df4 = pd.DataFrame({'A': [1, 2], 'key': ['a', 'b']})
df5 = pd.DataFrame({'B': [3, 4]}, index=['a', 'b'])
result = df4.set_index('key').join(df5)
print("\n指定key列连接:\n", result)
```

### 2.4 合并实践案例

```python
import pandas as pd
import numpy as np

# 模拟电商订单数据
orders = pd.DataFrame({
    'order_id': range(1, 8),
    'customer_id': [1, 2, 1, 3, 2, 4, 5],
    'product_id': [101, 102, 103, 101, 104, 102, 101],
    'quantity': [2, 1, 3, 1, 2, 1, 5],
    'order_date': pd.date_range('2023-01-01', periods=7)
})

customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
})

products = pd.DataFrame({
    'product_id': [101, 102, 103, 104],
    'product_name': ['Laptop', 'Phone', 'Tablet', 'Watch'],
    'price': [8000, 5000, 3000, 2000]
})

print("订单表:\n", orders)
print("\n客户表:\n", customers)
print("\n产品表:\n", products)

# 合并订单与客户
order_customer = pd.merge(orders, customers, on='customer_id', how='left')
print("\n订单+客户:\n", order_customer)

# 再合并产品
full_data = pd.merge(order_customer, products, on='product_id', how='left')
print("\n完整数据:\n", full_data)

# 计算订单金额
full_data['amount'] = full_data['quantity'] * full_data['price']
print("\n带金额数据:\n", full_data)

# 分析：各城市销售总额
city_sales = full_data.groupby('city')['amount'].sum().sort_values(ascending=False)
print("\n各城市销售额:\n", city_sales)
```

---

## 三、数据透视表

### 3.1 pivot_table

```python
import pandas as pd
import numpy as np

# 创建销售数据
df = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=12),
    'region': ['North', 'South', 'East', 'West'] * 3,
    'product': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
    'sales': [100, 150, 120, 180, 110, 160, 130, 190, 105, 155, 125, 185],
    'quantity': [10, 15, 12, 18, 11, 16, 13, 19, 10, 15, 12, 18]
})

print("原始数据:")
print(df)

# 基本透视表
pivot = df.pivot_table(values='sales', index='region', columns='product', aggfunc='sum')
print("\n基本透视表:\n", pivot)

# 多个聚合函数
pivot_multi = df.pivot_table(
    values='sales', 
    index='region', 
    columns='product', 
    aggfunc=['sum', 'mean', 'count']
)
print("\n多聚合函数:\n", pivot_multi)

# 多个值列
pivot_multi_values = df.pivot_table(
    values=['sales', 'quantity'],
    index='region',
    columns='product',
    aggfunc='sum'
)
print("\n多值列:\n", pivot_multi_values)

# 添加小计
pivot_margins = df.pivot_table(
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum',
    margins=True,
    margins_name='总计'
)
print("\n带小计:\n", pivot_margins)

# 处理缺失值
pivot_filled = df.pivot_table(
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum',
    fill_value=0
)
print("\n填充缺失值:\n", pivot_filled)
```

### 3.2 pivot 与 melt

```python
import pandas as pd

# pivot - 长变宽（需要唯一索引组合）
df_long = pd.DataFrame({
    'date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
    'city': ['Beijing', 'Shanghai', 'Beijing', 'Shanghai'],
    'temp': [5, 10, 6, 12]
})

# 长格式转宽格式
df_wide = df_long.pivot(index='date', columns='city', values='temp')
print("宽格式:\n", df_wide)

# melt - 宽变长
df_wide_reset = df_wide.reset_index()
df_melted = df_wide_reset.melt(
    id_vars=['date'],
    value_vars=['Beijing', 'Shanghai'],
    var_name='city',
    value_name='temperature'
)
print("\nmelt转长格式:\n", df_melted)

# 更复杂的melt
df_complex = pd.DataFrame({
    'student': ['Alice', 'Bob'],
    'math': [90, 85],
    'english': [88, 92],
    'science': [95, 80]
})
print("\n原始成绩表:\n", df_complex)

melted = df_complex.melt(
    id_vars=['student'],
    value_vars=['math', 'english', 'science'],
    var_name='subject',
    value_name='score'
)
print("\nmelt后:\n", melted)

# 使用 pivot_table 后再 melt 回去
summary = melted.groupby('subject')['score'].mean().reset_index()
print("\n各科平均分:\n", summary)
```

### 3.3 交叉表 crosstab

```python
import pandas as pd
import numpy as np

# 创建示例数据
df = pd.DataFrame({
    'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'age_group': ['young', 'young', 'middle', 'middle', 'old', 'old', 'young', 'middle'],
    'purchase': ['yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes']
})

print("原始数据:")
print(df)

# 基本交叉表
cross = pd.crosstab(df['gender'], df['purchase'])
print("\n基本交叉表:\n", cross)

# 归一化
cross_norm = pd.crosstab(df['gender'], df['purchase'], normalize='index')
print("\n按行归一化:\n", cross_norm)

cross_norm_col = pd.crosstab(df['gender'], df['purchase'], normalize='columns')
print("\n按列归一化:\n", cross_norm_col)

cross_norm_all = pd.crosstab(df['gender'], df['purchase'], normalize='all')
print("\n全局归一化:\n", cross_norm_all)

# 多级交叉表
cross_multi = pd.crosstab([df['gender'], df['age_group']], df['purchase'])
print("\n多级交叉表:\n", cross_multi)

# 添加小计
cross_margins = pd.crosstab(df['gender'], df['purchase'], margins=True)
print("\n带小计:\n", cross_margins)
```

---

## 四、时间序列处理

### 4.1 时间序列基础

```python
import pandas as pd
import numpy as np

# 创建时间序列
dates = pd.date_range('2023-01-01', periods=10, freq='D')
print("日期序列:\n", dates)

ts = pd.Series(np.random.randn(10), index=dates)
print("\n时间序列:\n", ts)

# 不同的频率
print("\n小时频率:", pd.date_range('2023-01-01', periods=5, freq='H'))
print("月频率:", pd.date_range('2023-01-01', periods=5, freq='M'))
print("年频率:", pd.date_range('2023-01-01', periods=5, freq='Y'))
print("工作日:", pd.date_range('2023-01-01', periods=5, freq='B'))

# 时间戳转周期
periods = dates.to_period('M')
print("\n月周期:\n", periods)

# 常用频率别名
# D - 日, B - 工作日, W - 周
# M - 月末, MS - 月初
# Q - 季末, QS - 季初
# A/Y - 年末, AS/YS - 年初
# H - 小时, T/min - 分钟, S - 秒
```

### 4.2 时间序列索引与切片

```python
import pandas as pd
import numpy as np

# 创建时间序列数据
dates = pd.date_range('2023-01-01', periods=365, freq='D')
ts = pd.Series(np.random.randn(365), index=dates)
ts.name = 'value'

# 精确索引
print("特定日期:", ts['2023-01-05'])

# 字符串切片
print("\n1月数据:\n", ts['2023-01'].head())
print("\n1-2月数据:\n", ts['2023-01':'2023-02'].head())

# 部分日期索引
print("\n2023年数据量:", len(ts['2023']))

# 使用 truncate
print("\n截取到3月:", ts.truncate(after='2023-03-01').tail())

# 获取特定时间
ts_hourly = pd.Series(
    np.random.randn(48),
    index=pd.date_range('2023-01-01', periods=48, freq='H')
)
print("\n上午数据:\n", ts_hourly.at_time('09:00'))
print("\n两个时间之间:\n", ts_hourly.between_time('09:00', '12:00'))
```

### 4.3 时间序列重采样

```python
import pandas as pd
import numpy as np

# 创建小时数据
dates = pd.date_range('2023-01-01', periods=72, freq='H')
ts = pd.Series(np.random.randn(72).cumsum(), index=dates)
print("原始数据(前10):\n", ts.head(10))

# 降采样 - 日均值
daily_mean = ts.resample('D').mean()
print("\n日均值:\n", daily_mean)

# 降采样 - 日汇总
daily_ohlc = ts.resample('D').ohlc()  # 开高低收
print("\n日OHLC:\n", daily_ohlc)

# 其他聚合方式
daily_sum = ts.resample('D').sum()
daily_max = ts.resample('D').max()

# 使用 apply
daily_range = ts.resample('D').apply(lambda x: x.max() - x.min())
print("\n日波动范围:\n", daily_range)

# 升采样 - 填充
hourly = daily_mean.resample('H').asfreq()  # 产生缺失值
hourly_ffill = daily_mean.resample('H').ffill()  # 前向填充
hourly_interpolate = daily_mean.resample('H').interpolate()  # 插值
print("\n插值后:\n", hourly_interpolate.head(10))
```

### 4.4 时间窗口操作

```python
import pandas as pd
import numpy as np

# 创建时间序列
dates = pd.date_range('2023-01-01', periods=20, freq='D')
ts = pd.Series(np.random.randn(20), index=dates)

# 滚动窗口
rolling_mean = ts.rolling(window=5).mean()
rolling_std = ts.rolling(window=5).std()
print("滚动均值:\n", rolling_mean)

# 滚动统计
rolling_stats = pd.DataFrame({
    '原始': ts,
    '5日均值': rolling_mean,
    '5日标准差': rolling_std,
    '5日最大': ts.rolling(window=5).max(),
    '5日最小': ts.rolling(window=5).min()
})
print("\n滚动统计:\n", rolling_stats)

# 扩展窗口
expanding_mean = ts.expanding().mean()  # 累计均值
expanding_max = ts.expanding().max()
print("\n扩展均值:\n", expanding_mean)

# 指数加权移动平均
ewm_mean = ts.ewm(span=5).mean()  # 5日EMA
print("\n指数加权均值:\n", ewm_mean)

# 窗口居中
centered = ts.rolling(window=5, center=True).mean()
print("\n居中窗口:\n", centered)

# 自定义窗口函数
def zscore(x):
    return (x[-1] - x.mean()) / x.std() if x.std() > 0 else 0

rolling_zscore = ts.rolling(window=5).apply(zscore)
print("\n滚动Z分数:\n", rolling_zscore)
```

### 4.5 时间偏移与转换

```python
import pandas as pd
from pandas.tseries.offsets import Day, MonthEnd, YearBegin

# 时间偏移
ts = pd.Timestamp('2023-06-15')
print(f"原始时间: {ts}")
print(f"加3天: {ts + Day(3)}")
print(f"月末: {ts + MonthEnd(0)}")
print(f"下月末: {ts + MonthEnd(1)}")
print(f"年初: {ts + YearBegin()}")

# 工作日偏移
from pandas.tseries.offsets import BDay
print(f"下一个工作日: {ts + BDay()}")

# 日期移动
dates = pd.date_range('2023-01-01', periods=5, freq='D')
shifted = pd.Series(range(5), index=dates)
print("\n原始:\n", shifted)
print("\n前移2天:\n", shifted.shift(2))
print("\n后移2天:\n", shifted.shift(-2))

# 频率转换
monthly = pd.date_range('2023-01-01', periods=12, freq='MS')  # 月初
data = pd.Series(range(12), index=monthly)
print("\n月数据:\n", data)

# 转换为季度
quarterly = data.resample('Q').sum()
print("\n季度数据:\n", quarterly)
```

---

## 五、字符串处理

### 5.1 字符串方法

```python
import pandas as pd
import numpy as np

# 创建示例数据
df = pd.DataFrame({
    'name': ['alice', 'BOB', 'Charlie', 'david', 'EVE'],
    'email': ['alice@example.com', 'bob@test.org', 'charlie@mail.net', 
              'david@example.com', 'eve@demo.io'],
    'phone': ['138-1234-5678', '139 8765 4321', '13612345678', 
              '137-9999-8888', '135 5555 6666']
})

# 大小写转换
print("大写:\n", df['name'].str.upper())
print("小写:\n", df['name'].str.lower())
print("首字母大写:\n", df['name'].str.capitalize())
print("单词首字母大写:\n", df['name'].str.title())

# 长度和计数
print("\n长度:\n", df['name'].str.len())
print("包含'a':\n", df['name'].str.contains('a', case=False))
print("计数'l':\n", df['name'].str.count('l'))

# 填充和对齐
print("\n左填充:\n", df['name'].str.pad(10, fillchar='-'))
print("居中:\n", df['name'].str.center(10, '-'))
print("补零:\n", pd.Series(['1', '22', '333']).str.zfill(5))

# 去除空格
s = pd.Series(['  hello  ', '  world', 'python  '])
print("\n去除两端空格:", s.str.strip().tolist())
print("去除左空格:", s.str.lstrip().tolist())
print("去除右空格:", s.str.rstrip().tolist())
```

### 5.2 字符串分割与提取

```python
import pandas as pd

df = pd.DataFrame({
    'email': ['alice@example.com', 'bob@test.org', 'charlie@mail.net'],
    'full_name': ['Alice Smith', 'Bob Johnson', 'Charlie Brown']
})

# 分割
print("邮箱分割:\n", df['email'].str.split('@'))
print("邮箱域名:\n", df['email'].str.split('@').str[1])
print("扩展分割:\n", df['email'].str.split('@', expand=True))

# 姓名分割
name_parts = df['full_name'].str.split(' ', expand=True)
df['first_name'] = name_parts[0]
df['last_name'] = name_parts[1]
print("\n分割后:\n", df)

# 正则提取
df['domain'] = df['email'].str.extract(r'@(.+)')
print("\n提取域名:\n", df)

# 多组提取
phone = pd.Series(['Cell: 138-1234-5678', 'Work: 021-8765-4321'])
extracted = phone.str.extract(r'(\w+):\s*(\d{3})-(\d{4})-(\d{4})')
print("\n多组提取:\n", extract)

# 查找
print("\n查找位置:", df['email'].str.find('@'))
print("查找所有:", df['email'].str.findall(r'[aeiou]'))
```

### 5.3 字符串替换

```python
import pandas as pd

s = pd.Series(['hello world', 'hello python', 'python world'])

# 简单替换
print("替换hello:", s.str.replace('hello', 'hi'))

# 正则替换
print("替换数字:", pd.Series(['abc123', 'def456']).str.replace(r'\d+', 'NUM'))

# 多次替换
replacements = {'hello': 'hi', 'world': 'earth'}
result = s.replace(replacements, regex=True)
print("\n多次替换:\n", result)

# 重复
print("\n重复3次:", pd.Series(['ab', 'cd']).str.repeat(3))

# 切片
print("\n前3个字符:", s.str[:3])
print("\n后5个字符:", s.str[-5:])
```

---

## 六、分类数据

### 6.1 分类类型基础

```python
import pandas as pd
import numpy as np

# 创建分类数据
s = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'], dtype='category')
print("分类Series:\n", s)
print(f"类别: {s.cat.categories}")
print(f"编码: {s.cat.codes}")

# 从DataFrame列创建
df = pd.DataFrame({'grade': ['A', 'B', 'C', 'A', 'B']})
df['grade'] = df['grade'].astype('category')
print("\nDataFrame分类列:\n", df['grade'])

# 指定类别顺序
df['grade'] = pd.Categorical(df['grade'], 
                              categories=['C', 'B', 'A'], 
                              ordered=True)
print("\n有序分类:\n", df['grade'])
print(f"A > B: {(df['grade'] == 'A').any() and 'A' in df['grade'].cat.categories}")

# 添加新类别
df['grade'] = df['grade'].cat.add_categories(['D'])
print(f"\n添加类别后: {df['grade'].cat.categories}")

# 删除未使用的类别
df['grade'] = df['grade'].cat.remove_unused_categories()
```

### 6.2 分类操作

```python
import pandas as pd

# 创建有序分类
grades = pd.Categorical(['B', 'A', 'C', 'A', 'B'],
                         categories=['C', 'B', 'A'],
                         ordered=True)
s = pd.Series(grades)
print("有序分类:\n", s)

# 比较操作
print(f"\n > 'B':\n{s > 'B'}")
print(f"\n >= 'B':\n{s >= 'B'}")

# 重命名类别
s = s.cat.rename_categories({'C': 'Poor', 'B': 'Good', 'A': 'Excellent'})
print("\n重命名后:\n", s)

# 重新编码
s = s.cat.reorder_categories(['Poor', 'Good', 'Excellent'], ordered=True)
print("\n重排序后:\n", s)

# 分箱转分类
ages = pd.Series([22, 45, 67, 34, 89, 12, 56])
age_groups = pd.cut(ages, bins=[0, 18, 35, 60, 100], 
                    labels=['儿童', '青年', '中年', '老年'])
print("\n年龄分组:\n", age_groups)

# qcut - 等频分箱
scores = pd.Series(np.random.randint(0, 100, 20))
score_quartiles = pd.qcut(scores, q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
print("\n成绩四分位:\n", score_quartiles.value_counts())
```

---

## 七、实战案例

### 7.1 销售数据分析

```python
import pandas as pd
import numpy as np

# 创建模拟销售数据
np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'order_id': range(1, n + 1),
    'customer_id': np.random.randint(1, 101, n),
    'product_category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], n),
    'product_name': [f'Product_{i}' for i in np.random.randint(1, 51, n)],
    'quantity': np.random.randint(1, 11, n),
    'unit_price': np.random.uniform(10, 500, n).round(2),
    'order_date': pd.date_range('2023-01-01', periods=n, freq='H'),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n),
    'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'Cash', 'Online'], n)
})

# 计算总金额
df['total_amount'] = df['quantity'] * df['unit_price']

# 提取时间特征
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['day_of_week'] = df['order_date'].dt.day_name()
df['hour'] = df['order_date'].dt.hour

print("数据概览:")
print(df.info())
print(df.head())
```

### 7.2 多维度分析

```python
import pandas as pd

# 延续上面的数据

# 1. 各产品类别销售分析
category_stats = df.groupby('product_category').agg({
    'order_id': 'count',
    'quantity': 'sum',
    'total_amount': ['sum', 'mean']
}).round(2)
print("产品类别分析:\n", category_stats)

# 2. 各地区销售透视表
region_pivot = df.pivot_table(
    values='total_amount',
    index='region',
    columns='product_category',
    aggfunc='sum',
    margins=True
).round(2)
print("\n地区销售透视:\n", region_pivot)

# 3. 时间序列分析
daily_sales = df.set_index('order_date').resample('D')['total_amount'].sum()
print("\n日销售额:\n", daily_sales.head())

# 4. 客户分析
customer_stats = df.groupby('customer_id').agg({
    'order_id': 'count',
    'total_amount': ['sum', 'mean']
}).round(2)
customer_stats.columns = ['order_count', 'total_spent', 'avg_order_value']
top_customers = customer_stats.nlargest(10, 'total_spent')
print("\nTop 10 客户:\n", top_customers)

# 5. 支付方式分析
payment_analysis = df.groupby('payment_method').agg({
    'order_id': 'count',
    'total_amount': 'sum'
})
payment_analysis['percentage'] = (payment_analysis['total_amount'] / payment_analysis['total_amount'].sum() * 100).round(2)
print("\n支付方式分析:\n", payment_analysis)
```

---

## 总结

| 知识点 | 核心要点 |
|--------|----------|
| 分组聚合 | `groupby()`, `agg()`, `transform()`, `filter()`, `apply()` |
| 数据合并 | `concat()`, `merge()`, `join()` |
| 透视表 | `pivot_table()`, `pivot()`, `melt()`, `crosstab()` |
| 时间序列 | `resample()`, `rolling()`, `shift()`, 日期提取 |
| 字符串 | `str` 访问器, 正则表达式 |

---

**上一篇**：[Pandas 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-basic %})

**下一篇**：[Pandas 数据分析实战]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-analysis %})

**返回**：[AI学习路线总览]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})

*最后更新: 2026年4月12日*

> 参考资源：
> - [Pandas官方文档 - GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html) - 分组聚合官方指南
> - [Pandas官方文档 - 时间序列](https://pandas.pydata.org/docs/user_guide/timeseries.html) - 时间序列官方指南
> - [Pandas官方文档 - Merge](https://pandas.pydata.org/docs/user_guide/merging.html) - 数据合并官方指南
> - [Pandas官方文档 - Reshape](https://pandas.pydata.org/docs/user_guide/reshaping.html) - 数据重塑官方指南
> - [SQL to Pandas Cheatsheet](https://pandas.pydata.org/pandas-docs/stable/getting_started/comparison/comparison_with_sql.html) - SQL到Pandas对照
> - [Time Series Analysis教程](https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/) - 时间序列预测速查
> - [Pandas GroupBy详解](https://realpython.com/pandas-groupby/) - Real Python GroupBy教程
> - [Time Series with Pandas](https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/) - Dataquest时间序列教程
> - [Working with Time Series](https://jakevdp.github.io/PythonDataScienceHandbook/03.11-working-with-time-series.html) - Python数据科学手册
> - [Pandas String Operations](https://jakevdp.github.io/PythonDataScienceHandbook/03.10-working-with-strings.html) - 字符串操作教程
> - [Pandas Merge vs Join详解](https://realpython.com/pandas-merge-join-and-concat/) - Real Python合并教程
