#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT_DIR/.astro-dev.pid"
LOG_FILE="$ROOT_DIR/.astro-dev.log"

cd "$ROOT_DIR"

"$ROOT_DIR/stop.sh"

if [[ ! -d node_modules ]]; then
  echo "未找到 node_modules，正在安装依赖..."
  npm install
fi

echo "正在启动 Astro 页面应用..."
nohup npm run dev >"$LOG_FILE" 2>&1 &
APP_PID=$!
echo "$APP_PID" >"$PID_FILE"

for _ in {1..30}; do
  if ! kill -0 "$APP_PID" 2>/dev/null; then
    rm -f "$PID_FILE"
    echo "页面应用启动失败，请查看日志：$LOG_FILE" >&2
    exit 1
  fi

  if curl --silent --fail --output /dev/null http://127.0.0.1:4321/; then
    echo "页面应用已启动：http://127.0.0.1:4321"
    echo "PID: $APP_PID"
    echo "日志：$LOG_FILE"
    exit 0
  fi

  sleep 1
done

echo "页面应用仍在启动，请稍后访问 http://127.0.0.1:4321"
echo "PID: $APP_PID"
echo "日志：$LOG_FILE"
