# -*- coding: utf-8 -*-

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from conf.settings import test

if __name__ == '__main__':
    test()