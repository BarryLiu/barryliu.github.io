---
layout: post
title: "Pandas 基础教程 - 数据分析入门"
date: 2026-04-12
categories: ailearn
tags: [AI, Python, Pandas, 数据分析]
keywords: Pandas, DataFrame, Series, 数据清洗, 数据分析入门
description: 深入学习 Pandas 基础操作，掌握 Series、DataFrame 创建与操作，为数据科学打下基础
---

* content
{:toc}

> **前置知识**：需要先掌握 [NumPy 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-basic %})。
>
> **本文重点**：理解 Series 和 DataFrame 核心概念，掌握数据创建、选择、过滤操作。

Pandas 是 Python 数据分析的核心库，提供了高效的数据结构和数据分析工具。本文将系统讲解 Pandas 的核心用法。

---

## 一、Pandas 简介

### 1.1 为什么需要 Pandas？

NumPy 适合处理同质数值数据，但现实数据通常是：
- **异构类型**：一列字符串，一列数值，一列日期
- **带标签**：需要用列名、行名而非数字索引
- **缺失值**：数据不完整是常态

Pandas 解决了这些问题：

```python
import numpy as np
import pandas as pd

# 生成示例数据
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, np.nan, 35],  # 包含缺失值
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'],
    'salary': [10000.0, 15000.0, 12000.0, 20000.0]
}

df = pd.DataFrame(data)
print(df)

#       name   age       city   salary
# 0    Alice  25.0    Beijing  10000.0
# 1      Bob  30.0   Shanghai  15000.0
# 2  Charlie   NaN  Guangzhou  12000.0
# 3    David  35.0   Shenzhen  20000.0
```

### 1.2 安装与导入

```bash
# 安装
pip install pandas

# 安装完整数据分析栈
pip install pandas numpy matplotlib seaborn openpyxl
```

```python
import pandas as pd
import numpy as np

# 查看版本
print(pd.__version__)  # 如: 2.2.0

# 常用配置
pd.set_option('display.max_rows', 10)      # 最大显示行数
pd.set_option('display.max_columns', 10)   # 最大显示列数
pd.set_option('display.width', 100)        # 显示宽度
pd.set_option('display.precision', 2)      # 小数精度
```

---

## 二、Series - 一维数据结构

Series 是带标签的一维数组，可以存储任何数据类型。

### 2.1 创建 Series

```python
import pandas as pd
import numpy as np

# 从列表创建
s1 = pd.Series([1, 2, 3, 4, 5])
print(s1)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

# 指定索引
s2 = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
print(s2)
# a    1
# b    2
# c    3
# d    4
# e    5
# dtype: int64

# 从字典创建
data = {'a': 100, 'b': 200, 'c': 300}
s3 = pd.Series(data)
print(s3)
# a    100
# b    200
# c    300
# dtype: int64

# 指定名称
s4 = pd.Series([1, 2, 3], name='my_series')
print(f"Series名称: {s4.name}")
```

### 2.2 Series 属性

```python
import pandas as pd

s = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'], name='numbers')

print(f"值 values: {s.values}")       # numpy数组
print(f"索引 index: {s.index}")       # 索引对象
print(f"数据类型 dtype: {s.dtype}")   # 数据类型
print(f"形状 shape: {s.shape}")       # (5,)
print(f"元素数 size: {s.size}")       # 5
print(f"名称 name: {s.name}")         # 'numbers'
```

### 2.3 Series 索引与切片

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

# 通过标签索引
print(s['a'])       # 10
print(s[['a', 'c']])  # 返回Series

# 通过位置索引
print(s[0])         # 10
print(s[1:3])       # b 20, c 30
print(s.iloc[0])    # 10 (显式位置索引)
print(s.iloc[1:3])  # b 20, c 30

# 标签切片（包含两端）
print(s['a':'c'])   # a 10, b 20, c 30

# 布尔索引
print(s[s > 25])
# c    30
# d    40
# e    50

# 使用 loc 和 iloc
print(s.loc['a'])    # 标签索引
print(s.loc['a':'c'])  # 标签切片
print(s.iloc[0])     # 位置索引
print(s.iloc[0:3])   # 位置切片
```

### 2.4 Series 运算

```python
import pandas pd
import numpy as np

s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])

# 算术运算
print(s1 + s2)    # 元素相加
print(s1 * 2)     # 标量乘法
print(s1 ** 2)    # 平方

# 数学函数
print(np.sqrt(s1))
print(np.exp(s1))

# 统计方法
print(f"求和: {s1.sum()}")
print(f"均值: {s1.mean()}")
print(f"标准差: {s1.std()}")
print(f"最大值: {s1.max()}")
print(f"最大值索引: {s1.idxmax()}")

# 不同索引的运算
s3 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s4 = pd.Series([10, 20, 30], index=['b', 'c', 'd'])
print(s3 + s4)  # 自动对齐，不匹配的位置为 NaN
# a     NaN
# b    12.0
# c    23.0
# d     NaN
```

---

## 三、DataFrame - 二维数据结构

DataFrame 是带标签的二维表格，是数据分析的核心数据结构。

### 3.1 创建 DataFrame

```python
import pandas as pd
import numpy as np

# 从字典创建
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
}
df = pd.DataFrame(data)
print(df)

# 指定列顺序
df = pd.DataFrame(data, columns=['city', 'name', 'age'])
print(df)

# 指定索引
df = pd.DataFrame(data, index=['A', 'B', 'C', 'D'])
print(df)

# 从列表的列表创建
data2 = [
    ['Alice', 25, 'Beijing'],
    ['Bob', 30, 'Shanghai'],
    ['Charlie', 35, 'Guangzhou']
]
df2 = pd.DataFrame(data2, columns=['name', 'age', 'city'])
print(df2)

# 从 NumPy 数组创建
arr = np.random.randn(4, 3)
df3 = pd.DataFrame(arr, columns=['A', 'B', 'C'])
print(df3)

# 从 Series 字典创建
s1 = pd.Series([1, 2, 3], name='col1')
s2 = pd.Series([4, 5, 6], name='col2')
df4 = pd.DataFrame({s1.name: s1, s2.name: s2})
print(df4)
```

### 3.2 DataFrame 属性

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85.5, 90.0, 78.5]
})

print(f"形状 shape: {df.shape}")         # (3, 3)
print(f"列数 len(df.columns): {len(df.columns)}")   # 3
print(f"行数 len(df): {len(df)}")         # 3
print(f"列名 columns: {list(df.columns)}")
print(f"索引 index: {list(df.index)}")
print(f"数据类型 dtypes:\n{df.dtypes}")
print(f"值 values:\n{df.values}")         # NumPy数组
print(f"维度 ndim: {df.ndim}")           # 2
print(f"总元素数 size: {df.size}")        # 9
```

### 3.3 查看数据

```python
import pandas as pd
import numpy as np

# 创建较大数据集
df = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100),
    'C': np.random.randn(100),
    'D': np.random.randn(100)
})

# 查看前几行
print(df.head())      # 默认5行
print(df.head(10))    # 10行

# 查看后几行
print(df.tail())
print(df.tail(3))

# 查看数据概览
print(df.info())

# 统计描述
print(df.describe())

# 快速查看唯一值
df_cat = pd.DataFrame({'category': ['A', 'B', 'A', 'C', 'B', 'A']})
print(df_cat['category'].value_counts())

# 查看数据类型
print(df.dtypes)

# 查看内存使用
print(df.memory_usage())
```

---

## 四、数据选择与过滤

### 4.1 选择列

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'],
    'salary': [10000, 15000, 12000, 20000]
})

# 选择单列（返回Series）
print(df['name'])        # 推荐方式
print(df.name)           # 属性访问（列名必须是有效Python标识符）

# 选择多列（返回DataFrame）
print(df[['name', 'age']])

# 选择指定顺序的列
cols = ['city', 'name', 'salary']
print(df[cols])

# 使用 filter 选择列
print(df.filter(like='a'))       # 列名包含'a'的列
print(df.filter(regex='^[ac]'))  # 列名以a或c开头的列
```

### 4.2 选择行

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
}, index=['A', 'B', 'C', 'D'])

# 使用标签索引 (loc)
print(df.loc['A'])           # 选择单行
print(df.loc[['A', 'C']])    # 选择多行
print(df.loc['A':'C'])       # 切片（包含两端）

# 使用位置索引 (iloc)
print(df.iloc[0])            # 第一行
print(df.iloc[[0, 2]])       # 第1和第3行
print(df.iloc[0:2])          # 前两行
print(df.iloc[-1])           # 最后一行

# 同时选择行和列
print(df.loc['A', 'name'])           # 单个值
print(df.loc['A':'C', 'name'])       # 多行单列
print(df.loc['A':'C', ['name', 'age']])  # 多行多列
print(df.iloc[0:2, 0:2])             # 位置切片
```

### 4.3 布尔索引

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 40, 45],
    'city': ['Beijing', 'Shanghai', 'Beijing', 'Shanghai', 'Guangzhou'],
    'salary': [10000, 15000, 12000, 20000, 18000]
})

# 单条件过滤
print(df[df['age'] > 30])
print(df[df['city'] == 'Beijing'])

# 多条件过滤
print(df[(df['age'] > 30) & (df['salary'] > 15000)])  # 且
print(df[(df['age'] < 30) | (df['salary'] > 15000)])  # 或

# 使用 query 方法
print(df.query('age > 30'))
print(df.query('age > 30 and salary > 15000'))
print(df.query('city == "Beijing" or city == "Shanghai"'))

# isin 方法
cities = ['Beijing', 'Shanghai']
print(df[df['city'].isin(cities)])

# between 方法
print(df[df['age'].between(30, 40)])

# 包含字符串
print(df[df['name'].str.contains('a', case=False)])

# 检查缺失值
df_with_nan = df.copy()
df_with_nan.loc[1, 'salary'] = np.nan
print(df_with_nan[df_with_nan['salary'].isna()])
print(df_with_nan[df_with_nan['salary'].notna()])
```

### 4.4 条件赋值

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'score': [85, 45, 92, 58],
    'attendance': [90, 70, 95, 60]
})

# 直接赋值
df['passed'] = df['score'] >= 60

# 使用 loc 条件赋值
df.loc[df['score'] < 60, 'grade'] = 'F'
df.loc[(df['score'] >= 60) & (df['score'] < 80), 'grade'] = 'C'
df.loc[(df['score'] >= 80) & (df['score'] < 90), 'grade'] = 'B'
df.loc[df['score'] >= 90, 'grade'] = 'A'

print(df)

# 使用 np.where
df['status'] = np.where(df['score'] >= 60, 'Pass', 'Fail')

# 使用 apply
def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 60:
        return 'C'
    else:
        return 'F'

df['grade2'] = df['score'].apply(get_grade)

# 使用 map
df['grade_map'] = df['grade'].map({'A': '优秀', 'B': '良好', 'C': '及格', 'F': '不及格'})

print(df)
```

---

## 五、数据增删改

### 5.1 添加数据

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30]
})

# 添加列
df['city'] = ['Beijing', 'Shanghai']
df['salary'] = [10000, 15000]
df['is_active'] = True  # 广播到所有行

# 使用 assign 方法（返回新DataFrame）
df_new = df.assign(
    department=['IT', 'HR'],
    level=['Junior', 'Senior']
)

# 添加行
new_row = pd.DataFrame({'name': ['Charlie'], 'age': [35], 'city': ['Guangzhou']})
df = pd.concat([df, new_row], ignore_index=True)

# 使用 loc 添加行
df.loc[len(df)] = ['David', 40, 'Shenzhen', 20000, True]

# 插入列到指定位置
df.insert(1, 'gender', ['F', 'M', 'M', 'M'])
print(df)
```

### 5.2 删除数据

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'city': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
})

# 删除列
df_dropped = df.drop('age', axis=1)  # 返回新DataFrame
df.drop('age', axis=1, inplace=True)  # 原地修改

# 删除多列
df_dropped = df.drop(['age', 'city'], axis=1)

# 使用列选择删除
df_selected = df[['name']]  # 只保留name列

# 删除行
df_dropped = df.drop(0)  # 删除第一行
df_dropped = df.drop([0, 2])  # 删除多行

# 条件删除
df_filtered = df[df['age'] > 30]  # 删除age <= 30的行

# 删除缺失值
df_with_nan = df.copy()
df_with_nan.loc[1, 'age'] = np.nan
df_cleaned = df_with_nan.dropna()  # 删除有缺失值的行
df_cleaned = df_with_nan.dropna(subset=['age'])  # 只检查特定列
df_cleaned = df_with_nan.dropna(how='all')  # 全部为NaN才删除

# 删除重复值
df_dup = pd.DataFrame({
    'A': [1, 2, 2, 3, 3, 3],
    'B': ['a', 'b', 'b', 'c', 'c', 'd']
})
df_unique = df_dup.drop_duplicates()  # 删除完全重复的行
df_unique = df_dup.drop_duplicates(subset=['A'])  # 只看A列
df_unique = df_dup.drop_duplicates(keep='last')  # 保留最后一个
```

### 5.3 修改数据

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Beijing', 'Shanghai', 'Guangzhou']
})

# 修改单个值
df.loc[0, 'age'] = 26
df.iloc[1, 1] = 31

# 批量修改列
df['age'] = df['age'] + 1
df['city'] = df['city'].str.upper()

# 条件修改
df.loc[df['age'] > 30, 'category'] = 'Senior'
df.loc[df['age'] <= 30, 'category'] = 'Junior'

# 使用 replace
df['city'] = df['city'].replace('BEIJING', 'BJ')
df['city'] = df['city'].replace({'SHANGHAI': 'SH', 'GUANGZHOU': 'GZ'})

# 使用 apply 修改
df['age_months'] = df['age'].apply(lambda x: x * 12)

# 更新多个值
df.update(pd.DataFrame({'age': [27, 32, 37]}, index=[0, 1, 2]))
```

---

## 六、数据导入导出

### 6.1 CSV 文件

```python
import pandas as pd
import numpy as np

# 创建示例数据
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'salary': [10000.0, 15000.0, 12000.0, 20000.0]
})

# 写入CSV
df.to_csv('data.csv', index=False)  # 不保存索引
df.to_csv('data.csv', index=False, encoding='utf-8')

# 读取CSV
df_read = pd.read_csv('data.csv')

# 更多读取选项
df = pd.read_csv(
    'data.csv',
    sep=',',              # 分隔符
    header=0,             # 表头行
    names=['A', 'B', 'C'], # 自定义列名
    index_col=0,          # 指定索引列
    usecols=['name', 'age'],  # 只读特定列
    dtype={'age': int},   # 指定数据类型
    nrows=100,            # 只读前n行
    skiprows=1,           # 跳过行
    na_values=['NA', 'N/A', 'null'],  # 缺失值标记
    parse_dates=['date'], # 解析日期
    encoding='utf-8'
)

# 读取大型文件（分块）
chunk_iter = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in chunk_iter:
    process(chunk)  # 处理每个块
```

### 6.2 Excel 文件

```python
import pandas as pd

# 写入Excel
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df.to_excel('data.xlsx', index=False, sheet_name='Sheet1')

# 多个工作表
with pd.ExcelWriter('multi_sheet.xlsx') as writer:
    df1 = pd.DataFrame({'A': [1, 2]})
    df2 = pd.DataFrame({'B': [3, 4]})
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)

# 读取Excel
df = pd.read_excel('data.xlsx')
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df = pd.read_excel('data.xlsx', sheet_name=0)  # 按索引
df = pd.read_excel('data.xlsx', sheet_name=['Sheet1', 'Sheet2'])  # 多sheet

# 读取所有sheet
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)
print(all_sheets.keys())
```

### 6.3 其他格式

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

# ===== JSON =====
# 写入JSON
df.to_json('data.json', orient='records', indent=2)

# 读取JSON
df_json = pd.read_json('data.json')
df_json = pd.read_json('data.json', orient='records')

# ===== Parquet（推荐大数据格式）=====
# 需要安装: pip install pyarrow 或 fastparquet
df.to_parquet('data.parquet')
df_parquet = pd.read_parquet('data.parquet')

# ===== Pickle（Python对象序列化）=====
df.to_pickle('data.pkl')
df_pickle = pd.read_pickle('data.pkl')

# ===== SQL 数据库 =====
# 需要安装: pip install sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mydatabase.db')
df.to_sql('users', engine, if_exists='replace', index=False)
df_sql = pd.read_sql('SELECT * FROM users', engine)

# ===== HTML 表格 =====
# 需要安装: pip install lxml html5lib
dfs = pd.read_html('https://example.com/table.html')  # 返回列表
df_html = dfs[0]

# ===== 剪贴板 =====
# 从剪贴板读取（复制Excel数据后）
df_clip = pd.read_clipboard()

# 写入剪贴板
df.to_clipboard()
```

---

## 七、数据清洗基础

### 7.1 处理缺失值

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 2, 3, np.nan, 5],
    'C': [1, 2, 3, 4, 5]
})

# 检查缺失值
print(df.isna())          # 布尔DataFrame
print(df.isna().sum())    # 每列缺失值数量
print(df.isna().any())    # 哪些列有缺失值

# 删除缺失值
df_dropna = df.dropna()              # 删除有缺失值的行
df_dropna_all = df.dropna(how='all') # 只有全部缺失才删除
df_dropna_subset = df.dropna(subset=['A'])  # 只检查特定列
df_dropna_thresh = df.dropna(thresh=2)  # 至少有2个非缺失值

# 填充缺失值
df_fill = df.fillna(0)               # 用0填充
df_fill_mean = df.fillna(df.mean())  # 用均值填充
df_fill_ffill = df.fillna(method='ffill')  # 前向填充
df_fill_bfill = df.fillna(method='bfill')  # 后向填充

# 不同列不同填充值
df_fill_dict = df.fillna({'A': 0, 'B': df['B'].mean()})

# 插值填充
df_interpolate = df.interpolate()    # 线性插值
df_interpolate_time = df.interpolate(method='time')  # 时间插值
```

### 7.2 处理重复值

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
    'age': [25, 30, 25, 35, 30],
    'city': ['Beijing', 'Shanghai', 'Beijing', 'Guangzhou', 'Shanghai']
})

# 检查重复
print(df.duplicated())          # 每行是否重复
print(df.duplicated().sum())    # 重复行数
print(df.duplicated(subset=['name']))  # 只看特定列

# 删除重复
df_unique = df.drop_duplicates()
df_unique_name = df.drop_duplicates(subset=['name'])
df_unique_keep_last = df.drop_duplicates(keep='last')

# 标记重复
df['is_duplicate'] = df.duplicated()
```

### 7.3 数据类型转换

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': ['1', '2', '3', '4'],
    'B': ['1.1', '2.2', '3.3', '4.4'],
    'C': ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01'],
    'D': ['True', 'False', 'True', 'False']
})

# 查看数据类型
print(df.dtypes)

# 转换为数值
df['A'] = pd.to_numeric(df['A'])
df['B'] = df['B'].astype(float)

# 转换为日期
df['C'] = pd.to_datetime(df['C'])

# 转换为布尔
df['D'] = df['D'].map({'True': True, 'False': False})

# 转换为分类
df['category'] = df['A'].astype('category')

# 一次转换多列
df = df.astype({'A': int, 'B': float})

# 智能转换
df['A'] = pd.to_numeric(df['A'], errors='coerce')  # 错误转为NaN
df['A'] = pd.to_numeric(df['A'], errors='ignore')  # 保持原样

# 日期解析
df['C'] = pd.to_datetime(df['C'], format='%Y-%m-%d')
df['C'] = pd.to_datetime(df['C'], yearfirst=True)

# 提取日期组件
df['year'] = df['C'].dt.year
df['month'] = df['C'].dt.month
df['day'] = df['C'].dt.day
df['weekday'] = df['C'].dt.day_name()

print(df.dtypes)
```

---

## 八、实战案例

### 8.1 数据加载与初步分析

```python
import pandas as pd
import numpy as np

# 创建模拟数据集
np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'user_id': range(1, n + 1),
    'name': [f'User_{i}' for i in range(1, n + 1)],
    'age': np.random.randint(18, 70, n),
    'gender': np.random.choice(['M', 'F'], n),
    'city': np.random.choice(['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'], n),
    'registration_date': pd.date_range('2020-01-01', periods=n, freq='D'),
    'total_spent': np.random.exponential(1000, n),
    'order_count': np.random.poisson(5, n),
    'is_vip': np.random.choice([True, False], n, p=[0.2, 0.8])
})

# 引入一些缺失值和异常值
df.loc[np.random.choice(n, 50), 'age'] = np.nan
df.loc[np.random.choice(n, 30), 'city'] = np.nan
df.loc[np.random.choice(n, 10), 'total_spent'] = -1  # 异常值

print("数据概览:")
print(df.info())
print("\n前5行:")
print(df.head())
print("\n统计描述:")
print(df.describe())
```

### 8.2 数据清洗流程

```python
import pandas as pd
import numpy as np

# 延续上面的数据集

# 1. 检查缺失值
print("缺失值统计:")
print(df.isna().sum())

# 2. 处理缺失值
# age用中位数填充
df['age'] = df['age'].fillna(df['age'].median())
# city用众数填充
df['city'] = df['city'].fillna(df['city'].mode()[0])

# 3. 处理异常值
# 将负的消费金额修正为0
df.loc[df['total_spent'] < 0, 'total_spent'] = 0

# 4. 数据类型优化
df['user_id'] = df['user_id'].astype('int32')
df['gender'] = df['gender'].astype('category')
df['city'] = df['city'].astype('category')

# 5. 创建派生特征
df['avg_order_value'] = df['total_spent'] / (df['order_count'] + 1)
df['registration_year'] = df['registration_date'].dt.year
df['days_since_registration'] = (pd.Timestamp.now() - df['registration_date']).dt.days
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], 
                          labels=['<25', '25-35', '35-45', '45-55', '>55'])

print("\n清洗后数据:")
print(df.info())
print(df.head())
```

---

## 总结

| 知识点 | 核心要点 |
|--------|----------|
| Series | 一维带标签数组，`values`, `index`, `name` |
| DataFrame | 二维表格，`shape`, `columns`, `index`, `dtypes` |
| 数据选择 | `[]`, `loc`, `iloc`, `query`, 布尔索引 |
| 数据修改 | `loc`赋值, `apply`, `map`, `replace` |
| 数据清洗 | `dropna`, `fillna`, `drop_duplicates`, 类型转换 |

---

**上一篇**：[NumPy 进阶教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-advanced %})

**下一篇**：[Pandas 进阶教程 - 数据处理与分组聚合]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-advanced %})

**返回**：[AI学习路线总览]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})

*最后更新: 2026年4月12日*

> 参考资源：
> - [Pandas官方文档](https://pandas.pydata.org/docs/) - 官方完整文档
> - [Pandas中文教程](https://www.pypandas.cn/) - 中文文档
> - [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html) - 10分钟入门
> - [Pandas Cookbook](https://pandas-cookbook.readthedocs.io/) - 实战食谱
> - [Kaggle Pandas教程](https://www.kaggle.com/learn/pandas) - Kaggle官方教程
> - [Data School Pandas](https://www.dataschool.io/easier-data-analysis-with-pandas/) - 视频教程
> - [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) - 速查表PDF
> - [Real Python Pandas](https://realpython.com/learning-paths/pandas-data-science/) - Real Python教程
> - [Python for Data Analysis](https://wesmckinney.com/book/) - Pandas作者经典书籍
> - [Pandas Exercises](https://github.com/guipsamora/pandas_exercises) - Pandas练习题
