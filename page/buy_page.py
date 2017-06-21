# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from pyse.init_pyse import Pyse

class Buy(Pyse):
    def __init__(self,driver):
        self.driver = driver
