import os
import json

initial = {
    "violation": 0,
    "info": []
}

# 预处理
def pretreatment(Gid, Uid):
    if not os.path.isdir("./data"):
        os.mkdir("./data")
    if not os.path.isdir("./data/" + str(Gid)):
        os.mkdir("./data/" + str(Gid))
    uPath = "./data/" + str(Gid) + "/" + str(Uid)
    if not os.path.isdir(uPath):
        os.mkdir(uPath)
    if not os.path.isfile(uPath + "/data.json"):
        f = open(uPath + "/data.json", "x")
        f.write(json.dumps(initial))
        f.close()
    return ""

# 读取key值
def readRecord(Gid, Uid, key):
    pretreatment(Gid, Uid)
    uPath = "./data/" + str(Gid) + "/" + str(Uid)
    f = open(uPath + "/data.json")
    temp = json.loads(f.read())[key]
    f.close()
    return temp

# 设置key值
def setRecord(Gid, Uid, key, value):
    pretreatment(Gid, Uid)
    uPath = "./data/" + str(Gid) + "/" + str(Uid)
    f = open(uPath + "/data.json", "r+")
    temp = json.loads(f.read())
    temp[key] = value
    f.seek(0)
    f.truncate(0)
    # f.write(json.dumps(temp).encode().decode())
    f.write(json.dumps(temp))
    f.close()
    return temp
