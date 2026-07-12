#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT_DIR/.astro-dev.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "页面应用未运行（未找到 PID 文件）。"
  exit 0
fi

APP_PID="$(tr -d '[:space:]' <"$PID_FILE")"

if [[ ! "$APP_PID" =~ ^[0-9]+$ ]]; then
  echo "PID 文件内容无效，已清理：$PID_FILE" >&2
  rm -f "$PID_FILE"
  exit 1
fi

if ! kill -0 "$APP_PID" 2>/dev/null; then
  echo "PID ${APP_PID} 对应的进程已不存在，清理 PID 文件。"
  rm -f "$PID_FILE"
  exit 0
fi

PROCESS_CWD="$(lsof -a -p "$APP_PID" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')"
PROCESS_COMMAND="$(ps -p "$APP_PID" -o command= 2>/dev/null || true)"

if [[ "$PROCESS_CWD" != "$ROOT_DIR" ]] || [[ "$PROCESS_COMMAND" != *"npm run dev"* ]]; then
  echo "拒绝停止 PID ${APP_PID}：该进程不是本仓库的 npm run dev。" >&2
  echo "请检查并手动删除错误的 PID 文件：$PID_FILE" >&2
  exit 1
fi

echo "正在停止页面应用（PID: ${APP_PID}）..."
kill -TERM "$APP_PID"

for _ in {1..10}; do
  if ! kill -0 "$APP_PID" 2>/dev/null; then
    rm -f "$PID_FILE"
    echo "页面应用已停止。"
    exit 0
  fi
  sleep 1
done

echo "页面应用未能在 10 秒内停止，请检查 PID ${APP_PID}。" >&2
exit 1
