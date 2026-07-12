#!/usr/bin/python3
#coding:utf-8

# pip install PyJWT== 2.10.1

import sys
import requests
import json
import os
import re
import subprocess
import time,datetime
import jwt


# ===========tb中全局参数=======================
# tb中权限比较高的一个人id
operator_id = '567f4d7c2674302859e4dc9a'
# tb中企业id
tenant_id = '5ceb7c34b59805000140b9e7'
# TB中某个应用真实的appSecret和appId
app_secret = "qR5REd3eOxBGLrAIETDY0dCLGMl3KdZH"
app_id = "6306ec3a1fabc895788fe14a"


# change-merged --change <change id> --change-url <change url> --change-owner <change owner> --change-owner-username <username> --project <project name> --branch <branch> --topic <topic> --submitter <submitter> --submitter-username <username> --commit <sha1> --newrev <sha1>
#--change  xc_app~51447  --change-url  http://192.168.110.165:8080/c/xc_app/+/51447  --change-owner  "蔡永川 <yongchuan.cai@xc-tech.com>"  --change-owner-username  yongchuan.cai  --project  xc_app  --branch  intelligent_inspection_factory  --topic    --submitter  "蔡永川 <yongchuan.cai@xc-tech.com>"  --submitter-username  yongchuan.cai  --commit  3478faeccd7f7999e7509aa09a96cdc99b825c4f  --newrev  3478faeccd7f7999e7509aa09a96cdc99b825c4f
change_merged_argv = sys.argv[1:]
xcstring = ""
xclogstring = ""
for x in change_merged_argv:
    xclogstring += str(x)
    xclogstring += "  "



def extract_fields(args):
    """
    提取所需字段：commit, submitter, change-url, project, branch。
    :param args: sys.argv[1:] 参数列表
    :return: 字典，包含提取的字段信息
    """
    fields = {
        "commit": None,
        "change-owner": None,
        "change_url": None,
        "project": None,
        "branch": None,
    }

    # 提取 commit
    if "--commit" in args:
        index = args.index("--commit")
        if index + 1 < len(args):
            fields["commit"] = args[index + 1]

    # 提取 submitter
    if "--change-owner" in args:
        index = args.index("--change-owner")
        if index + 1 < len(args):
            fields["change-owner"] = args[index + 1]

    # 提取 change-url
    if "--change-url" in args:
        index = args.index("--change-url")
        if index + 1 < len(args):
            fields["change_url"] = args[index + 1]

    # 提取 project
    if "--project" in args:
        index = args.index("--project")
        if index + 1 < len(args):
            fields["project"] = args[index + 1]

    # 提取 branch
    if "--branch" in args:
        index = args.index("--branch")
        if index + 1 < len(args):
            fields["branch"] = args[index + 1]

    return fields

def extract_commit_from_args(args):
    """
    提取 --commit 参数的值。
    :param args: sys.argv[1:] 列表
    :return: 提取的 commit 参数值。
    """
    # 将参数列表转换成字符串
    args_str = " ".join(args)

    # 匹配 --commit 后面的值
    match = re.search(r"--commit\s+(\S+)",args_str)
    if match:
        return match.group(1)  # 提取匹配的 commit 值
    return None



def read_commit_msg(commit_hash):
    """
    使用 git 命令读取指定 commit 的 commit-msg 内容
    """
    try:
        # 使用 git 命令获取 commit msg
        result = subprocess.run(
            ["git" ,"log" ,"--format=%s","-n" ,"1",commit_hash],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE ,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error reading commit message: {e.stderr}" ,  file=sys.stderr)
        sys.exit(1)


def is_valid_commit_hash(commit_hash):
    try:
        subprocess.run(
            ["git", "cat-file", "-e", commit_hash],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def gen_app_token()->str:
        # 创建payload
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        "_appId": app_id,
    }
    token = jwt.encode(payload, app_secret, algorithm="HS256")
    return token



def request_tb_task_id(short_id):
    """
    :param short_id: eg: ZZMZ-1850
    :return:
    """
    short_ids = short_id
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {gen_app_token()}",
        "X-Tenant-Type": "organization",
        "X-Tenant-Id": tenant_id
    }
    tburl = f"https://open.teambition.com/api/v3/task/query?shortIds={short_ids}"
    #print(tburl)
    #print(headers)
    try:
        response = requests.get(tburl, headers=headers, params={})
        response.raise_for_status()  # 如果请求失败，抛出异常
        body = response.json()  # 将响应内容解析为JSON格式
        print(f"获取任务:任务id:{short_ids}  响应: {body}")
        result = body.get("result")
        if not result:
            return None
        return result[0]['id']
    except requests.RequestException as e:
        print(f"获取任务信息时出错: {e}")
        return None
    pass



def request_comment_note(task_id,xcstring):
    """
    tb任务中评论内容
    :param task_id 任务id
    :param xcstring:
    :return:
    """
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {gen_app_token()}",
        "X-Tenant-Type": "organization",
        "X-Tenant-Id": tenant_id,
        "x-operator-id": operator_id
    }
    tbcommenturl = f"https://open.teambition.com/api/v3/task/{task_id}/comment"
    try:
        params = {
            'content': xcstring,
            'renderMode': 'markdown'
        }
        response = requests.post(tbcommenturl, headers=headers,data=json.dumps(params))
        response.raise_for_status()  # 如果请求失败，抛出异常
        body = response.json()  # 将响应内容解析为JSON格式
        #print(f"获取任务:任务id:{task_id}  响应: {body}")
        if body.get("code") != 200:
            return None
        #print('评论成功',body)
    except requests.RequestException as e:
        print(f"获取任务信息时出错: {e}")
        return None
    pass


def extracted_tbshort_ids(commit_msg)-> list:
    """
    解析commit内容中
    :param commit_msg: eg: [APEX][ZZMZ-1850]【ZZMZ-1959】 修改添加测试任务时创建tb任务与编译选项下计划
    :return: commit中携带的 tb_id 数组 eg: ['ZZMZ-1850','ZZMZ-1959']
    """
    # 提取英文中括号 [] 内的值
    english_brackets_result = re.findall(r'\[(.*?)]', commit_msg)
    # 提取中文中括号 【】 内的值
    chinese_brackets_result = re.findall(r'【(.*?)】', commit_msg)
    return english_brackets_result +chinese_brackets_result

dingtalkurl = 'https://oapi.dingtalk.com/robot/send?access_token=de753d0a4bffa446d1f930e99080bca3d73257e3bab3c79af7ef4ed96f2229c2'

print(sys.argv[1:])


# 提取字段
extracted_fields = extract_fields(sys.argv[1:])

# 打印提取结果
print(f"Commit: {extracted_fields['commit']}")
print(f"change-owner: {extracted_fields['change-owner']}")
print(f"Change URL: {extracted_fields['change_url']}")
print(f"Project: {extracted_fields['project']}")
print(f"Branch: {extracted_fields['branch']}")

#commit_hash = extract_commit_from_args(sys.argv[1:])

#print(commit_hash)

commit_hash = extracted_fields['commit']

print(commit_hash)

commit_msg=""
if is_valid_commit_hash(commit_hash):
    commit_msg = read_commit_msg(commit_hash)
else:
    print(f"Invalid commit hash: {commit_hash}", file=sys.stderr)


xcstring += f"change-owner: {extracted_fields['change-owner']}"+"\n"
xcstring += f"Project: {extracted_fields['project']}"+"\n"
xcstring += f"Branch: {extracted_fields['branch']}"+"\n"
xcstring += f"change_url: {extracted_fields['change_url']}"+"\n"
xcstring += f"commit_msg: {commit_msg}"+"\n"

print(xcstring)

headers = {'Content-Type': 'application/json; charset=utf-8'}
data = {
    "msgtype": "text",
    "text": {
        "content": 'Gerrit: '+xcstring
    }
}

#钉钉hooks消息
#response = requests.post(dingtalkurl, data=json.dumps(data), headers=headers)


#if response.status_code == 200:
#    print("消息发送成功")
#else:
#    print(f"消息发送失败，状态码：{response.status_code}")

#print(response.text)

# =============================================
# 解析commit中TB任务id并且评论内容
# commit_msg = '[APEX][ZZMZ-1850]【ZZMZ-1959】 修改添加测试任务时创建tb任务与编译选项下计划'
tb_short_ids = extracted_tbshort_ids(commit_msg)

#tb_short_ids=['yleb-1839'] #调试用
#py-jwt 2.9.0以上才能正常！！
for short_id in tb_short_ids:
    task_id = request_tb_task_id(short_id)
    if not task_id:
        print('不是有效id:', task_id)
        continue
    request_comment_note(task_id,xcstring)
    print('tb任务中评论完成!')

### ÈÕÖ¾ÎÄ¼þÂ·¾¶
log_file =  os.path.expanduser("~/gerrit-change-merged.log")
#
## Ð´ÈëÈÕÖ¾
with open(log_file, "a") as log:
    log.write(f"Change {xclogstring} \n")
    log.write(f"Change {xcstring} \n")
    log.write(response.text)
    log.write(f"Commit-msg for hash {commit_hash}:\n")
    log.write(commit_msg + "\n")