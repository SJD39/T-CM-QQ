from flask import Flask
from flask import request
import requests
import time
from concurrent.futures import ThreadPoolExecutor

import json
import os
import sys
import time

import botFun
import botQQ
import botRecord
import MiraiDP

groups = [
    681464620
]

executor = ThreadPoolExecutor(10)
app = Flask(__name__)


def run(backJson):
    # 只保留群信息
    if backJson['type'] != "GroupMessage":
        return ""

    # 如果群号不在列表内
    if backJson['sender']['group']['id'] not in groups:
        return ""

    # 遍历信息内图片
    result = []
    for messageChain in backJson['messageChain']:
        # 如果不是图片或者聊天记录
        if messageChain['type'] != "Image" and messageChain['type'] != "Forward":
            continue

        if messageChain['type'] == "Image":
            # 检测图片
            malice, info, data = botQQ.checkImg(messageChain['url'])
            if malice == True:
                result.append(info)

        if messageChain['type'] == "Forward":
            # 检测转发聊天图片
            for node in messageChain['nodeList']:
                for nodeMessageChain in node['messageChain']:
                    if nodeMessageChain['type'] != "Image":
                        continue
                    # 检测图片
                    malice, info, data = botQQ.checkImg(nodeMessageChain['url'])
                    if malice == True:
                        result.append(info)

    if result == []:
        return ""

    botFun.sendGroupMessage(
        backJson['sender']['group']['id'], 
        [{"type": "Plain", "text": '\n'.join(result)}], 
        backJson['messageChain'][0]['id']
    )

    botFun.recall(
        backJson['sender']['group']['id'],
        backJson['messageChain'][0]['id']
    )

    # 用户记录    
    botRecord.setRecord(
        backJson['sender']['group']['id'], 
        backJson['sender']['id'], 
        "violation",
        int(
            botRecord.readRecord(
                backJson['sender']['group']['id'], 
                backJson['sender']['id'], 
                "violation"
            )
        )
        +
        1
    )

    temp = botRecord.readRecord(
        backJson['sender']['group']['id'], 
        backJson['sender']['id'], 
        "info"
    )
    temp.append(result)

    botRecord.setRecord(
        backJson['sender']['group']['id'], 
        backJson['sender']['id'], 
        "info",
        temp
    )

    return ""


@app.route("/se", methods=['POST'])
def main():
    backJson = json.loads(request.get_data())
    print("----------------------------------------------------")
    print(backJson)
    # executor.submit(run(backJson))
    run(backJson)
    return ""


app.run(port=5700)
