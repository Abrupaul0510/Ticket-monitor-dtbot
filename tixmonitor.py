import time
import requests
import pandas as pd
import re
from requestcalls.getdata import get_task_order
from requestcalls.bot import send_ding,send_ding_error2
import datetime
from dotenv import load_dotenv
import os
import gspread
from win10toast import ToastNotifier
import pprint

toaster = ToastNotifier()
#LOAD .env file
load_dotenv()

#intialize session needed data from ENV
name = os.getenv("NNAME")
sapp = os.getenv("SAPP")
bothost = os.getenv("BOTHOST")

def check_ticket_count():

    cookies =  {}
 
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '669fc550-0ba9-4d60-ad2b-f18e0498a038',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryOrderByParam',
        'operator': '',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryOrderByParam","p0":"{\\"operationType\\":\\"mytask-todo\\",\\"sortList\\":[],\\"staffId\\":26009,\\"partyId\\":26009,\\"partyOrgId\\":12012,\\"workOrderTitle\\":\\"\\",\\"timeoutFlag\\":\\"01\\",\\"pageIndex\\":1,\\"pageSize\\":20,\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    rawdata = response.json()

    resultdata = rawdata

    return resultdata['resultData']


def checknget_owner(sdstaffid,filterstatus):

    cfile = "C:\\Users\\Paul Abrugar\\Desktop\\Ticket-monitor-dtbot\\paul-monitoring-c738e35dd511.json"

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


def get_all_available(filterstatus):

    cfile = "C:\\Users\\Paul Abrugar\\Desktop\\Ticket-monitor-dtbot\\paul-monitoring-c738e35dd511.json"

    gc = gspread.service_account(cfile)
    
    sh = gc.open('dutypol')

    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()

    df = pd.DataFrame(data)


    data = df[df['SD.Status'] == filterstatus]

    my_dict = data.to_dict(orient = 'records')


    sdnumber = [d['SD.Number'] for d in my_dict]



    allavail = []
    for items in sdnumber:
        sdnum = "+63-"+str(items)
        allavail.append(str(sdnum))



    return allavail


def tixmonitor():

    count = False
    while True:

        tixcountres = check_ticket_count()

        # print(tixcountres)
        tixcount = tixcountres['rows']
        # print(len(tixcount))
        if len(tixcount) == 0:
            __ignore_ = "None"
            # print(__ignore_)
        else:
            count = True

        if count == True:
            for item in tixcountres['rows']:
                tix = item['orderCode']
                tixstart = item['publicDate']          
                date_str = tixstart
                format_str = "%Y-%m-%d %H:%M:%S"
                date = datetime.datetime.strptime(date_str, format_str)
                now = datetime.datetime.now()
                difference = now - date
                tminutes = int(difference.total_seconds() // 60)
                tseconds = int(difference.total_seconds() % 60)
                tixnum = tix
                duration = str(tminutes)+"Minutes "+str(tseconds)+"Seconds"
                print(tixnum+" - "+duration)

                bothostcheck = item['partyName'].strip()
                if bothostcheck == bothost:
                    tixnum = tix
                    duration = str(tminutes)+"Minutes "+str(tseconds)+"Seconds"
                    # toaster.show_toast(
                    #     tixnum,
                    #    duration,
                    #     duration=5,  # (optional) Specify the time in seconds for the notification to disappear
                    # )
                    print(tixnum+" - "+duration)
                    
                else:
                    tixnum = tix
 

           
                    date_str = tixstart
                    
                    format_str = "%Y-%m-%d %H:%M:%S"

                    date = datetime.datetime.strptime(date_str, format_str)
                    print(date)
                    now = datetime.datetime.now()

                    # Calculate the difference between the two dates
                    difference = now - date

                    tminutes = int(difference.total_seconds() // 60)
                    tseconds = int(difference.total_seconds() % 60)


                    # pprint.pprint(samp)
                    domain = item['systemDomain']
                    system = item['system']
                    title = str(item['orderTitle'])
                    domaindata = {
                            'tdomain' : domain,
                            'system' : system,
                            'title' : str(title),
                        }
                    status = item['tacheName'] #STATUS
                    orderId = item['orderId'] #HANDLER ORG
                    shardingKey = item['shardingKey']
                    title = item['orderTitle']
                        
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
                        allavail = ""


                        if sdstatusowner == "Available":
                            res = send_ding(tix,sdname,sdwhat,sdnumber,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,allavail)
        
                            if sdstatusowner == "Not Available":
                                # pprint.pprint(taskdata)
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
 

                                result = checknget_owner(sdstaffid,filterstatus='Not Available')
                                sdnameoff = result.get('Name')

                                sdnames = ""
                                res = send_ding(tix,name,sdwhat,number,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,allavail)
                                print(res)
                    else:
                        print("NEW TICKET!")
                        sdwhat = "New"
                        sdnames = ""
                        sdnumber= ""
                        sdstatusowner=" "
                        sdnameoff = ""
                        sdlasttouch = ""
                        # GET all available
                        allavail = get_all_available(filterstatus='Available')
                        res = send_ding(tix,sdnames,sdwhat,sdnumber,sdstatusowner,sdnameoff,sdlasttouch,status,tminutes,tseconds,domaindata,allavail)
                        print(res)
                            
                        
            print("Monitoring OSS My Task....")
            time.sleep(30)
            count = False
        time.sleep(3)



def startMonitoring():
    while True:
        try:
            print('Monitoring OSS My Task....')
            tixmonitor()
        except Exception as err:
            print(err)
            send_ding_error2(err)
            time.sleep(30)


startMonitoring()
