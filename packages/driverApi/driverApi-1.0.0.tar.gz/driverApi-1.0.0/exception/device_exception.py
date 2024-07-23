# author: haoliqing
# date: 2023/10/19 16:15
# desc:
from exception.properties_util import PropertiesUtil


class DeviceException(Exception):

    prop_util: PropertiesUtil = PropertiesUtil()

    def __init__(self, code: str, *params: str):
        """

        :param code:  错误码定义文件中对应的错误码
        :param param:  参数值，可输入多个参数
        """
        self.__code = code
        self.__param = params

    def __str__(self):
        code_desc = self.prop_util.get(self.__code)
        if code_desc == '':
            return "未定义异常{0},异常信息{1}".format(self.__code, str(self.__param))
        else:
            return code_desc.format(*self.__param)


if __name__ == '__main__':
    print(DeviceException('E01002', "222", "3333"))
