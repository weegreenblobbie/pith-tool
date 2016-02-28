import unittest

from module_a.fun_1 import fun_1
from module_a.fun_2 import fun_2


class Test1(unittest.TestCase):

    def test_01(self):
        "test 1.1"
        fun_1()

    def test_02(self):
        "test 1.2"
        fun_1()


class Test2(unittest.TestCase):

    def test_01(self):
        "test 2.1"
        fun_2()

    def test_02(self):
        "test 2.2"
        fun_2()
