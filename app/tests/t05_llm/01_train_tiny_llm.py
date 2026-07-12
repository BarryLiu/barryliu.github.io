"""
Tiny LLM 训练示例（纯 PyTorch）
学习目标：
1. 跑通“指令数据 -> 训练 -> 保存模型”闭环
2. 产出可用于上传到 ModelScope（魔搭）的模型目录
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset


ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "datas" / "sft_train_zh.jsonl"
OUTPUT_DIR = ROOT_DIR / "outputs" / "tiny_llm_demo"

PAD_TOKEN = "<pad>"
BOS_TOKEN = "<bos>"
EOS_TOKEN = "<eos>"


@dataclass
class TrainConfig:
    max_seq_len: int = 128
    batch_size: int = 4
    epochs: int = 30
    lr: float = 2e-3
    embed_dim: int = 128
    n_heads: int = 4
    n_layers: int = 2
    dropout: float = 0.1
    seed: int = 42


class CharTokenizer:
    """字符级分词器，便于教学演示，不依赖外部库。"""

    def __init__(self, stoi: Dict[str, int], itos: Dict[int, str]):
        self.stoi = stoi
        self.itos = itos

    @classmethod
    def from_texts(cls, texts: List[str]) -> "CharTokenizer":
        vocab = sorted(set("".join(texts)))
        tokens = [PAD_TOKEN, BOS_TOKEN, EOS_TOKEN] + vocab
        stoi = {ch: idx for idx, ch in enumerate(tokens)}
        itos = {idx: ch for ch, idx in stoi.items()}
        return cls(stoi=stoi, itos=itos)

    @property
    def pad_id(self) -> int:
        return self.stoi[PAD_TOKEN]

    @property
    def bos_id(self) -> int:
        return self.stoi[BOS_TOKEN]

    @property
    def eos_id(self) -> int:
        return self.stoi[EOS_TOKEN]

    @property
    def vocab_size(self) -> int:
        return len(self.stoi)

    def encode(self, text: str) -> List[int]:
        return [self.stoi[BOS_TOKEN]] + [self.stoi[ch] for ch in text] + [self.stoi[EOS_TOKEN]]

    def decode(self, token_ids: List[int]) -> str:
        chars = []
        for token_id in token_ids:
            ch = self.itos[token_id]
            if ch in (PAD_TOKEN, BOS_TOKEN, EOS_TOKEN):
                continue
            chars.append(ch)
        return "".join(chars)

    def save(self, path: Path) -> None:
        payload = {"stoi": self.stoi}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class SFTDataset(Dataset):
    """构造自回归训练样本：input_ids 与 next-token labels。"""

    def __init__(self, rows: List[Dict[str, str]], tokenizer: CharTokenizer, max_seq_len: int):
        self.samples: List[torch.Tensor] = []
        for row in rows:
            prompt = row["instruction"].strip()
            answer = row["response"].strip()
            text = f"### 指令\n{prompt}\n\n### 回答\n{answer}"
            token_ids = tokenizer.encode(text)[:max_seq_len]
            if len(token_ids) < 2:
                continue
            self.samples.append(torch.tensor(token_ids, dtype=torch.long))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> torch.Tensor:
        return self.samples[idx]


def collate_batch(batch: List[torch.Tensor], pad_id: int, max_seq_len: int):
    batch_size = len(batch)
    x = torch.full((batch_size, max_seq_len - 1), pad_id, dtype=torch.long)
    y = torch.full((batch_size, max_seq_len - 1), -100, dtype=torch.long)

    for i, ids in enumerate(batch):
        ids = ids[:max_seq_len]
        input_ids = ids[:-1]
        labels = ids[1:]
        length = min(len(input_ids), max_seq_len - 1)
        x[i, :length] = input_ids[:length]
        y[i, :length] = labels[:length]

    return x, y


class TinyCausalLM(nn.Module):
    """极简 Transformer Causal LM。"""

    def __init__(
        self,
        vocab_size: int,
        max_seq_len: int,
        embed_dim: int,
        n_heads: int,
        n_layers: int,
        dropout: float,
    ):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Embedding(max_seq_len, embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=n_heads,
            dim_feedforward=embed_dim * 4,
            dropout=dropout,
            batch_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.norm = nn.LayerNorm(embed_dim)
        self.lm_head = nn.Linear(embed_dim, vocab_size)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        batch, seq_len = input_ids.shape
        positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch, -1)
        hidden = self.token_embed(input_ids) + self.pos_embed(positions)

        # Causal mask: 上三角为 True，表示不可见
        mask = torch.triu(torch.ones(seq_len, seq_len, device=input_ids.device), diagonal=1).bool()
        hidden = self.encoder(hidden, mask=mask)
        hidden = self.norm(hidden)
        return self.lm_head(hidden)


def load_rows(data_path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for line in data_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        rows.append({"instruction": obj["instruction"], "response": obj["response"]})
    return rows


def generate_text(
    model: TinyCausalLM,
    tokenizer: CharTokenizer,
    prompt: str,
    max_new_tokens: int,
    device: torch.device,
    max_seq_len: int,
) -> str:
    model.eval()
    ids = tokenizer.encode(prompt)
    ids = ids[:-1]  # 去掉 prompt 的 eos，避免过早终止

    with torch.no_grad():
        for _ in range(max_new_tokens):
            input_ids = torch.tensor([ids[-(max_seq_len - 1):]], dtype=torch.long, device=device)
            logits = model(input_ids)
            next_id = int(torch.argmax(logits[0, -1]).item())
            ids.append(next_id)
            if next_id == tokenizer.eos_id:
                break
    return tokenizer.decode(ids)


def save_artifacts(model: TinyCausalLM, tokenizer: CharTokenizer, config: TrainConfig, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_path = output_dir / "model.pt"
    tokenizer_path = output_dir / "tokenizer.json"
    config_path = output_dir / "config.json"
    model_card_path = output_dir / "README.md"

    torch.save(model.state_dict(), checkpoint_path)
    tokenizer.save(tokenizer_path)
    config_payload = {
        "model_type": "tiny-causal-lm",
        "vocab_size": tokenizer.vocab_size,
        "max_seq_len": config.max_seq_len,
        "embed_dim": config.embed_dim,
        "n_heads": config.n_heads,
        "n_layers": config.n_layers,
        "dropout": config.dropout,
    }
    config_path.write_text(json.dumps(config_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    model_card = (
        "# tiny-llm-demo\n\n"
        "这是一个用于教学的极简中文字符级 Causal LM（PyTorch）。\n\n"
        "## 文件说明\n"
        "- `model.pt`: 训练后的权重\n"
        "- `tokenizer.json`: 字符词表\n"
        "- `config.json`: 模型结构配置\n\n"
        "## 训练数据\n"
        "来自 `tests/t05_llm/datas/sft_train_zh.jsonl`，仅用于演示端到端流程。\n\n"
        "## 使用限制\n"
        "该模型规模很小，只适合作为训练与发布流程示例，不适合生产任务。\n"
    )
    model_card_path.write_text(model_card, encoding="utf-8")


def main():
    print("=" * 60)
    print("Tiny LLM 训练示例（可衔接 ModelScope 上传）")
    print("=" * 60)

    config = TrainConfig()
    torch.manual_seed(config.seed)

    rows = load_rows(DATA_PATH)
    all_texts = [
        f"### 指令\n{row['instruction']}\n\n### 回答\n{row['response']}"
        for row in rows
    ]
    tokenizer = CharTokenizer.from_texts(all_texts)
    dataset = SFTDataset(rows=rows, tokenizer=tokenizer, max_seq_len=config.max_seq_len)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyCausalLM(
        vocab_size=tokenizer.vocab_size,
        max_seq_len=config.max_seq_len,
        embed_dim=config.embed_dim,
        n_heads=config.n_heads,
        n_layers=config.n_layers,
        dropout=config.dropout,
    ).to(device)

    loader = DataLoader(
        dataset,
        batch_size=config.batch_size,
        shuffle=True,
        collate_fn=lambda batch: collate_batch(batch, tokenizer.pad_id, config.max_seq_len),
    )

    optimizer = optim.AdamW(model.parameters(), lr=config.lr)
    criterion = nn.CrossEntropyLoss(ignore_index=-100)

    print(f"训练样本数: {len(dataset)}")
    print(f"词表大小: {tokenizer.vocab_size}")
    print(f"设备: {device}")
    print("开始训练...\n")

    model.train()
    for epoch in range(config.epochs):
        epoch_loss = 0.0
        for x, y in loader:
            x = x.to(device)
            y = y.to(device)
            logits = model(x)
            loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.item())

        avg_loss = epoch_loss / max(1, len(loader))
        ppl = math.exp(min(10.0, avg_loss))
        print(f"Epoch [{epoch + 1}/{config.epochs}] Loss: {avg_loss:.4f} | PPL: {ppl:.2f}")

    save_artifacts(model=model, tokenizer=tokenizer, config=config, output_dir=OUTPUT_DIR)
    print("\n模型已保存到:", OUTPUT_DIR)

    demo_prompt = "### 指令\n请解释什么是过拟合。\n\n### 回答\n"
    demo_text = generate_text(
        model=model,
        tokenizer=tokenizer,
        prompt=demo_prompt,
        max_new_tokens=80,
        device=device,
        max_seq_len=config.max_seq_len,
    )
    print("\n推理示例：")
    print("-" * 60)
    print(demo_text)
    print("-" * 60)

    print("\n下一步：")
    print("1) 准备魔搭仓库（例如 yourname/tiny-llm-demo）")
    print("2) 设置环境变量: export MODELSCOPE_TOKEN=你的token")
    print(
        "3) 运行上传脚本: python tests/t05_llm/02_upload_to_modelscope.py "
        "--repo-id yourname/tiny-llm-demo --model-dir tests/t05_llm/outputs/tiny_llm_demo"
    )


if __name__ == "__main__":
    main()

