"""
将训练后的模型目录上传到 ModelScope（魔搭）示例。

说明：
1. 该脚本通过 git + git-lfs 推送模型文件
2. 认证使用 MODELSCOPE_TOKEN 环境变量
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"命令执行失败: {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result.stdout.strip()


def ensure_binary(cmd: str):
    if shutil.which(cmd) is None:
        raise RuntimeError(f"未找到命令 `{cmd}`，请先安装后重试。")


def ensure_repo_initialized(model_dir: Path, repo_id: str):
    if not (model_dir / ".git").exists():
        run_cmd(["git", "init", "-b", "main"], cwd=model_dir)

    # 大文件走 LFS
    run_cmd(["git", "lfs", "install"], cwd=model_dir)
    lfs_attr = model_dir / ".gitattributes"
    line = "*.pt filter=lfs diff=lfs merge=lfs -text\n"
    if lfs_attr.exists():
        content = lfs_attr.read_text(encoding="utf-8")
        if line not in content:
            lfs_attr.write_text(content + line, encoding="utf-8")
    else:
        lfs_attr.write_text(line, encoding="utf-8")

    # README 是魔搭模型页最重要的说明文件
    readme_path = model_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text(
            f"# {repo_id.split('/')[-1]}\n\n"
            "该模型由 `tests/t05_llm/01_train_tiny_llm.py` 训练得到。\n",
            encoding="utf-8",
        )


def configure_remote(model_dir: Path, repo_id: str):
    remote_url = f"https://www.modelscope.cn/{repo_id}.git"
    remotes = run_cmd(["git", "remote"], cwd=model_dir).splitlines()
    if "origin" in remotes:
        run_cmd(["git", "remote", "set-url", "origin", remote_url], cwd=model_dir)
    else:
        run_cmd(["git", "remote", "add", "origin", remote_url], cwd=model_dir)


def build_askpass_script(token: str) -> str:
    content = f"""#!/bin/sh
case "$1" in
  *Username*) echo "oauth2" ;;
  *Password*) echo "{token}" ;;
  *) echo "" ;;
esac
"""
    fd, path = tempfile.mkstemp(prefix="ms_askpass_", suffix=".sh")
    os.close(fd)
    script_path = Path(path)
    script_path.write_text(content, encoding="utf-8")
    script_path.chmod(0o700)
    return str(script_path)


def upload(model_dir: Path, repo_id: str, commit_message: str):
    ensure_binary("git")
    ensure_binary("git-lfs")

    token = os.getenv("MODELSCOPE_TOKEN", "").strip()
    if not token:
        raise RuntimeError("请先设置环境变量 MODELSCOPE_TOKEN。")

    ensure_repo_initialized(model_dir, repo_id)
    configure_remote(model_dir, repo_id)

    run_cmd(["git", "add", "."], cwd=model_dir)
    status = run_cmd(["git", "status", "--porcelain"], cwd=model_dir)
    if status:
        run_cmd(["git", "commit", "-m", commit_message], cwd=model_dir)

    askpass_script = build_askpass_script(token)
    try:
        env = os.environ.copy()
        env["GIT_ASKPASS"] = askpass_script
        env["GIT_TERMINAL_PROMPT"] = "0"
        run_cmd(["git", "push", "-u", "origin", "main"], cwd=model_dir, env=env)
    finally:
        try:
            Path(askpass_script).unlink(missing_ok=True)
        except OSError:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description="上传模型到 ModelScope（魔搭）")
    parser.add_argument(
        "--repo-id",
        required=True,
        help="魔搭模型仓库ID，格式: 用户名/仓库名",
    )
    parser.add_argument(
        "--model-dir",
        default="tests/t05_llm/outputs/tiny_llm_demo",
        help="待上传的本地模型目录",
    )
    parser.add_argument(
        "--commit-message",
        default="upload tiny llm model artifacts",
        help="提交信息",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    model_dir = Path(args.model_dir).resolve()
    if not model_dir.exists():
        raise RuntimeError(f"模型目录不存在: {model_dir}")

    upload(
        model_dir=model_dir,
        repo_id=args.repo_id,
        commit_message=args.commit_message,
    )
    print("=" * 60)
    print("上传成功")
    print(f"模型目录: {model_dir}")
    print(f"仓库地址: https://www.modelscope.cn/{args.repo_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()

