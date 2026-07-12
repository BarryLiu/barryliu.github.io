# t05_llm：模型训练与上传魔搭

这个包用于演示一个最小可运行的“训练 -> 产物保存 -> 上传 ModelScope（魔搭）”闭环。

> 说明：这里使用纯 PyTorch 实现了一个教学版 Tiny Causal LM，重点在流程闭环，而不是模型效果。

## 目录结构

```text
tests/t05_llm/
├── __init__.py
├── README.md
├── 01_train_tiny_llm.py          # 训练脚本（生成模型产物）
├── 02_upload_to_modelscope.py    # 上传脚本（推送到魔搭）
├── datas/
│   └── sft_train_zh.jsonl        # 示例SFT数据
└── outputs/
    └── tiny_llm_demo/            # 训练后自动生成
```

## 你会得到什么

运行训练脚本后，`tests/t05_llm/outputs/tiny_llm_demo` 下会生成：

- `model.pt`：模型参数
- `tokenizer.json`：字符词表
- `config.json`：模型结构配置
- `README.md`：模型卡（上传后展示在模型页）

## 环境准备

### 1) Python依赖

项目已经有 `torch` 依赖，可直接运行。

### 2) 上传依赖

上传到魔搭需要本机安装：

- `git`
- `git-lfs`

macOS 安装示例：

```bash
brew install git git-lfs
git lfs install
```

## 运行步骤

### 第一步：训练模型

```bash
python tests/t05_llm/01_train_tiny_llm.py
```

### 第二步：准备魔搭仓库

先在 [ModelScope 官网](https://www.modelscope.cn/) 创建一个模型仓库，例如：

- `yourname/tiny-llm-demo`

并在个人设置里生成 Access Token。

### 第三步：上传到魔搭

```bash
export MODELSCOPE_TOKEN="你的token"
python tests/t05_llm/02_upload_to_modelscope.py \
  --repo-id yourname/tiny-llm-demo \
  --model-dir tests/t05_llm/outputs/tiny_llm_demo
```

成功后可在下列地址查看：

- `https://www.modelscope.cn/yourname/tiny-llm-demo`

## 数据格式（JSONL）

`datas/sft_train_zh.jsonl` 每行一个 JSON 对象：

```json
{"instruction":"请解释什么是机器学习。","response":"机器学习是让计算机通过数据自动学习规律的方法。"}
```

你可以替换成自己的业务数据，只需保持 `instruction/response` 字段即可。

## 常见问题

- 上传报 401：通常是 `MODELSCOPE_TOKEN` 无效或权限不足
- 上传报 git-lfs 错误：确认已执行 `git lfs install`
- 训练很慢：当前脚本走教学小模型，建议先用 CPU 跑通流程再扩展

