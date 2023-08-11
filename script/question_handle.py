#!/usr/bin/env python
# -*- coding:utf-8 _*-

from paddlenlp import Taskflow
import json

filepath = './test_questions.jsonl'

schema = ['时间',  '公司名称']  # Define the schema for entity extraction



ie = Taskflow('information_extraction', schema=schema)

new_question_list = []
question_json_list = open(filepath).readlines()

for question_json in question_json_list:
    question = json.loads(question_json)
    ie_result = ie(question['question']) 
    for ie_one in ie_result:
        question['company'] = ie_one.get('公司名称')[0]['text'] if ie_one.get(('公司名称')) else None
        question['date'] = ie_one.get('时间')[0]['text'] if ie_one.get(('时间')) else None

    new_question_list.append(question)


# 生成json文件
with open('./new_test_questions.json', 'w+') as f:
    f.write(json.dumps(new_question_list, ensure_ascii=False))
    print("公司数据生成成功")
