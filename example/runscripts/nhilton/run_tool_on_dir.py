import argparse
import glob
import os


from module_a.fun_1 import fun_1
from module_c.fun_4 import fun_4

from external_a.extra_fun import extra_fun


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input_dir',
        help = 'Some input dir',
    )

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        raise RuntimeError('Could not find dir: %s' % args.input_dir)

    print('Processing input dir')
    print('    in: %s' % args.input_dir)

    matches = glob.glob(os.path.join(args.input_dir, '*'))

    for m in matches:
        print('Found %s' % m)

    fun_1()
    fun_4()
    extra_fun()

    print('Processing complete!')


if __name__ == "__main__":
    main()
