import unittest

import module_a.fun_1 as fun_1
import module_a.fun_2 as fun_2


class Test1(untitest.TestCase):

    def test_01(self):
        "test 1.1"
        fun_1()

    def test_02(self):
        "test 1.2"
        fun_1()


class Test2(untitest.TestCase):

    def test_01(self):
        "test 2.1"
        fun_2()

    def test_02(self):
        "test 2.2"
        fun_2()
