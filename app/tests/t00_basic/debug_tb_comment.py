#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本: 模拟传入参数测试 07_tb_comment.py
"""

import subprocess
import sys
import os
import json

# 要测试的 commit message
TEST_COMMIT_MSG = "[JRMKRD-1693]PDM中添加工模参数"


def create_test_commit(message):
    """创建一个测试 commit 并返回其 hash"""
    # 创建测试 commit (允许空提交)
    result = subprocess.run(
        ["git", "commit", "--allow-empty", "-m", message],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"创建 commit 失败: {result.stderr}")
        return None

    commit_hash = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True
    ).stdout.strip()

    return commit_hash


def main():
    # 创建测试 commit
    commit_hash = create_test_commit(TEST_COMMIT_MSG)
    if not commit_hash:
        print("无法创建测试 commit")
        return

    print(f"测试 commit message: {TEST_COMMIT_MSG}")
    print(f"测试 commit hash: {commit_hash}")

    # 构造模拟的 gerrit hook 参数
    test_args = [
        "--change", "project~1234",
        "--change-url", "http://gerrit.example.com/1234",
        "--change-owner", "Test User <test@example.com>",
        "--change-owner-username", "testuser",
        "--project", "test_project",
        "--branch", "main",
        "--topic", "",
        "--submitter", "Test User <test@example.com>",
        "--submitter-username", "testuser",
        "--commit", commit_hash,
        "--newrev", commit_hash
    ]

    print(f"\n调用命令: python 07_tb_comment.py {' '.join(test_args)}\n")

    # 使用 subprocess 运行脚本，继承当前 Python 的环境
    result = subprocess.run(
        [sys.executable, "07_tb_comment.py"] + test_args,
        capture_output=False,
        text=True
    )

    print(f"\n脚本退出码: {result.returncode}")


if __name__ == "__main__":
    main()
