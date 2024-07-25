#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2024/5/10 7:29 PM
@Desc    :  modifybody line.
"""
import json
from loguru import logger


class ModifyRules:
    """
    mj = ModifyRules()
    data = mj.get_json_value(test_json, 'location')
    pprint(data)

    mj.set_json_value(test_json, 'name', '北京市')
    pprint(test_json)

    mj.set_json_value_batch(test_json, {'name': '北京市'}, {'location': '北京市海淀区'})
    pprint(test_json)

    data = mj.replace_str_value(test_json, {'name': '北京市'}, {'location': '北京市海淀区'})
    pprint(data)
    """
    def get_json_value(self, json_data, key, json_list=None):
        """
        Recursively iterate the values corresponding to all keys in JSON, obtain the value from the key value, and output it as a list
        :param json_data:
        :param key:
        :param json_list:
        :return: json_list
        """
        # noinspection PyBroadException
        if json_list is None:
            json_list=[]
        # noinspection PyBroadException
        try:
            # 传入数据存在则存入json_list
            if key in json_data.keys():
                json_list.append(json_data[key])
            # 传入数据不符合则对其value值进行遍历
            for value in json_data.values():
                # 传入数据的value值是字典，则直接调用自身
                if isinstance(value, dict):
                    self.get_json_value(value, key, json_list)
                # 传入数据的value值是列表或者元组，则调用get_value
                elif isinstance(value, (list, tuple)):
                    self.get_value(value, key, json_list)
            return json_list
        except BaseException as e:
            logger.error('get_json_value function: {}'.format(e))

    def get_value(self, json_data, key, json_list):
        """
        Submethod: Recursively iterate the value corresponding to all keys in JSON, obtain the value from the key value, and output it as a list
        :param json_data:
        :param key:
        :param json_list:
        :return: None
        """
        for val in json_data:
            # 传入数据的value值是字典，则调用get_json_value
            if isinstance(val, dict):
                self.get_json_value(val, key, json_list)
            # 传入数据的value值是列表或者元组，则调用自身
            elif isinstance(val, (list, tuple)):
                self.get_value(val, key, json_list)

    def set_json_value(self, json_data, key, target_value):
        """
        Recursively iterate through the values corresponding to all keys in JSON and modify the values by the key values
        Only a single key is supported, and the value corresponding to all the same keys will be modified
        :param json_data:
        :param key:
        :param target_value:
        :return: json_data
        """
        # noinspection PyBroadException
        try:
            if isinstance(json_data, str):
                json_data=json.loads(json_data)
            # 传入数据存在则修改字典
            if key in json_data.keys():
                json_data[key]=target_value
            # 传入数据不符合则对其value值进行遍历
            for value in json_data.values():
                # 传入数据的value值是字典，则直接调用自身,将value作为字典传进来
                if isinstance(value, dict):
                    self.set_json_value(value, key, target_value)
                    value[key]=target_value
                # 传入数据的value值是列表或者元组，则调用set_value
                elif isinstance(value, (list, tuple)):
                    self.set_value(value, key, target_value)
            return json_data
        except BaseException as e:
            logger.error('set_json_value function: {}'.format(e))

    def set_value(self, json_data, key, target_value):
        """
        Sub-method: Recursively iterate the value corresponding to all keys in JSON, and modify the value by the key value
        :param json_data:
        :param key:
        :param target_value:
        :return: None
        """
        for val in json_data:
            # 传入数据的value值是字典，则调用get_json_value
            if isinstance(val, dict):
                self.set_json_value(val, key, target_value)
            # 传入数据的value值是列表或者元组，则调用自身
            elif isinstance(val, (list, tuple)):
                self.set_value(val, key, target_value)

    def set_json_value_batch(self, json_data, *args):
        """
        Multiple keys are supported, and the value corresponding to all the same keys will be modified
        :param json_data:
        :param args:
        :return: new_json_data
        """
        # noinspection PyBroadException
        try:
            if isinstance(args, tuple):
                if args == ():
                    return json_data
                else:
                    new_json_data=json_data
                    for arg in args:
                        for key in arg:
                            value=arg[key]
                            new_json_data=self.set_json_value(new_json_data, key, value)
                    return new_json_data
        except BaseException as e:
            logger.error('set_json_value_batch function: {}'.format(e))

    @staticmethod
    def replace_str_value(input_data, *args):
        """
        Batch replacement of values containing ${vars}, *args is dictionary format data, multiple parameters can be passed,
        suitable for request bodies in any format (json, xml, etc.)
        This function does not use self-related variables, so make this function a static method (brute force substitution)
        :param input_data:
        :param args:
        :return: new_data
        """
        # noinspection PyBroadException
        try:
            # 将传入数据强转为字符串进行替换
            new_data=str(input_data)
            for arg in args:
                for i in arg:
                    target_value=arg[i]
                    replace_value="${" + i + "}"
                    print(replace_value)
                    new_data=new_data.replace(replace_value, target_value)
            # 判断传进的数据如果为json格式,如果是就转换为json格式
            if isinstance(input_data, (list, dict)):
                return eval(new_data)
            return new_data
        except BaseException as e:
            logger.error('replace_str_value function: {}'.format(e))
