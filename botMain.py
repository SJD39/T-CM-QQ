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

executor = ThreadPoolExecutor(10)
app = Flask(__name__)

def run(backJson):
    # 预处理数据
    backJson = MiraiDP.MDP(backJson)
    if backJson == None:
        return ""
    backJson = json.loads(backJson)

    # 遍历信息内图片
    result = []
    for message in backJson['messages']:
        # 如果不是图片或者聊天记录
        if message['type'] != "Image":
            continue

        if message['type'] == "Image":
            # 检测图片
            malice, info, data = botQQ.checkImg(message['url'])
            if malice == True:
                result.append(info)

    if result == []:
        return ""

    botFun.sendGroupMessage(
        backJson['group']['id'], 
        [{"type": "Plain", "text": '\n'.join(result)}], 
        backJson['info']['id']
    )

    botFun.recall(
        backJson['group']['id'],
        backJson['info']['id']
    )

    # 用户记录    
    botRecord.setRecord(
        backJson['group']['id'], 
        backJson['sender']['id'], 
        "violation",
        int(
            botRecord.readRecord(
                backJson['group']['id'], 
                backJson['sender']['id'], 
                "violation"
            )
        )
        +
        1
    )

    temp = botRecord.readRecord(
        backJson['group']['id'], 
        backJson['sender']['id'], 
        "info"
    )
    temp.append(result)

    botRecord.setRecord(
        backJson['group']['id'], 
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
