#!/usr/bin/python3

###################################################################
#    File name     : tuling.py
#    Author        : doggy
#    Date          : 2018年06月02日 星期六 12时29分05秒
#    Description   : 
###################################################################

import requests
import json
import sys

TULING_API        = 'http://openapi.tuling123.com/openapi/api/v2'
TULING_KEY        = ''
DEFAULT_USER_ID   = '0'*32
DEFAULT_GROUP_ID  = '0'*64
DEFAULT_USER_NAME = 'emm...'

class Tuling(object):
    __api = TULING_API
    __errs = {
            5000:'无解析结果',
            6000:'暂不支持该功能',
            4000:'请求参数格式错误',
            4001:'加密方式错误',
            4002:'无功能权限',
            4003:'该apiKey没有可用请求次数',
            4005:'无功能权限',
            4007:'apiKey不合法',
            4100:'userId获取失败',
            4200:'上传格式错误',
            4300:'批量操作超过限制',
            4400:'没有上传合法userId',
            4500:'userId申请个数超过限制',
            4600:'输入内容为空',
            4602:'输入文本内容超过150',
            7002:'上传信息失败',
            8008:'服务器错误'
            }

    def __init__(self, key):
        self.__key = key
        self.__parser_func = {
            10003: self.__parser_news,
            10004: self.__parser_text,
            10015: self.__parser_food
            }
    
    @property
    def api(self):
        return self.__api

    @property
    def key(self):
        return self.__key

    @property
    def errs(self):
        return self.__errs

    def __post(self, **kwargs):
        text       = kwargs.pop('inputText',None)
        imgurl     = kwargs.pop('inputImage', None)
        mediaurl   = kwargs.pop('inputMedia', None)
        userid     = kwargs.pop('userId', DEFAULT_USER_ID)
        groupid    = kwargs.pop('groupId', DEFAULT_GROUP_ID)
        useridname = kwargs.pop('userIdName', DEFAULT_USER_NAME)
        
        if (text == None) and (imgurl == None) and (mediaurl == None):
            raise ValueError('You have no data to post')
            sys.exit(1)

        selfInfo = {
            "location": {
                "city"     : "厦门",
                "province" : "福建",
                "street"   : "就不告诉你街道"
                }
            }
        userInfo = {
            "apiKey"     : self.key,
            "userId"     : userid,
            "groupId"    : groupid,
            "userIdName" : useridname
            }
        perception = {
            "selfInfo": selfInfo
            }
        if text != None:
            inputText = {
                "text": text
                }
            reqType = 0
            perception['inputText'] = inputText
        if imgurl != None:
            inputImage = {
                'url': imgurl
                }
            reqType = 1 
            perception['inputImage'] = inputImage
        if mediaurl != None:
            inputMedia = {
                "url": mediaurl
                }
            reqType = 2 
            perception['inputMedia'] = inputMedia

        postdata = { 
            "perception" : perception,
            "userInfo"   : userInfo
            }
        response = requests.post(self.api, json=postdata)
        return json.loads(response.text, encoding='utf-8')
    
    def __parser_text(self, results_dict):
        return results_dict['results'][0]['values']['text']

    def __parser_news(self, results_dict):
        return_str = ''
        return_str_format = '【{0}】\n{1}\n{2}\n'
        for item in results_dict['results'][1]['values']['news']:
            return_str = return_str + return_str_format.format(item['name'],item['detailurl'],item['info'])
        return return_str

    def __parser_food(self, results_dict):
        return_str = ''
        return_str_format = '【{0}】\n{1}\n{2}\n'
        for item in results_dict['results'][1]['values']['news']:
            return_str = return_str + return_str_format.format(item['name'],item['detailurl'],item['info'])
        return return_str

    def reply(self, **kwargs):
        return_dict = self.__post(**kwargs)
        code = return_dict.pop('intent').pop('code')
        if code in self.errs.keys():
            pass
        else:
            return self.__parser_func[code](return_dict)
    

if __name__ == '__main__':
    xrobot = Tuling(TULING_KEY)
    print(xrobot.reply(inputText='红烧肉怎么做？'))
    print(xrobot.reply(inputText='你好'))
    print(xrobot.reply(inputText='今天的新闻'))










