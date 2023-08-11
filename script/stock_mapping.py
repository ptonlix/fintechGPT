#!/usr/bin/env python
# -*- coding:utf-8 _*-

import os
import json

dataset = './alltxt'
filelist = os.listdir(dataset)

stock_map = []
# 处理文件名分割生成json
for file in filelist:
    metalist = file.split('__')
    print(metalist)
    meta_map = {'create':metalist[0], 'name': metalist[1], "stock_code": metalist[2],
                "short_name":metalist[3], "date":metalist[4].strip('年')}
    stock_map.append(meta_map)


# 生成json文件
with open('./stock_mapping.json', 'w+') as f:
    f.write(json.dumps(stock_map))
    print("公司数据生成成功")

