---
layout: post
title: "Pandas 数据分析实战 - 完整案例"
date: 2026-04-12
categories: ailearn
tags: [AI, Python, Pandas, 数据分析, 实战]
keywords: Pandas, 数据分析, 数据清洗, 特征工程, 实战案例
description: 通过完整实战案例学习 Pandas 数据分析流程，掌握数据清洗、特征工程、数据可视化等技能
---

* content
{:toc}

> **前置知识**：需要先掌握 [Pandas 进阶教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-advanced %})。
>
> **本文重点**：通过实战案例串联所有知识点，形成完整的数据分析能力。

本文通过一个完整的电商用户分析案例，串联 Pandas 所有核心知识点，帮助你建立数据分析的完整工作流程。

---

## 一、项目背景与目标

### 1.1 案例场景

我们是一家电商公司的数据分析师，需要分析用户行为数据，回答以下问题：

1. **用户画像**：我们的用户是谁？年龄、地域分布如何？
2. **购买行为**：用户购买频率、金额分布如何？
3. **用户价值**：哪些用户价值最高？如何划分用户层级？
4. **流失预警**：哪些用户可能流失？

### 1.2 数据准备

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置显示选项
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 120)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# 创建模拟数据集
np.random.seed(42)
n_users = 1000
n_orders = 5000

# 用户基础数据
users = pd.DataFrame({
    'user_id': range(1, n_users + 1),
    'register_date': pd.date_range('2020-01-01', periods=n_users, freq='6H'),
    'age': np.random.randint(18, 65, n_users),
    'gender': np.random.choice(['M', 'F'], n_users),
    'city': np.random.choice(
        ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Hangzhou', 'Chengdu'], 
        n_users,
        p=[0.25, 0.25, 0.15, 0.15, 0.1, 0.1]
    ),
    'membership_level': np.random.choice(['Normal', 'Silver', 'Gold', 'Diamond'], n_users, p=[0.5, 0.3, 0.15, 0.05])
})

# 订单数据
orders = pd.DataFrame({
    'order_id': range(1, n_orders + 1),
    'user_id': np.random.randint(1, n_users + 1, n_orders),
    'order_date': pd.date_range('2022-01-01', periods=n_orders, freq='90min'),
    'product_category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Home', 'Beauty'], n_orders),
    'quantity': np.random.randint(1, 5, n_orders),
    'unit_price': np.random.exponential(200, n_orders).round(2),
    'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'Alipay', 'WeChat Pay'], n_orders),
    'is_returned': np.random.choice([0, 1], n_orders, p=[0.9, 0.1])
})

# 计算订单金额
orders['order_amount'] = orders['quantity'] * orders['unit_price']

# 添加一些数据问题
# 缺失值
users.loc[np.random.choice(n_users, 30, replace=False), 'age'] = np.nan
users.loc[np.random.choice(n_users, 20, replace=False), 'city'] = np.nan

# 异常值
orders.loc[np.random.choice(n_orders, 5, replace=False), 'unit_price'] = -100
orders.loc[np.random.choice(n_orders, 5, replace=False), 'quantity'] = 100

print(f"用户数据: {users.shape}")
print(f"订单数据: {orders.shape}")
```

---

## 二、数据探索与清洗

### 2.1 数据概览

```python
# 基本信息
print("=== 用户数据概览 ===")
print(users.info())
print("\n前5行:")
print(users.head())

print("\n=== 订单数据概览 ===")
print(orders.info())
print("\n前5行:")
print(orders.head())

# 统计描述
print("\n=== 用户数据统计 ===")
print(users.describe())
print(users.describe(include='object'))

print("\n=== 订单数据统计 ===")
print(orders.describe())
```

### 2.2 数据质量检查

```python
def check_data_quality(df, name):
    """数据质量检查函数"""
    print(f"\n{'='*50}")
    print(f"数据集: {name}")
    print(f"{'='*50}")
    
    # 缺失值
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        '缺失数量': missing,
        '缺失比例%': missing_pct
    })
    if missing.sum() > 0:
        print("\n缺失值:")
        print(missing_df[missing_df['缺失数量'] > 0])
    else:
        print("\n无缺失值")
    
    # 重复值
    duplicates = df.duplicated().sum()
    print(f"\n重复行: {duplicates} ({duplicates/len(df)*100:.2f}%)")
    
    # 数值列异常值检测
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        if outliers > 0:
            print(f"\n{col} 异常值: {outliers} (范围: {lower:.2f} ~ {upper:.2f})")

# 检查两个数据集
check_data_quality(users, 'Users')
check_data_quality(orders, 'Orders')
```

### 2.3 数据清洗

```python
# 备份原始数据
users_clean = users.copy()
orders_clean = orders.copy()

# ===== 清洗用户数据 =====
# 处理年龄缺失值 - 用中位数填充
age_median = users_clean['age'].median()
users_clean['age'] = users_clean['age'].fillna(age_median)

# 处理城市缺失值 - 用众数填充
city_mode = users_clean['city'].mode()[0]
users_clean['city'] = users_clean['city'].fillna(city_mode)

# 创建年龄分组
users_clean['age_group'] = pd.cut(
    users_clean['age'], 
    bins=[0, 25, 35, 45, 55, 100],
    labels=['<25', '25-35', '35-45', '45-55', '>55']
)

print("用户数据清洗完成")

# ===== 清洗订单数据 =====
# 处理异常值 - 负价格
orders_clean.loc[orders_clean['unit_price'] < 0, 'unit_price'] = np.nan
orders_clean['unit_price'] = orders_clean['unit_price'].fillna(orders_clean['unit_price'].median())

# 处理异常值 - 过大数量
orders_clean.loc[orders_clean['quantity'] > 20, 'quantity'] = 20

# 重新计算订单金额
orders_clean['order_amount'] = orders_clean['quantity'] * orders_clean['unit_price']

# 提取时间特征
orders_clean['year'] = orders_clean['order_date'].dt.year
orders_clean['month'] = orders_clean['order_date'].dt.month
orders_clean['day'] = orders_clean['order_date'].dt.day
orders_clean['day_of_week'] = orders_clean['order_date'].dt.day_name()
orders_clean['hour'] = orders_clean['order_date'].dt.hour
orders_clean['is_weekend'] = orders_clean['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)

print("订单数据清洗完成")

# 再次检查数据质量
check_data_quality(users_clean, 'Users (Cleaned)')
check_data_quality(orders_clean, 'Orders (Cleaned)')
```

---

## 三、用户画像分析

### 3.1 基础特征分布

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体（如果可用）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图表
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 年龄分布
axes[0, 0].hist(users_clean['age'], bins=20, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Age Distribution')
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Count')

# 性别分布
gender_counts = users_clean['gender'].value_counts()
axes[0, 1].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
axes[0, 1].set_title('Gender Distribution')

# 城市分布
city_counts = users_clean['city'].value_counts()
axes[1, 0].bar(city_counts.index, city_counts.values)
axes[1, 0].set_title('City Distribution')
axes[1, 0].set_xlabel('City')
axes[1, 0].set_ylabel('Count')
axes[1, 0].tick_params(axis='x', rotation=45)

# 会员等级分布
membership_counts = users_clean['membership_level'].value_counts()
axes[1, 1].bar(membership_counts.index, membership_counts.values)
axes[1, 1].set_title('Membership Level Distribution')
axes[1, 1].set_xlabel('Level')
axes[1, 1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('user_profile.png', dpi=150)
plt.show()

print("用户画像图表已保存")
```

### 3.2 用户分组统计

```python
# 按性别统计
gender_stats = users_clean.groupby('gender').agg({
    'user_id': 'count',
    'age': 'mean'
}).round(2)
gender_stats.columns = ['用户数', '平均年龄']
print("性别统计:\n", gender_stats)

# 按城市统计
city_stats = users_clean.groupby('city').agg({
    'user_id': 'count',
    'age': ['mean', 'std']
}).round(2)
city_stats.columns = ['用户数', '平均年龄', '年龄标准差']
print("\n城市统计:\n", city_stats)

# 按会员等级统计
membership_stats = users_clean['membership_level'].value_counts(normalize=True).round(4) * 100
print("\n会员等级占比(%):\n", membership_stats)

# 年龄分组统计
age_group_stats = users_clean['age_group'].value_counts().sort_index()
print("\n年龄分组统计:\n", age_group_stats)
```

---

## 四、购买行为分析

### 4.1 订单概况

```python
# 合并用户和订单数据
orders_with_user = pd.merge(orders_clean, users_clean, on='user_id', how='left')

print("合并后数据:")
print(orders_with_user.info())

# 基础统计
print("\n=== 订单基础统计 ===")
print(f"总订单数: {len(orders_clean):,}")
print(f"总金额: ¥{orders_clean['order_amount'].sum():,.2f}")
print(f"平均订单金额: ¥{orders_clean['order_amount'].mean():.2f}")
print(f"订单金额中位数: ¥{orders_clean['order_amount'].median():.2f}")
print(f"退货率: {orders_clean['is_returned'].mean()*100:.2f}%")

# 产品类别分析
category_stats = orders_clean.groupby('product_category').agg({
    'order_id': 'count',
    'quantity': 'sum',
    'order_amount': ['sum', 'mean']
}).round(2)
category_stats.columns = ['订单数', '总数量', '总金额', '平均金额']
category_stats['订单占比%'] = (category_stats['订单数'] / category_stats['订单数'].sum() * 100).round(2)
category_stats = category_stats.sort_values('总金额', ascending=False)
print("\n产品类别分析:\n", category_stats)
```

### 4.2 时间维度分析

```python
# 每日订单趋势
daily_orders = orders_clean.groupby(orders_clean['order_date'].dt.date).agg({
    'order_id': 'count',
    'order_amount': 'sum'
})
daily_orders.columns = ['订单数', '销售额']
print("每日订单统计:\n", daily_orders.head())

# 每周趋势
weekly_orders = orders_clean.groupby('day_of_week')['order_amount'].sum()
weekly_orders = weekly_orders.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
print("\n每周销售额:\n", weekly_orders)

# 每小时趋势
hourly_orders = orders_clean.groupby('hour')['order_id'].count()
print("\n每小时订单数:\n", hourly_orders)

# 工作日 vs 周末
weekend_comparison = orders_clean.groupby('is_weekend').agg({
    'order_id': 'count',
    'order_amount': ['sum', 'mean']
}).round(2)
weekend_comparison.index = ['工作日', '周末']
weekend_comparison.columns = ['订单数', '总金额', '平均金额']
print("\n工作日vs周末:\n", weekend_comparison)

# 可视化
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 每周趋势
axes[0].bar(weekly_orders.index, weekly_orders.values)
axes[0].set_title('Weekly Sales')
axes[0].set_xlabel('Day')
axes[0].set_ylabel('Sales Amount')
axes[0].tick_params(axis='x', rotation=45)

# 每小时趋势
axes[1].plot(hourly_orders.index, hourly_orders.values, marker='o')
axes[1].set_title('Hourly Orders')
axes[1].set_xlabel('Hour')
axes[1].set_ylabel('Order Count')
axes[1].set_xticks(range(24))

plt.tight_layout()
plt.savefig('time_analysis.png', dpi=150)
plt.show()
```

### 4.3 支付方式分析

```python
# 支付方式统计
payment_stats = orders_clean.groupby('payment_method').agg({
    'order_id': 'count',
    'order_amount': ['sum', 'mean'],
    'is_returned': 'mean'
}).round(4)
payment_stats.columns = ['订单数', '总金额', '平均金额', '退货率']
payment_stats['退货率'] = (payment_stats['退货率'] * 100).round(2)
payment_stats = payment_stats.sort_values('总金额', ascending=False)
print("支付方式分析:\n", payment_stats)

# 不同支付方式的金额分布
payment_amount_dist = orders_clean.groupby('payment_method')['order_amount'].describe().round(2)
print("\n支付方式金额分布:\n", payment_amount_dist)
```

---

## 五、用户价值分析 (RFM)

### 5.1 RFM 模型

RFM 是经典的用户价值分析模型：
- **R (Recency)**：最近一次购买距今天数
- **F (Frequency)**：购买频次
- **M (Monetary)**：购买金额

```python
# 计算RFM指标
current_date = orders_clean['order_date'].max() + pd.Timedelta(days=1)

rfm = orders_clean.groupby('user_id').agg({
    'order_date': lambda x: (current_date - x.max()).days,  # Recency
    'order_id': 'count',                                      # Frequency
    'order_amount': 'sum'                                     # Monetary
}).round(2)

rfm.columns = ['recency', 'frequency', 'monetary']
print("RFM数据:\n", rfm.head(10))
print("\nRFM统计:\n", rfm.describe())

# RFM评分 (1-5分)
# Recency: 越小越好，反向打分
rfm['r_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1])

# Frequency: 越大越好，正向打分
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])

# Monetary: 越大越好，正向打分
rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])

# 综合评分
rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
rfm['rfm_total'] = rfm[['r_score', 'f_score', 'm_score']].astype(int).sum(axis=1)

print("\n带评分的RFM:\n", rfm.head())
```

### 5.2 用户分层

```python
# 基于RFM总分进行用户分层
def segment_user(score):
    if score >= 13:
        return '重要价值客户'
    elif score >= 10:
        return '重要发展客户'
    elif score >= 7:
        return '一般价值客户'
    elif score >= 4:
        return '一般发展客户'
    else:
        return '低价值客户'

rfm['segment'] = rfm['rfm_total'].apply(segment_user)

# 分层统计
segment_stats = rfm.groupby('segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': ['mean', 'sum', 'count']
}).round(2)

segment_stats.columns = ['平均R天数', '平均F次数', '平均M金额', '总M金额', '用户数']
segment_stats['用户占比%'] = (segment_stats['用户数'] / segment_stats['用户数'].sum() * 100).round(2)
segment_stats['金额占比%'] = (segment_stats['总M金额'] / segment_stats['总M金额'].sum() * 100).round(2)

print("用户分层统计:\n", segment_stats)

# 合并回用户数据
users_with_rfm = pd.merge(users_clean, rfm.reset_index(), on='user_id')
print("\n合并RFM后的用户数据:\n", users_with_rfm.head())
```

### 5.3 用户分层可视化

```python
import matplotlib.pyplot as plt

# 分层用户数
segment_counts = rfm['segment'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 用户数分布
axes[0].pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('User Segment Distribution')

# RFM散点图
scatter = axes[1].scatter(rfm['recency'], rfm['monetary'], 
                          c=rfm['frequency'], cmap='viridis', 
                          alpha=0.5, s=rfm['frequency']*5)
axes[1].set_xlabel('Recency (days)')
axes[1].set_ylabel('Monetary (amount)')
axes[1].set_title('RFM Scatter Plot')
plt.colorbar(scatter, ax=axes[1], label='Frequency')

plt.tight_layout()
plt.savefig('rfm_analysis.png', dpi=150)
plt.show()
```

---

## 六、流失预警分析

### 6.1 定义流失用户

```python
# 假设30天未购买为流失风险
churn_threshold = 30

# 计算每个用户的最后购买日期
last_purchase = orders_clean.groupby('user_id')['order_date'].max()
last_purchase = last_purchase.reset_index()
last_purchase.columns = ['user_id', 'last_purchase_date']

# 合并到用户数据
users_churn = pd.merge(users_clean, last_purchase, on='user_id', how='left')

# 计算距今天数
analysis_date = orders_clean['order_date'].max() + pd.Timedelta(days=1)
users_churn['days_since_last_purchase'] = (analysis_date - users_churn['last_purchase_date']).dt.days

# 定义流失标签
users_churn['is_churn_risk'] = (users_churn['days_since_last_purchase'] > churn_threshold).astype(int)

# 处理从未购买的用户
users_churn['days_since_last_purchase'] = users_churn['days_since_last_purchase'].fillna(999)
users_churn.loc[users_churn['days_since_last_purchase'] == 999, 'is_churn_risk'] = 1

print("流失风险分析:")
print(users_churn['is_churn_risk'].value_counts())
print(f"\n流失风险比例: {users_churn['is_churn_risk'].mean()*100:.2f}%")
```

### 6.2 流失因素分析

```python
# 合并更多特征
user_features = pd.merge(users_churn, rfm.reset_index()[['user_id', 'frequency', 'monetary']], 
                          on='user_id', how='left')
user_features['frequency'] = user_features['frequency'].fillna(0)
user_features['monetary'] = user_features['monetary'].fillna(0)

# 按流失风险分组分析
churn_analysis = user_features.groupby('is_churn_risk').agg({
    'age': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'user_id': 'count'
}).round(2)
churn_analysis.index = ['正常', '流失风险']
churn_analysis.columns = ['平均年龄', '平均购买次数', '平均购买金额', '用户数']
print("流失风险对比:\n", churn_analysis)

# 不同会员等级的流失率
membership_churn = user_features.groupby('membership_level')['is_churn_risk'].agg(['mean', 'count']).round(4)
membership_churn.columns = ['流失率', '用户数']
membership_churn['流失率'] = membership_churn['流失率'] * 100
print("\n会员等级流失率:\n", membership_churn)

# 城市流失率
city_churn = user_features.groupby('city')['is_churn_risk'].mean().round(4) * 100
print("\n城市流失率%:\n", city_churn.sort_values(ascending=False))
```

---

## 七、综合报告生成

### 7.1 汇总报告

```python
def generate_report():
    """生成数据分析报告"""
    report = """
================================================================================
                        电商用户行为分析报告
================================================================================

一、数据概况
------------
- 用户总数: {:,}
- 订单总数: {:,}
- 总销售额: ¥{:,.2f}
- 平均订单金额: ¥{:.2f}
- 退货率: {:.2f}%

二、用户画像
------------
1. 性别分布:
{}
2. 年龄分布:
   - 平均年龄: {:.1f}岁
   - 年龄分组: {}
3. 地域分布 TOP3:
{}
4. 会员等级分布:
{}

三、购买行为
------------
1. 产品类别销售TOP3:
{}
2. 支付方式偏好:
{}
3. 购买时间偏好:
   - 工作日占比: {:.1f}%
   - 热门时段: {}-{}点

四、用户价值分层(RFM)
--------------------
{}
金额贡献占比: {:.1f}%

五、流失预警
------------
- 流失风险用户: {} ({:.1f}%)
- 高风险会员等级: {}
- 高风险城市: {}
================================================================================
""".format(
        len(users_clean),
        len(orders_clean),
        orders_clean['order_amount'].sum(),
        orders_clean['order_amount'].mean(),
        orders_clean['is_returned'].mean() * 100,
        
        users_clean['gender'].value_counts().to_string(),
        users_clean['age'].mean(),
        users_clean['age_group'].value_counts().to_dict(),
        users_clean['city'].value_counts().head(3).to_string(),
        users_clean['membership_level'].value_counts().to_string(),
        
        category_stats.head(3).to_string(),
        payment_stats.to_string(),
        orders_clean['is_weekend'].mean() * 100,
        hourly_orders.idxmax(),
        hourly_orders.idxmax() + 1,
        
        segment_stats[['用户数', '用户占比%', '金额占比%']].to_string(),
        segment_stats.loc['重要价值客户', '金额占比%'],
        
        users_churn['is_churn_risk'].sum(),
        users_churn['is_churn_risk'].mean() * 100,
        membership_churn['流失率'].idxmax(),
        city_churn.idxmax()
    )
    return report

# 生成报告
print(generate_report())

# 保存报告
with open('user_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(generate_report())
```

### 7.2 导出分析结果

```python
# 导出用户RFM分析结果
users_with_rfm.to_csv('user_rfm_analysis.csv', index=False, encoding='utf-8-sig')
print("RFM分析结果已导出: user_rfm_analysis.csv")

# 导出用户流失风险列表
churn_risk_users = user_features[user_features['is_churn_risk'] == 1][
    ['user_id', 'age', 'gender', 'city', 'membership_level', 'frequency', 'monetary', 'days_since_last_purchase']
]
churn_risk_users.to_csv('churn_risk_users.csv', index=False, encoding='utf-8-sig')
print("流失风险用户列表已导出: churn_risk_users.csv")

# 导出产品类别销售报表
category_stats.to_csv('category_sales_report.csv', encoding='utf-8-sig')
print("产品类别销售报表已导出: category_sales_report.csv")

# 导出到Excel多sheet
with pd.ExcelWriter('analysis_results.xlsx', engine='openpyxl') as writer:
    users_with_rfm.to_excel(writer, sheet_name='用户RFM分析', index=False)
    segment_stats.to_excel(writer, sheet_name='用户分层统计')
    category_stats.to_excel(writer, sheet_name='产品类别分析')
    payment_stats.to_excel(writer, sheet_name='支付方式分析')

print("\n所有分析结果已导出到: analysis_results.xlsx")
```

---

## 八、代码封装与复用

### 8.1 分析函数封装

```python
class UserAnalyzer:
    """用户行为分析器"""
    
    def __init__(self, users_df, orders_df):
        self.users = users_df.copy()
        self.orders = orders_df.copy()
        self.users_clean = None
        self.orders_clean = None
        self.rfm = None
        
    def clean_data(self):
        """数据清洗"""
        # 用户数据清洗
        self.users_clean = self.users.copy()
        self.users_clean['age'] = self.users_clean['age'].fillna(self.users_clean['age'].median())
        self.users_clean['city'] = self.users_clean['city'].fillna(self.users_clean['city'].mode()[0])
        
        # 订单数据清洗
        self.orders_clean = self.orders.copy()
        self.orders_clean.loc[self.orders_clean['unit_price'] < 0, 'unit_price'] = self.orders_clean['unit_price'].median()
        self.orders_clean.loc[self.orders_clean['quantity'] > 20, 'quantity'] = 20
        self.orders_clean['order_amount'] = self.orders_clean['quantity'] * self.orders_clean['unit_price']
        
        return self
    
    def calculate_rfm(self, analysis_date=None):
        """计算RFM"""
        if analysis_date is None:
            analysis_date = self.orders_clean['order_date'].max() + pd.Timedelta(days=1)
        
        self.rfm = self.orders_clean.groupby('user_id').agg({
            'order_date': lambda x: (analysis_date - x.max()).days,
            'order_id': 'count',
            'order_amount': 'sum'
        })
        self.rfm.columns = ['recency', 'frequency', 'monetary']
        
        # 评分
        self.rfm['r_score'] = pd.qcut(self.rfm['recency'], q=5, labels=[5, 4, 3, 2, 1])
        self.rfm['f_score'] = pd.qcut(self.rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        self.rfm['m_score'] = pd.qcut(self.rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        self.rfm['rfm_total'] = self.rfm[['r_score', 'f_score', 'm_score']].astype(int).sum(axis=1)
        
        return self
    
    def get_summary(self):
        """获取分析摘要"""
        return {
            'total_users': len(self.users_clean),
            'total_orders': len(self.orders_clean),
            'total_revenue': self.orders_clean['order_amount'].sum(),
            'avg_order_value': self.orders_clean['order_amount'].mean(),
            'return_rate': self.orders_clean['is_returned'].mean() * 100
        }

# 使用分析器
analyzer = UserAnalyzer(users, orders)
analyzer.clean_data().calculate_rfm()
summary = analyzer.get_summary()
print("\n分析摘要:", summary)
```

---

## 九、最佳实践总结

### 9.1 数据分析流程

```python
# 数据分析标准流程
"""
1. 数据加载与探索
   - 检查数据形状、类型、缺失值
   - 查看统计描述
   - 发现异常值

2. 数据清洗
   - 处理缺失值（删除/填充）
   - 处理异常值（删除/修正）
   - 处理重复值
   - 类型转换

3. 特征工程
   - 提取时间特征
   - 创建派生特征
   - 分箱与编码

4. 数据分析
   - 单变量分析
   - 双变量分析
   - 多变量分析
   - 分组聚合

5. 可视化展示
   - 选择合适的图表类型
   - 突出关键洞察
   - 保持视觉一致性

6. 报告输出
   - 结构化报告
   - 数据导出
   - 结论建议
"""
```

### 9.2 性能优化建议

```python
# 1. 使用合适的数据类型
df_optimized = df.copy()
df_optimized['category'] = df_optimized['category'].astype('category')  # 分类数据
df_optimized['id'] = df_optimized['id'].astype('int32')  # 降低整数精度
df_optimized['price'] = df_optimized['price'].astype('float32')  # 降低浮点精度

# 2. 避免逐行操作
# 慢
for i in range(len(df)):
    df.loc[i, 'new_col'] = df.loc[i, 'a'] * 2

# 快
df['new_col'] = df['a'] * 2

# 3. 使用向量化操作
# 慢
df['text_len'] = df['text'].apply(len)

# 快
df['text_len'] = df['text'].str.len()

# 4. 合理使用分组
# 慢：多次分组
result1 = df.groupby('group')['a'].mean()
result2 = df.groupby('group')['b'].mean()

# 快：一次分组多聚合
result = df.groupby('group').agg({'a': 'mean', 'b': 'mean'})

# 5. 使用 query 进行条件过滤（大数据集更快）
filtered = df.query('age > 30 and city == "Beijing"')

# 6. 大文件分块读取
chunk_size = 100000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process(chunk)
```

---

## 总结

本文通过完整的电商用户分析案例，串联了 Pandas 的所有核心知识点：

| 阶段 | 核心技能 |
|------|----------|
| 数据探索 | `info()`, `describe()`, `head()`, 缺失值检查 |
| 数据清洗 | `fillna()`, `dropna()`, 类型转换, 异常值处理 |
| 特征工程 | 时间特征提取, 分箱, 派生特征创建 |
| 数据分析 | `groupby()`, `pivot_table()`, `merge()` |
| 可视化 | Matplotlib/Seaborn 集成 |
| 结果导出 | `to_csv()`, `to_excel()`, 报告生成 |

---

**完整系列**：
1. [NumPy 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-basic %})
2. [NumPy 进阶教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-advanced %})
3. [Pandas 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-basic %})
4. [Pandas 进阶教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-advanced %})
5. **本文**：Pandas 数据分析实战

**返回**：[AI学习路线总览]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})

*最后更新: 2026年4月12日*

> 参考资源：
> - [Pandas官方文档](https://pandas.pydata.org/docs/) - 官方完整文档
> - [Kaggle Learn - Pandas](https://www.kaggle.com/learn/pandas) - Kaggle交互式教程
> - [Python for Data Analysis](https://wesmckinney.com/book/) - Pandas作者经典书籍
> - [RFM Analysis Guide](https://www.putler.com/rfm-analysis-how-to/) - RFM分析详解
> - [Customer Segmentation](https://towardsdatascience.com/rfm-analysis-using-bigquery-ml-c459731f194) - 客户分群教程
> - [Kaggle数据科学教程](https://www.kaggle.com/learn/data-cleaning) - 数据清洗教程
> - [Python数据科学手册](https://jakevdp.github.io/PythonDataScienceHandbook/) - Jake VanderPlas
> - [Seaborn官方教程](https://seaborn.pydata.org/tutorial.html) - 数据可视化教程
> - [数据可视化最佳实践](https://www.storytellingwithdata.com/blog) - 数据叙事技巧
> - [Jupyter Notebook技巧](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/) - Jupyter使用技巧
> - [数据分析案例合集](https://github.com/donnemartin/data-science-ipython-notebooks) - IPython笔记本合集
> - [Pandas性能优化](https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6) - 性能优化指南
