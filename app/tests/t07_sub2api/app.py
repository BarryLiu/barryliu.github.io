#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sub2API 钉钉跳板服务
作用：承接钉钉公网请求，内网代理调用 Sub2API，实现 API Key 自动创建与下发
安全原则：Sub2API 管理员 Token 仅存于此服务，不暴露给钉钉或公网
"""

import os
import sys
import json
import secrets
import logging
import hashlib
import hmac
import base64
import urllib.parse
import subprocess
from datetime import datetime, timezone
from typing import Optional, Tuple

import requests
import csv
from flask import Flask, request, jsonify

# =============================================================================
# 初始化
# =============================================================================
app = Flask(__name__)

CONFIG_PATH = os.environ.get("CONFIG_PATH", "./config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# 日志
log_level = getattr(logging, CONFIG.get("logging", {}).get("level", "INFO"), logging.INFO)
log_file = CONFIG.get("logging", {}).get("file", "./dingtalk-bridge.log")
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Sub2API 配置
SUB2API_BASE = CONFIG["sub2api"]["base_url"]
ADMIN_API_KEY = CONFIG["sub2api"]["admin_api_key"]
ADMIN_HEADERS = {
    "x-api-key": ADMIN_API_KEY,
    "Content-Type": "application/json",
}

# 数据库配置（通过 docker exec 操作）
DB_CONTAINER = CONFIG["database"]["container_name"]
DB_USER = CONFIG["database"]["user"]
DB_PASSWORD = CONFIG["database"]["password"]
DB_NAME = CONFIG["database"]["dbname"]

# 钉钉配置
DINGTALK_WEBHOOK = CONFIG.get("dingtalk", {}).get("webhook_url", "")
DINGTALK_SECRET = CONFIG.get("dingtalk", {}).get("secret", "")

# 分组映射
NAME_GROUP_MAP = CONFIG.get("name_group_map", {})
DEFAULT_GROUP = CONFIG.get("default_group", {"group_id": 3, "group_name": "kimi"})

# API Key 默认归属用户（所有 Key 都挂在这个用户下，便于管理员统一管理）
DEFAULT_KEY_OWNER_USER_ID = CONFIG.get("default_key_owner_user_id", 1)

# API Key 默认值
KEY_DEFAULTS = CONFIG.get("api_key_defaults", {})

# 加载钉钉通讯录，建立 姓名 -> userId 映射
DINGTALK_USER_MAP = {}
CONTACTS_CSV_PATH = os.path.join(os.path.dirname(CONFIG_PATH), "dingtalk_contacts.csv")
try:
    with open(CONTACTS_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if len(row) >= 2:
                name = row[0].strip()
                user_id = row[1].strip()
                if name and user_id:
                    DINGTALK_USER_MAP[name] = user_id
    # 建立 userId -> 姓名 反向映射
    USER_ID_TO_NAME_MAP = {v: k for k, v in DINGTALK_USER_MAP.items()}
    logger.info(f"Loaded {len(DINGTALK_USER_MAP)} contacts from dingtalk_contacts.csv")
except Exception as e:
    logger.warning(f"Failed to load dingtalk_contacts.csv: {e}")
    USER_ID_TO_NAME_MAP = {}


# =============================================================================
# 工具函数
# =============================================================================

def generate_api_key() -> str:
    """生成 Sub2API 格式的 API Key：sk- + 64 位 hex"""
    return "sk-" + secrets.token_hex(32)


def _escape_sql_param(val) -> str:
    """安全转义 SQL 字符串参数"""
    if val is None:
        return "NULL"
    if isinstance(val, (int, float)):
        return str(val)
    return "'" + str(val).replace("'", "''") + "'"


def run_sql(query: str, params: tuple = ()) -> Tuple[bool, list]:
    """
    通过 docker exec 执行 PostgreSQL 查询
    使用 sg docker 确保 docker 组权限可用
    返回: (success, rows_or_error_message)
    """
    try:
        # 安全嵌入参数：替换占位符 $1, $2...
        safe_query = query
        for i, p in enumerate(params, 1):
            safe_query = safe_query.replace(f"${i}", _escape_sql_param(p))

        # 通过 sg docker 执行 docker 命令，确保权限
        # -F 后的制表符直接在 Python 字符串中嵌入真实 tab 字符
        tab = "\t"
        docker_cmd = f'docker exec -i {DB_CONTAINER} psql -U {DB_USER} -d {DB_NAME} -t -A -F"{tab}" -c "{safe_query}"'
        cmd = ["sg", "docker", "-c", docker_cmd]
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        if result.returncode != 0:
            err = result.stderr.strip() if result.stderr else "unknown error"
            logger.error(f"SQL error: {err}")
            return False, [err]
        lines = [line for line in result.stdout.strip().split("\n") if line]
        rows = [line.split("\t") for line in lines]
        return True, rows
    except Exception as e:
        logger.error(f"SQL execution exception: {str(e)}")
        return False, [str(e)]


def get_user_by_username(username: str) -> Optional[dict]:
    """根据 username（即申请人姓名）查询用户"""
    ok, rows = run_sql(
        "SELECT id, email, username, status FROM users WHERE username = $1 AND deleted_at IS NULL",
        (username,),
    )
    if not ok or not rows:
        return None
    row = rows[0]
    return {
        "id": int(row[0]),
        "email": row[1],
        "username": row[2],
        "status": row[3],
    }


def get_api_key_by_name(user_id: int, name: str) -> Optional[dict]:
    """查询指定用户下 name 相同的有效 API Key"""
    ok, rows = run_sql(
        "SELECT id, key, name, group_id, status, quota FROM api_keys WHERE user_id = $1 AND name = $2 AND deleted_at IS NULL",
        (user_id, name),
    )
    if not ok or not rows:
        return None
    row = rows[0]
    return {
        "id": int(row[0]),
        "key": row[1],
        "name": row[2],
        "group_id": int(row[3]) if row[3] else None,
        "status": row[4],
        "quota": row[5],
    }


def get_api_keys_by_user_id(user_id: int) -> list:
    """查询用户的有效 API Keys"""
    ok, rows = run_sql(
        "SELECT id, key, name, group_id, status, quota FROM api_keys WHERE user_id = $1 AND deleted_at IS NULL",
        (user_id,),
    )
    if not ok:
        return []
    keys = []
    for row in rows:
        keys.append({
            "id": int(row[0]),
            "key": row[1],
            "name": row[2],
            "group_id": int(row[3]) if row[3] else None,
            "status": row[4],
            "quota": row[5],
        })
    return keys


def create_api_key_in_db(user_id: int, name: str, group_id: int) -> Tuple[bool, str]:
    """
    直接在数据库中创建 API Key
    返回: (success, key_or_error)
    """
    new_key = generate_api_key()
    quota = KEY_DEFAULTS.get("quota", 10000000)
    rl_5h = KEY_DEFAULTS.get("rate_limit_5h", 0)
    rl_1d = KEY_DEFAULTS.get("rate_limit_1d", 600)
    rl_7d = KEY_DEFAULTS.get("rate_limit_7d", 0)

    query = """
    INSERT INTO api_keys (
        user_id, key, name, group_id, status,
        quota, quota_used,
        rate_limit_5h, rate_limit_1d, rate_limit_7d,
        usage_5h, usage_1d, usage_7d,
        created_at, updated_at
    ) VALUES (
        $1, $2, $3, $4, 'active',
        $5, 0,
        $6, $7, $8,
        0, 0, 0,
        NOW(), NOW()
    )
    RETURNING key
    """
    ok, rows = run_sql(query, (user_id, new_key, name, group_id, quota, rl_5h, rl_1d, rl_7d))
    if not ok or not rows:
        return False, rows[0][0] if rows else "insert failed"
    return True, rows[0][0]


def create_sub2api_user(username: str, email: str, password: str) -> Tuple[bool, dict]:
    """调用 Sub2API 管理接口创建用户"""
    try:
        payload = {
            "email": email,
            "password": password,
            "username": username,
            "role": "user",
            "balance": 0,
            "concurrency": 5,
        }
        resp = requests.post(
            f"{SUB2API_BASE}/api/v1/admin/users",
            headers=ADMIN_HEADERS,
            json=payload,
            timeout=10,
        )
        data = resp.json()
        if data.get("code") == 0:
            return True, data.get("data", {})
        logger.error(f"Create user failed: {data}")
        return False, data
    except Exception as e:
        logger.error(f"Create user exception: {str(e)}")
        return False, {"message": str(e)}


def resolve_group(name: str) -> dict:
    """根据申请人姓名匹配分组"""
    if name in NAME_GROUP_MAP:
        return NAME_GROUP_MAP[name]
    logger.warning(f"Name '{name}' not found in name_group_map, using default group")
    return DEFAULT_GROUP


def make_dingtalk_sign(timestamp: str, secret: str) -> str:
    """钉钉加签算法"""
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return urllib.parse.quote_plus(base64.b64encode(hmac_code))


def send_dingtalk_message(user_id: str, title: str, content: str) -> bool:
    """发送钉钉工作通知（如果配置了 webhook）"""
    if not DINGTALK_WEBHOOK:
        logger.info("DingTalk webhook not configured, skipping notification")
        return False

    try:
        timestamp = str(int(datetime.now(timezone.utc).timestamp() * 1000))
        url = DINGTALK_WEBHOOK
        if DINGTALK_SECRET:
            sign = make_dingtalk_sign(timestamp, DINGTALK_SECRET)
            url = f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content,
            },
        }
        resp = requests.post(url, json=payload, timeout=10)
        result = resp.json()
        if result.get("errcode") == 0:
            logger.info(f"DingTalk message sent successfully")
            return True
        logger.error(f"DingTalk send failed: {result}")
        return False
    except Exception as e:
        logger.error(f"DingTalk send exception: {str(e)}")
        return False


# =============================================================================
# API 路由
# =============================================================================

@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/dingtalk/create-key", methods=["POST"])
def create_key():
    """
    核心接口：钉钉自动化调用此接口创建 API Key
    请求体：{"name": "申请人姓名"}
    返回：HTTP 始终 200，用 JSON code 区分业务状态：
      - code=0:  创建成功 {"code": 0, "data": {"key": "sk-...", "group_name": "...", "is_new": true}}
      - code=409: 重复申请 {"code": 409, "data": {"key": "sk-...", "group_name": "...", "is_new": false}}
      - code=400/500: 参数错误或系统异常
    """
    try:
        req_data = request.get_json(force=True) or {}
        user_name = req_data.get("name", "").strip()
        submitter = req_data.get("submitter", "").strip()
        submitter_name = USER_ID_TO_NAME_MAP.get(submitter, submitter)

        if not user_name:
            return jsonify({"code": 400, "msg": "申请人姓名不能为空"}), 200

        logger.info(f"Received create-key request for name='{user_name}', submitter='{submitter_name}'")

        # ---------------------------------------------------------------
        # Step 1: 重复申请校验（检查默认用户下是否已有同名 Key）
        # ---------------------------------------------------------------
        owner_user_id = DEFAULT_KEY_OWNER_USER_ID
        existing_key = get_api_key_by_name(owner_user_id, user_name)
        if existing_key and existing_key["status"] == "active":
            group_info = resolve_group(user_name)
            exist_key = existing_key["key"]
            logger.info(f"Duplicate request: user='{user_name}', submitter='{submitter_name}', existing_key={exist_key[:20]}...")
            return jsonify({
                "code": 409,
                "msg": "重复申请",
                "data": {
                    "key": exist_key,
                    "group_name": group_info.get("group_name", ""),
                    "is_new": False,
                    "user_id": DINGTALK_USER_MAP.get(user_name, ""),
                    "submitter": submitter,
                },
            }), 200

        # ---------------------------------------------------------------
        # Step 2: 匹配分组
        # ---------------------------------------------------------------
        group_info = resolve_group(user_name)
        group_id = group_info["group_id"]
        group_name = group_info.get("group_name", "")
        logger.info(f"Matched group: id={group_id}, name={group_name}")

        # ---------------------------------------------------------------
        # Step 3: 创建 API Key（挂在默认用户下，便于管理员统一管理）
        # ---------------------------------------------------------------
        ok, new_key = create_api_key_in_db(owner_user_id, user_name, group_id)
        if not ok:
            logger.error(f"Create API Key failed: {new_key}")
            return jsonify({"code": 500, "msg": f"创建 API Key 失败: {new_key}"}), 200

        logger.info(f"Created API Key for user='{user_name}', submitter='{submitter_name}': {new_key[:20]}...")

        # ---------------------------------------------------------------
        # Step 4: 返回结果
        # ---------------------------------------------------------------
        return jsonify({
            "code": 0,
            "msg": "success",
            "data": {
                "key": new_key,
                "group_name": group_name,
                "is_new": True,
                "user_id": DINGTALK_USER_MAP.get(user_name, ""),
                "submitter": submitter,
            },
        })

    except Exception as e:
        logger.exception("Unhandled exception in create_key")
        return jsonify({"code": 500, "msg": f"服务异常: {str(e)}"}), 200


@app.route("/dingtalk/notify", methods=["POST"])
def dingtalk_notify():
    """
    可选接口：直接发送钉钉通知（供钉钉自动化备用）
    请求体：{"user_id": "钉钉UserID", "title": "标题", "content": "markdown内容"}
    """
    try:
        req_data = request.get_json(force=True) or {}
        user_id = req_data.get("user_id", "")
        title = req_data.get("title", "")
        content = req_data.get("content", "")
        if not all([user_id, title, content]):
            return jsonify({"code": 400, "msg": "参数不完整"}), 400
        ok = send_dingtalk_message(user_id, title, content)
        return jsonify({"code": 0 if ok else 500, "msg": "ok" if ok else "send failed"})
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500


# =============================================================================
# 启动
# =============================================================================

if __name__ == "__main__":
    # 开发模式：Flask 内置服务器
    app.run(host="0.0.0.0", port=9000, debug=False)
