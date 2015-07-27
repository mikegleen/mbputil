"""

Move the files in the per-day subdirectories to a single directory for the
year.

"""

from __future__ import print_function
import argparse
import os.path
import re
import shutil
__author__ = 'mlg'


def getparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('year')
    return parser


def getargs():
    parser = getparser()
    args = parser.parse_args()
    return args


def trace(level, msg):
    if level <= _args.verbose:
        print(msg)


def main(args):
    names = os.listdir('.')
    year = args.year
    try:
        os.mkdir(year)
    except OSError as ex:
        trace(1, 'Failed to make directory {}:\n{}'.format(year,
                                                           ex.strerror))
        # Ok if directory already exists
    for name in names:
        m = re.match(year + '_(\d\d)_(\d\d)', name)
        if not m:
            trace(2, 'Skipping {} (No match)'.format(name))
            continue
        mmdd = m.group(1) + m.group(2)
        subdir = os.listdir(name)
        for subname in subdir:
            if subname.startswith('.'):
                trace(2, 'Skipping {} (Hidden File)'.format(os.path.join(name,
                                                                     subname)))
                continue
            target = os.path.join(year, mmdd + '_' + subname)
            if os.path.exists(target):
                trace(2, 'Skipping {} (Target exists)'.format(
                    os.path.join(name, subname)))
                continue
            source = os.path.join(name, subname)
            trace(1, 'Copying {} -> {}'.format(source, target))
            shutil.copy(source, target)

if __name__ == '__main__':
    _args = getargs()
    main(_args)
