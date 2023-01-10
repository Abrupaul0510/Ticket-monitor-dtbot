import requests
from dotenv import load_dotenv
import os

load_dotenv()

dt_key = os.getenv("DT_API")
dt_key_checker = os.getenv("DT_API_CHECKER")
bot_host = os.getenv("NNAME")

def send_ding(tix,sdnames,sdwhatsya,sdnumber,sdlastouch,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata):
    title = domaindata['title']
    domain = domaindata['tdomain']
    system = domaindata['sytem']

    ding_token = dt_key
    sdnumbr = '+63-'+str(sdnumber)
    sdwhat = sdwhatsya
    sdstatus = sdlastouch
    tixstatus = status

    if sdwhat == "New":

        tixnum = tix

        wut = sdwhat
        title = domaindata['title']
        domain = domaindata['tdomain']
        sytem = domaindata['sytem']
  


        headers = {
            'Content-Type': 'application/json',
        }

        params = {
            'access_token': ding_token,
        }

        json_data = {
                    "at": {
                "atMobiles":[
                    ""  
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'[{wut}] OFM Ticket \n\nTicket: {tixnum}\n\nTitle: {title}\n\nSystem Domain: {domain}\nSystem:{system}\n\nStatus: {tixstatus}\nOn Que: {tminutes}m {tseconds}s\nPlease get the ticket\n\nBotHost:{bot_host}',
            },
        }
        response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
        return print(response)



    if sdwhat == "Existing":
        tixnum = tix
        title = title
        owners = sdnames
        wut = sdwhat
        
  

        if sdstatus == "Available":

            headers = {
            'Content-Type': 'application/json',
        }

            params = {
            'access_token': ding_token,
        }

            json_data = {
                    "at": {
                "atMobiles":[
                    sdnumbr
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'[{wut}] OFM Ticket 1.2\n\nTicket: {tixnum}\n\nTitle: {title}\n\nSystem Domain: {domain}\nSystem:{system}\n\n\Status: {tixstatus}\n\nOwner: {owners}\n\nOn Que: {tminutes}m {tseconds}s\n\nBotHost:{bot_host}',
            },
            }
            response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=5)
            return print(response)


        if sdstatus == "Not Available":

            headers = {
            'Content-Type': 'application/json',
        }

            params = {
            'access_token': ding_token,
        }

            json_data = {
                    "at": {
                "atMobiles":[
                    sdnumbr
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content': f'[{wut}] OFM Ticket 1.2\n\nTicket: {tixnum}\n\nTitle: {title}\nSystem Domain: {domain}\nSystem: {system}\n\nStatus: {tixstatus}\n\nOwner: {sdnameoff} ~~NOT AVAILABLE~~\nLast Handler: {sdnames}\n\nOn Que: {tminutes}m {tseconds}s\n\nBotHost:{bot_host}',
            },
            }
            response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
            return print(response)



def send_ding_open_tix(stringdata,stringdata2,data):
    headers = {
            'Content-Type': 'application/json',
        }

    params = {
            'access_token': dt_key_checker,
    # https://oapi.dingtalk.com/robot/send?access_token=491833b0fb23152ca7c951a354bce0efcc79d009945cf391089b43d08c9e620e Sample Changed
        }

    json_data = {
                    "at": {
                "atMobiles":[
                    ""  
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(data['mention'])
            },
            'msgtype': 'text',
            'text': {
                'content': data['date']+'\n\n--TEST--\nAll Open Tickets OFM \n'+stringdata+'\n\n\nWrong Flow:\n'+stringdata2+'\n\n\n\nRuntime: '+str(data['runtime']),
            },
        }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
    return print(response)



def send_ding_error(_error_):
    headers = {
            'Content-Type': 'application/json',
        }

    params = {
            'access_token': dt_key_checker,
    # https://oapi.dingtalk.com/robot/send?access_token=0440438cefcd8450062bd8fc6ba5c47f9c9da4898fc08246ca7ce9e165c20d58 Changed
        }

    json_data = {
                    "at": {
                "atMobiles":[
                    # "+63-9176136917","+63-9503358322","+63-9684100886","+63-9064474450","+63-9956286051"
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": bool(False)
            },
            'msgtype': 'text',
            'text': {
                'content':'OFM\n\n'+_error_,
            },
        }
    response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data,timeout=120)
    return print(response)