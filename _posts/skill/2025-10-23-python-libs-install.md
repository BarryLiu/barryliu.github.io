##  记录一下python下面各种依赖同步方式与虚拟环境维护方式







### 同步方式



* pip 
* vu 
* pyproject
* 







| **venv + pip** | `python -m venv` | `requirements.txt`                  | `pip install -r requirements.txt`    | 标准库，简单但功能弱             |
| -------------- | ---------------- | ----------------------------------- | ------------------------------------ | -------------------------------- |
| **Poetry**     | 内置（自动创建） | `pyproject.toml`                    | `poetry install`                     | 一体化，推荐现代项目             |
| **PDM**        | 内置或系统       | `pyproject.toml`(PEP 621)           | `pdm install`                        | 新一代，兼容标准                 |
| **Pipenv**     | 内置             | `Pipfile`                           | `pipenv install`                     | 曾流行，现逐渐被 Poetry/PDM 取代 |
| **uv + venv**  | 手动或脚本       | `pyproject.toml`/`requirements.txt` | `uv pip install -r requirements.txt` | 超快安装，新兴工具               |





### pip



``` python
# 创建
python -m venv .venv

# 激活（Linux/macOS）
source .venv/bin/activate
# 激活（Windows）
.venv\Scripts\activate

# 退出
deactivate

```



``` python

# 安装依赖
pip install -r requirements.txt

# 导出当前环境依赖
pip freeze > requirements.txt
```







### **Poetry**







