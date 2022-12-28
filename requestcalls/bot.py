import requests
from dotenv import load_dotenv
import os

load_dotenv()

dt_key = os.getenv("DT_API")

def send_ding(tix,title,sdnames,sdwhatsya,sdnumber,sdlastouch,sdnameoff,sdlasttouch,status,tminutes,tseconds):
    

    ding_token = dt_key
    sdnumbr = '+63-'+str(sdnumber)
    sdwhat = sdwhatsya
    sdstatus = sdlastouch
    tixstatus = status

    if sdwhat == "New":

        tixnum = tix
        title = title
        wut = sdwhat
  


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
                'content': f'****{wut} OFM ticket \n\nTicket: {tixnum}\n\nTitle: {title}\n\nStatus: {tixstatus}\nOn Que: {tminutes}m {tseconds}s\nPlease get the ticket',
            },
        }
        response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
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
                'content': f'****{wut} OFM ticket\n\nTicket: {tixnum}\n\nTitle: {title}\n\nStatus: {tixstatus}\n\nOwner: {owners}\n\nOn Que: {tminutes}m {tseconds}s',
            },
            }
            response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
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
                'content': f'****{wut} OFM ticket\n\nTicket: {tixnum}\n\nTitle: {title}\n\nStatus: {tixstatus}\n\nOwner: {sdnameoff} ~~NOT AVAILABLE~~\nLast Handler: {sdnames}\n\nOn Que: {tminutes}m {tseconds}s',
            },
            }
            response = requests.post('https://oapi.dingtalk.com/robot/send', params=params, headers=headers, json=json_data)
            return print(response)


