import json

# 单图片Mirai http输出
# {
#     'type': 'GroupMessage', 
#     'messageChain': [
#         {
#             'type': 'Source', 
#             'id': 3798, 
#             'time': 1677480328
#         }, 
#         {
#             'type': 'Image', 
#             'imageId': '{12AF81EC-0C20-7E8E-F8EB-D0053F9E2BE1}.jpg', 
#             'url': 'http://gchat.qpic.cn/gchatpic_new/3069935480/681464620-2335228282-12AF81EC0C207E8EF8EBD0053F9E2BE1/0?term=255&is_origin=0', 
#             'path': None, 
#             'base64': None, 
#             'width': 539, 
#             'height': 960, 
#             'size': 64644, 
#             'imageType': 'JPG', 
#             'isEmoji': False
#         }
#     ], 
#     'sender': {
#         'id': 3069935480, 
#         'memberName': '三九刀', 
#         'specialTitle': '', 
#         'permission': 'MEMBER', 
#         'joinTimestamp': 1627228692, 
#         'lastSpeakTimestamp': 1677480329, 
#         'muteTimeRemaining': 0, 
#         'group': {
#             'id': 681464620, 
#             'name': 'qq机器人测试群', 
#             'permission': 'OWNER'
#         }
#     }
# }
#  转发聊天记录
# {
#     'type': 'GroupMessage', 
#     'messageChain': [
#         {
#             'type': 'Source', 
#             'id': 3805, 
#             'time': 1677549579
#         }, 
#         {
#             'type': 'Forward', 
#             'display': None, 
#             'nodeList': [
#                 {
#                     'senderId': 1072711234, 
#                     'time': 1677485866, 
#                     'senderName': '徐子亭（博爱版）', 
#                     'messageChain': [
#                         {
#                             'type': 'Image', 
#                             'imageId': '{1E4883B7-65EA-73AF-7C4E-E94599B7D995}.mirai', 
#                             'url': 'http://gchat.qpic.cn/gchatpic_new/0/0-0-1E4883B765EA73AF7C4EE94599B7D995/0?term=2', 
#                             'path': None, 
#                             'base64': None, 
#                             'width': 1920, 
#                             'height': 886, 
#                             'size': 149325, 
#                             'imageType': 'UNKNOWN', 
#                             'isEmoji': False
#                         }
#                     ], 
#                     'messageId': None, 
#                     'messageRef': None
#                 }, 
#                 {
#                     'senderId': 1840560616, 
#                     'time': 1677487732, 
#                     'senderName': '萝卜', 
#                     'messageChain': [
#                         {
#                             'type': 'Image', 
#                             'imageId': '{AE816DF3-EFA0-47EE-A09E-A5E1773C4B54}.mirai', 
#                             'url': 'http://gchat.qpic.cn/gchatpic_new/0/0-0-AE816DF3EFA047EEA09EA5E1773C4B54/0?term=2', 
#                             'path': None, 
#                             'base64': None, 
#                             'width': 1920, 
#                             'height': 886, 
#                             'size': 116169, 
#                             'imageType': 'UNKNOWN', 
#                             'isEmoji': False
#                         }
#                     ], 
#                     'messageId': None, 
#                     'messageRef': None
#                 }
#             ]
#         }
#     ], 
#     'sender': {
#         'id': 3069935480, 
#         'memberName': '三九刀', 
#         'specialTitle': '', 
#         'permission': 'MEMBER', 
#         'joinTimestamp': 1627228692, 
#         'lastSpeakTimestamp': 1677549579, 
#         'muteTimeRemaining': 0, 
#         'group': {
#             'id': 681464620, 
#             'name': 'qq机器人测试群', 
#             'permission': 'OWNER'
#         }
#     }
# }

def MDP(inJson):
    with open('./config.json') as f:
        config = json.load(f)
    
    if inJson['type'] != "GroupMessage":
        return None

    # 判断信息是否来源于指定的群
    for taskList in config['taskList']:
        if taskList[0] == inJson['sender']['group']['id']:
            break
    else:
        return None

    outJson = {}

    # info
    info = {}
    info['id'] = inJson['messageChain'][0]['id']
    info['time'] = inJson['messageChain'][0]['time']

    # group
    group = {}
    group['id'] = inJson['sender']['group']['id']
    group['name'] = inJson['sender']['group']['name']
    group['permission'] = inJson['sender']['group']['permission']

    # sender
    sender = {}
    sender['id'] = inJson['sender']['id']
    sender['memberName'] = inJson['sender']['memberName']
    sender['permission'] = inJson['sender']['permission']

    # message
    messages = []
    for message in inJson['messageChain']:
        if message['type'] == "Image":
            temp = {}
            temp['type'] = message['type']
            temp['imageId'] = message['imageId']
            temp['url'] = message['url']
            temp['width'] = message['width']
            temp['height'] = message['height']
            temp['size'] = message['size']
            temp['imageType'] = message['imageType']
            temp['isEmoji'] = message['isEmoji']
            messages.append(temp)
            continue
        elif message['type'] == "Forward":
            for node in message['nodeList']:
                for forwardMessage in node['messageChain']:
                    if forwardMessage['type'] == "Image":
                        temp = {}
                        temp['type'] = forwardMessage['type']
                        temp['imageId'] = forwardMessage['imageId']
                        temp['url'] = forwardMessage['url']
                        temp['width'] = forwardMessage['width']
                        temp['height'] = forwardMessage['height']
                        temp['size'] = forwardMessage['size']
                        temp['imageType'] = forwardMessage['imageType']
                        temp['isEmoji'] = forwardMessage['isEmoji']
                        messages.append(temp)
                        continue
        elif message['type'] == 'Plain':
            temp = {}
            temp['type'] = message['type']
            temp['text'] = message['text']
            messages.append(temp)
            continue

    outJson['group'] = group
    outJson['sender'] = sender
    outJson['messages'] = messages
    outJson['info'] = info

    print(json.dumps(outJson, ensure_ascii=False))
    return json.dumps(outJson, ensure_ascii=False)
# 输出
# {
#     "group": {
#         "id": 681464620, 
#         "name": "qq机器人测试群", 
#         "permission": "OWNER"
#     }, 
#     "sender": {
#         "id": 3069935480, 
#         "memberName": "三九刀", 
#         "permission": "MEMBER"
#     }, 
#     "messages": [
#         {
#             "type": "Image", 
#             "imageId": "{12AF81EC-0C20-7E8E-F8EB-D0053F9E2BE1}.jpg", 
#             "url": "http://gchat.qpic.cn/gchatpic_new/3069935480/681464620-2156135152-12AF81EC0C207E8EF8EBD0053F9E2BE1/0?term=255&is_origin=0", 
#             "width": 539, 
#             "height": 960, 
#             "size": 64644, 
#             "imageType": "JPG", 
#             "isEmoji": false
#         }, 
#         {
#             "type": "Image", 
#             "imageId": "{12AF81EC-0C20-7E8E-F8EB-D0053F9E2BE1}.jpg", 
#             "url": "http://gchat.qpic.cn/gchatpic_new/3069935480/681464620-2156135152-12AF81EC0C207E8EF8EBD0053F9E2BE1/0?term=255&is_origin=0", 
#             "width": 539, 
#             "height": 960, 
#             "size": 64644, 
#             "imageType": "JPG", 
#             "isEmoji": false
#         }
#     ]
# }