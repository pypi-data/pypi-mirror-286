import sys
import unittest


sys.path.append("../graceful")


from graceful.graceful import Graceful


class TestGraceful(unittest.TestCase): ...


if __name__ == "__main__":
    unittest.main()
