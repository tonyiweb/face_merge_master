# -*- coding: utf-8 -*-
# @Time    : 2018/05/08
# @Author  : WangRong

import json
import time
import youtu_tool

#配置优图
appid = '********'
secret_id = '*********************'
secret_key = '************************'
#QQ号
userid= '***********'
end_point = youtu_tool.conf.API_YOUTU_END_POINT


def getFaceDataFromYoutu(image_path):
    youtu = youtu_tool.YouTu(appid, secret_id, secret_key, userid, end_point)
    ret = youtu.DetectFace(image_path,0)
    rTemp = str(ret).replace("False","0")
    rTemp = rTemp.replace("True", "1")
    rTemp = rTemp.replace("u'", "\"")
    rTemp = rTemp.replace("'", "\"")
    return json.loads(rTemp)