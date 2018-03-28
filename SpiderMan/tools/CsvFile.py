#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pandas as pd
import os


class CsvFile():
    path = ''
    reader = None

    def __init__(self,path):
        self.path = path
        self.reader = pd.read_table(self.getListFiles(path)[0], sep=',', chunksize=1)

    def getListFiles(self):
        path = self.path
        assert os.path.isdir(path), '%s not exist.' % path
        ret = []
        for root, dirs, files in os.walk(path):
            print
            '%s, %s, %s' % (root, dirs, files)
            for filespath in files:
                ret.append(os.path.join(root, filespath))
        return ret