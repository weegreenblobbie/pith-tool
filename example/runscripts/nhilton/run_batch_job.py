import argparse

from module_a.fun_1 import fun_1
from module_c.fun_4 import fun_4

from external_a.extra_fun import extra_fun


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input_txt_file',
        help = 'Some input file',
    )

    args = parser.parse_args()

    print('Running batch job ...')

    with open(args.input_txt_file, 'r') as fd:
        text = fd.read()

    print('Read "%s" from file' % repr(text))

    fun_1()
    fun_4()
    extra_fun()

    print('batch job complete!')


if __name__ == "__main__":
    main()
