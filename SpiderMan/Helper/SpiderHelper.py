#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import os

BASE_PATH = os.path.abspath('../../')
CONFIG_DIR = os.path.join(BASE_PATH,'config')

class SpiderHelper(object):
    config_dir = os.path.join(BASE_PATH,'config')
    file_path = ''

    def getConfig(self,file,*args):
        file_path = os.path.join(self.config_dir, file)
        self.file_path = file_path

        '''
        层次：section -> items/option -> value
        返回值：list        dict    string/int/float
        '''

        if os.path.exists(file_path):
            cf = ConfigParser()
            cf.read(file_path)

    # def openFile(self,file):
    #     file_path = os.path.join(self.config_dir, file)
    #     self.file_path = file_path
    #     if not os.path.exists(file_path):
    #         os.(file_path,755)
    #
    #     try:
    #         f = open(file_path, 'w+')
    #         return f
    #     except Exception:
    #         if f:
    #             f.close()

    def setConfig(self,file,**kwargs):
        f = None
        file_path = os.path.join(self.config_dir, file)
        self.file_path = file_path
        cf = ConfigParser()
        cf.add_section("test")
        cf.set("test","count",'1')
        cf.add_section("test1")
        cf.set("test1","name","xiaoming")

        with open(file_path,'w+') as f:
            cf.write(f)

'''
-write(fp)                         将config对象写入至某个 .init 格式的文件  Write an .ini-format representation of the configuration state.
-add_section(section)              添加一个新的section
-set( section, option, value       对section中的option进行设置，需要调用write将内容写入配置文件 ConfigParser2
-remove_section(section)           删除某个 section
-remove_option(section, option)    删除某个 section 下的 option
'''

if __name__ == '__main__':
    print('#############')
    sh = SpiderHelper()
    sh.setConfig("bbb")
    print('#############',sh.config_dir)
    print('#############', sh.file_path)


