#!/usr/bin/env python
# -*- coding:utf-8 _*-

from paddlenlp import Taskflow


schema = ['时间',  '选手',  '赛事名称']  # Define the schema for entity extraction

ie = Taskflow('information_extraction', schema=schema)

print(ie("2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！"))  # Better print results using pprint