import unittest

from app.demo import build_greeting


class DemoTest(unittest.TestCase):
    def test_build_greeting(self) -> None:
        self.assertEqual(build_greeting("Python"), "你好，Python！欢迎查看博客里的 Python 示例。")


if __name__ == "__main__":
    unittest.main()
