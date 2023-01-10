import time
import requests
import pandas as pd
import re
from requestcalls.getdata import get_tix_details,get_task_order
from requestcalls.bot import send_ding
import datetime
from dotenv import load_dotenv
import os
import gspread



#LOAD .env file
load_dotenv()

#intialize session needed data from ENV
name = os.getenv("NNAME")
sapp = os.getenv("SAPP")

def check_ticket_count(cookiesverfied):



    cookies =  {'SESSION': str(cookiesverfied)}
 

    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
 
    'Referer': 'https://portal.dito.ph/portal-web/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'X-CSRF-TOKEN': 'd7743bb9-72ca-4625-a753-e525c91c4acf',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    params = {
    'terminal': '2',
    '_': '',
}

    response = requests.get('https://portal.dito.ph/portal-web/centerTodoList/all', params=params, cookies=cookies, headers=headers)
  
    return response.json()


def checknget_owner(sdstaffid,filterstatus):

    cfile = "paul-monitoring-c738e35dd511.json"

    gc = gspread.service_account(cfile)
    
    sh = gc.open('dutypol')

    ###https://docs.google.com/spreadsheets/d/195PrVSPkEjvpvctcBP99vlVCOxD5QEmE7fp9YjFEDxE

    worksheet = sh.get_worksheet(0)

# read the data into a Pandas DataFrame
    data = worksheet.get_all_records()

# create a Pandas DataFrame from the data
    df = pd.DataFrame(data)


    data = df[df['SD.Status'] == filterstatus]

    #GETTING ALL DATA ===Second line in records format
    my_dict = data.to_dict(orient = 'records')

    #Extracting only ticket number with SL status
    sdid = [d['SD.Id'] for d in my_dict]
    sdname = [d['SD.Name'].strip() for d in my_dict]
    sdnumber = [d['SD.Number'] for d in my_dict]
    sdstatus = [d['SD.Status'].strip() for d in my_dict]



    dataSD = {}
    for i, (j, k, s) in zip(sdid, zip(sdname, sdnumber, sdstatus)):
        dataSD[i] = (j, k,s)  


    # print(dataSD)
    if sdstaffid in dataSD:
        name, number, status = dataSD[sdstaffid]
        return {'Status': status,
                'Name' : name,
                'Number' : number}

    else:
        return {'Status': "Not Available",
                'Name' : "",
                'Number' : ""}


def get_initial_session():
    cookies = {
    'bss3_portal_index': '1',
    'HTML_VERSION': '1672449694815',
    'ZSMART_LOCALE': 'en',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'image/avif,image/webp,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://portal.dito.ph/portal-web/',
        # 'Cookie': 'bss3_portal_index=1; HTML_VERSION=1672449694815; ZSMART_LOCALE=en',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
}

    responsecok = requests.get(
        'https://portal.dito.ph/portal-web/portal/LoginController/vcode.do?1672449751153',
        cookies=cookies,
        headers=headers,
    )
    

    return responsecok.cookies.get("SESSION")


def compelete_session():

    cookiesnotverify = get_initial_session()
    print('You are now login with SESSION ID: ',cookiesnotverify)


    cookies = {
    'bss3_portal_index': '1',
    'HTML_VERSION': '1672451500104',
    'ZSMART_LOCALE': 'en',
    'SESSION': str(cookiesnotverify),
    'areaId': '1',
    'userId': '',
    'orgId': '',
    'CLOUD_APP_NAME': 'DITO_BSS_pot-uportal-core',
    'CLOUD_APP_ID': '322',
    'pageno': 'MHwx',
}

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://portal.dito.ph',
    'Connection': 'keep-alive',
    'Referer': 'https://portal.dito.ph/portal-web/',
    # 'Cookie': 'bss3_portal_index=1; HTML_VERSION=1672451500104; ZSMART_LOCALE=en; SESSION=fd626db755d; areaId=1; userId=26009; orgId=12012; CLOUD_APP_NAME=DITO_BSS_pot-uportal-core; CLOUD_APP_ID=322; pageno=MHwx',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

    data = {
    'userCode': str(name),
    'password': str(sapp),
    'verifyCode': '',
    'clientType': '1000',
    'loginWay': 'password',
    'showVcode': 'false',
}

    responselog = requests.post(
    'https://portal.dito.ph/portal-web/portal/LoginController/login.do',
    cookies=cookies,
    headers=headers,
    data=data,
)
    
    result = responselog.json()
    return result['sessionId']


def tixmonitor(cookiesverfied):

    count = False
    while True:

        tixcountres = check_ticket_count(cookiesverfied)

        ##### FOR TEST TICKET
        # tixcountres = {
        #     'OSSB':[
        #         {  
        #         'date': '2022-12-19 21:09:05',
        #         'creator': 'Weicong Shi',
        #         'ticketType': 'IT Service Request',
        #         'terminal': '1',
        #         'title': 'Delete data of pac batch-20SLZ01071309 Bacoor IPRAN A  PAC 2022-12-19',
        #         'url': 'oss_core/ofm/modules/pto/workorder/views/newEngineeringCollaborationWorkOrderIng?todoFlag=Y&ticketType=RFT&packageId=1578625789908&orderCode=INT20221228000020&workOrderId=3411081'   
        #         },
        #         #  {  
        #         # 'date': '2022-12-19 21:09:05',
        #         # 'creator': 'Weicong Shi',
        #         # 'ticketType': 'IT Service Request',
        #         # 'terminal': '1',
        #         # 'title': 'Delete data of pac batch-20SLZ01071309 Bacoor IPRAN A  PAC 2022-12-19',
        #         # 'url': 'oss_core/ofm/modules/pto/workorder/views/newEngineeringCollaborationWorkOrderIng?todoFlag=Y&ticketType=RFT&packageId=1578625789908&orderCode=INT20221219000009&workOrderId=3411081'   
        #         # },
        #         ]
        #         }
        # # print(tixcountres)
        tixcount = tixcountres
        if len(tixcount) == 0:
            paul = "meron"
        else:
            count = True

        if count == True:
            print("Send DING DING")
            for item in tixcountres['OSSB']:
                tixlong = item['url']

                tixstart = item['date']
                                
                date_str = tixstart

                format_str = "%Y-%m-%d %H:%M:%S"

                date = datetime.datetime.strptime(date_str, format_str)
                print(date)
                now = datetime.datetime.now()

                # Calculate the difference between the two dates
                difference = now - date

                tminutes = int(difference.total_seconds() // 60)
                tseconds = int(difference.total_seconds() % 60)


                result = re.search(r'orderCode=([^&]+)', str(tixlong))
                if result:
                    ticketnum = result.group(1)
                    print(ticketnum)
                    resdata = get_tix_details(ticketnum)
                    # pprint.pprint(resdata)
                    samp = resdata['resultData']['rows'][0]

                    # pprint.pprint(samp)
                    domain = samp['systemDomain']
                    system = samp['system']
                    title = samp['orderTitle']
                    domaindata = {
                        'tdomain' : domain,
                        'system' : system,
                        'title' : title
                    }
                    tix = samp['orderCode'] #TIXNUM
                    status = samp['tacheName'] #STATUS
                    orderId = samp['orderId'] #HANDLER ORG
                    shardingKey = samp['shardingKey']
                    title = samp['orderTitle']
                    
                    # print(tix, orderId, shardingKey, status, title) 
                    detailed = get_task_order(str(orderId),str(shardingKey))
                    taskdata = detailed['resultData']
                    # pprint.pprint(detailed)




                    pos = -1
                    for i,item in enumerate(taskdata):
                        if item.get('operOrgName') == 'Stratnet' and item.get('operTypeName') == 'Check Out':
                                pos = i
                                break
                    
                    if pos >= 0:
                        print(f"Existing {pos}")
                        sdwhat = "Existing"
                        sdnameoff = ""
                        sdlasttouch = ""
                        # GET OWNER   staffId
                        sdstaffid = taskdata[pos]['operStaffId']
                        owner_excel = checknget_owner(sdstaffid,filterstatus='Available')
                        sdstatusowner = owner_excel.get('Status')
                        sdname = owner_excel.get('Name')
                        sdnumber = owner_excel.get('Number')

                        # to_ding = [{
                        #     'Ticket Number': tix, 
                        #     'Ticket Title': title,
                        #     'SD_Name': sdname,
                        #     'age': 30,
                        #     'age': 30,
                        #     'age': 30,
                        #     'age': 30,
                        #     'age': 30,
                        #     'age': 30,
                        #     'age': 30,
                        #     'age': 30,
                        #     }]

                        if sdstatusowner == "Available":
                            res = send_ding(tix,sdname,sdwhat,sdnumber,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata)
    
                        if sdstatusowner == "Not Available":
                            # pprint.pprint(taskdata)
                            print("Nont")
                            sdtouch = []
                            newtats = []
                            sdowner = "Off Duty or On Break"
                            for i,item in enumerate(taskdata):
                                if item.get('operOrgName') == 'Stratnet' and item.get('operTypeName') == 'Check Out':

                                    staffID = item.get('operStaffId')
                                    # print(staffID)
                                    dataSD = checknget_owner(staffID,filterstatus='Available')
                                    
                                    if dataSD.get('Name') != '':
                                        SDcnumber = dataSD.get('Number')
                                        SDname = dataSD.get('Name')

                                        # print(SDid,SDname)

                                        newdata = SDname
                                        sorting = str(i)
                                        sdtouchtrim2 = newdata.strip()

                                        dataappend =   { 
                                            "id": sorting,        
                                            "name": SDname,        
                                            "number": SDcnumber}

                                        newtats.append(dataappend)

                                    sdtouchtrim = item.get('operStaffName').strip()
                                    sdtouch.append(sdtouchtrim)

                            # print(newtats)

                            unique_names = {d['name']: d for d in newtats}
                            sorted_names = sorted(unique_names.values(), key=lambda x: x['id'])
                            names_and_numbers = [(d['name'], d['number']) for d in sorted_names]

                            if len(names_and_numbers) == 0:
                                name = "~~NONE~~"
                                number = ""
                            else: 
                                name, number = names_and_numbers[-1]
                                print(name)
                                print(number)

                            result = checknget_owner(sdstaffid,filterstatus='Not Available')
                            sdnameoff = result.get('Name')

                            sdnames = ""
                            # print(sdnameoff)
                            res = send_ding(tix,name,sdwhat,number,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata)
                            print(res)

                    else:
                        print("NEW TICKET!")
                        sdwhat = "New"
                        noowner = "None"
                        sdnames = ""
                        sdnumber= ""
                        sdstatusowner=" "
                        sdnameoff = ""
                        sdlasttouch = ""
                        # GET all available
                        owner_excel = checknget_owner(sdstaffid,filterstatus='Available')
                        sdstatusowner = owner_excel.get('Status')
                        sdname = owner_excel.get('Name')
                        sdnumber = owner_excel.get('Number')
                        res = send_ding(tix,sdnames,sdwhat,sdnumber,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata)
                        print(res)
                            
                        
            print("60 second cooldown")
            time.sleep(30)
            count = False
        time.sleep(3)




#START Monitor
cookiesverfied = compelete_session()
print('Monitoring your OFM To Do List....')
tixmonitor(cookiesverfied)

