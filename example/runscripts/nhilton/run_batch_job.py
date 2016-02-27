import module_a.fun_1 as fun_1
import module_c.fun_4 as fun_4

import external_module_a.extra_fun as extra_fun


def main():

    print('Run batch job ...')

    fun_1()
    fun_4()
    extra_fun()

    print('batch job done!')


if __name__ == "__main__":
    main()
