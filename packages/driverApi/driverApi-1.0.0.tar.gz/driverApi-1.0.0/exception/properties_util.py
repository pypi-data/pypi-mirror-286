# author: haoliqing
# date: 2023/10/20 11:10
# desc:
import os
import re
import sys
import tempfile
from common import Singleton, common_utils


@Singleton
class PropertiesUtil(object):

    def __init__(self):
        self.file_name = common_utils.get_absolute_path('config/error_code/message_zh_CN.properties')
        self.properties = {}
        try:
            fopen = open(self.file_name, 'r', encoding='utf-8')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except FileNotFoundError:
            print('File is not found.')
        else:
            fopen.close()

    def has_key(self, key):
        return key in self.properties.keys()

    def get(self, key, default_value=''):
        if key in self.properties.keys():
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)


def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    # 创建临时文件
    file = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r')
        pattern = re.compile(r'' + from_regex)
        found = None
        # 读取源文件
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            # 写入临时文件
            file.write(line.encode())
        if not found and append_on_not_exists:
            file.write('\n'.encode() + to_str.encode())
        r_open.close()
        file.seek(0)

        # 读取临时文件中的所有内容
        content = file.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'w')
        # 将临时文件中的内容写入源文件
        w_open.write(content.decode())
        w_open.close()
        # 关闭临时文件，同时也会自动删除临时文件
        file.close()
    else:
        print(f'File {file_name} is not found.')
