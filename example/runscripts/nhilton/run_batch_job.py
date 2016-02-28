from module_a.fun_1 import fun_1
from module_c.fun_4 import fun_4

from external_a.extra_fun import extra_fun


def main():

    print('Running batch job ...')

    fun_1()
    fun_4()
    extra_fun()

    print('batch job complete!')


if __name__ == "__main__":
    main()
