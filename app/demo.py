"""Small uv-managed demo used by the Python content article."""


def build_greeting(name: str) -> str:
    """Return a greeting that can be reused by scripts and notebooks."""
    return f"你好，{name}！欢迎查看博客里的 Python 示例。"


def main() -> None:
    print(build_greeting("想飞的鱼"))


if __name__ == "__main__":
    main()

