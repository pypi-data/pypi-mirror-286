# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 12:00 下午
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : test_yaml.py
import os

from ruamel.yaml import YAML

from ultipa_unitest.test_write import wrapper
yaml = YAML(typ='safe')
class ReadYaml:

    @staticmethod
    @wrapper
    def readYaml(filename, dataName):
        yaml_path = os.path.abspath(filename)
        with open(yaml_path, encoding='utf-8') as f:
            data = yaml.load(f)
            return data


if __name__ == '__main__':
    red = ReadYaml()
    ret = red.readYaml("/Users/ultipa/work/ultipa-integration-testing-python/intergration_tests/auto_tests/write_tests/insertNode_data.yaml",None)
    print(ret)