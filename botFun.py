import requests
import json

url = "http://localhost:5701"


def sendGroupMessage(Gid, content, quote):
    apiUrl = url + "/sendGroupMessage"
    body = {
        "quote": quote,
        "target": Gid,
        "messageChain": content
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(apiUrl, data=json.dumps(body), headers=headers)
    backJson = json.loads(r.text)
    return backJson


def sendFriendMessage(Gid, content, quote):
    apiUrl = url + "/sendFriendMessage"
    body = {
        "quote": quote,
        "target": Gid,
        "messageChain": content
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(apiUrl, data=json.dumps(body), headers=headers)
    backJson = json.loads(r.text)
    return backJson


def recall(target, messageId):
    apiUrl = url + "/recall"
    body = {
        "target": target,
        "messageId": messageId
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(apiUrl, data=json.dumps(body), headers=headers)
    backJson = json.loads(r.text)
    return backJson


def mute(target, memberId, time):
    apiUrl = url + "/mute"
    body = {
        "target": target,
        "memberId": memberId,
        "time": time
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(apiUrl, data=json.dumps(body), headers=headers)
    backJson = json.loads(r.text)
    return backJson
