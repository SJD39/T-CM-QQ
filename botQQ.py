import hashlib
import hmac
import os
import sys
import json
from datetime import datetime
import requests
import time
import botFun

def getAuthorization(params, timestamp):
    # 密钥参数
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    print(secret_id)
    print(secret_key)

    service = "ims"
    host = "ims.tencentcloudapi.com"
    endpoint = "https://" + host
    region = "ap-guangzhou"
    action = "ImageModeration"
    version = "2020-12-29"
    algorithm = "TC3-HMAC-SHA256"
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(
        payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)
    print(canonical_request)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)
    print(string_to_sign)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数

    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode(
        "utf-8"), hashlib.sha256).hexdigest()
    print(signature)

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)
    print(authorization)

    print('curl -X POST ' + endpoint
          + ' -H "Authorization: ' + authorization + '"'
          + ' -H "Content-Type: application/json; charset=utf-8"'
          + ' -H "Host: ' + host + '"'
          + ' -H "X-TC-Action: ' + action + '"'
          + ' -H "X-TC-Timestamp: ' + str(timestamp) + '"'
          + ' -H "X-TC-Version: ' + version + '"'
          + ' -H "X-TC-Region: ' + region + '"'
          + " -d '" + payload + "'")
    return authorization

def checkImg(imgUrl):
    malice = False
    
    timestamp = int(time.time())

    apiUrl = "https://ims.tencentcloudapi.com"

    body = {
        "FileUrl": imgUrl,
        "Interval": 1,
        "MaxFrames": 400
    }

    headers = {
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Region": "ap-guangzhou",
        "X-TC-Version": "2020-12-29",
        "Authorization": getAuthorization(body, timestamp),
        "Content-Type": "application/json",
        "Host": "ims.tencentcloudapi.com",
        "X-TC-Action": "ImageModeration"
    }

    r = requests.post(apiUrl, data=json.dumps(body), headers=headers)

    backJson = json.loads(r.text)

    print(backJson)

    # 返回结果
    if "Error" in backJson['Response']:
        return malice, "error"
    
    
    content = "---------------"
    content = content + "\n信息类型: " + backJson['Response']['Label']
    content = content + "\n处理ID: "
    content = content + "\n详细信息: "
    for LabelResult in backJson['Response']['LabelResults']:
        if LabelResult['Suggestion'] == "Pass":
            continue
        malice = True
        content = content + "\n--命中标签: " + LabelResult['Label']
        content = content + "\n--详细标签: " + LabelResult['SubLabel']
        content = content + "\n--置信度: " + str(LabelResult['Score'])
    return malice, content, backJson
    