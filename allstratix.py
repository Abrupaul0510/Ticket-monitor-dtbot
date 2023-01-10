import time
import datetime
import calendar
from dateutil import parser
import requests
from requestcalls.bot import send_ding_open_tix, send_ding_error
from requestcalls.getdata import get_task_order, get_tix_details


start_time = time.time()

header_all = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://portal.dito.ph',
        'Referer': 'https://portal.dito.ph/portal-web/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'f1e33406-dd30-44f3-b88f-f5ae196fc29c',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

def get_all_open_int():


    cookies = {
        '_tt_enable_cookie': '1',
    }

    headers = header_all

    data = {
        'serviceName': 'ptoOrderServiceBean',
        'methodName': 'queryOrderMonitorList',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"UNFINISHED\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"\\",\\"packageId\\":1578625789908,\\"pageIndex\\":1,\\"colName\\":\\"\\",\\"orderType\\":\\"asc\\",\\"pageSize\\":20,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=200
    )


    rawdata = response.json()

    resultdata = rawdata.get('resultData')
    numrows = resultdata.get('total')

    data = []
    for page in range(1, numrows+1):
        while True:
            try:
                resultbypage = get_record_by_page(page)
                data.extend(resultbypage)
                break
            except ConnectionError as _er_ror_:
                print(_er_ror_)

    dataInt = []
    for items in data:
        if items.get('orderStateName') == 'Processing':
            
            detailed = get_task_order(
                str(items.get('orderId')), str(items.get('shardingKey')))
            taskdata = detailed['resultData']

            for task in taskdata:
                if task.get('operOrgName') == 'Stratnet' and task.get('operTypeName') == 'Check Out':
                    dataInt.append(items.get('orderCode'))

    dats = set(dataInt)
    return dats


def get_record_by_page(page):

    cookies = {
        '_tt_enable_cookie': '1',
    }

    headers = header_all

    data = {
        'serviceName': 'ptoOrderServiceBean',
        'methodName': 'queryOrderMonitorList',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"UNFINISHED\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"\\",\\"packageId\\":1579139505552,\\"pageIndex\\":'+str(page)+',\\"colName\\":\\"\\",\\"orderType\\":\\"asc\\",\\"pageSize\\":20,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=200)


    rawdata = response.json()

    resultdata = rawdata.get('resultData')

    return resultdata.get('rows')

def get_record_by_page_srt(page):

    cookies = {
        '_tt_enable_cookie': '1',
    }

    headers = header_all

    data = {
        'serviceName': 'ptoOrderServiceBean',
        'methodName': 'queryOrderMonitorList',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"UNFINISHED\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"\\",\\"packageId\\":1578625789908,\\"pageIndex\\":'+str(page)+',\\"pageSize\\":20,\\"resetPage\\":true,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=200)

    # print(response.json())

    rawdata = response.json()

    resultdata = rawdata.get('resultData')

    return resultdata.get('rows')

def parse_date(month_string):
    return parser.parse(month_string)

def get_all_open_srt():
    cookies = {
        '_tt_enable_cookie': '1',
    }

    headers = header_all

    data = {
        'serviceName': 'ptoOrderServiceBean',
        'methodName': 'queryOrderMonitorList',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"UNFINISHED\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"\\",\\"packageId\\":1578625789908,\\"pageIndex\\":1,\\"pageSize\\":20,\\"resetPage\\":true,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=200)


    rawdata = response.json()


    resultdata = rawdata.get('resultData')
    numrows = resultdata.get('total')

    data = []
    for page in range(1, numrows+1):
        while True:
            try:
                resultbypage = get_record_by_page_srt(page)
                data.extend(resultbypage)
                break
            except ConnectionError as _er_ror_:
                print(_er_ror_)

    dataInt = []
    for items in data:
        if items.get('orderStateName') == 'Processing':
           
            detailed = get_task_order(
                str(items.get('orderId')), str(items.get('shardingKey')))
            taskdata = detailed['resultData']

            for task in taskdata:
                if task.get('operOrgName') == 'Stratnet' and task.get('operTypeName') == 'Check Out':
                    dataInt.append(items.get('orderCode'))

    dats = set(dataInt)
    return dats


def get_open_tix():
    start_time = time.time()

    while True:
        try:
            print("Running Wrong Flow Checker...Will Re-run every 15-20mins")
            open_srt = get_all_open_srt()
            open_int = get_all_open_int()
        
            break
        except ConnectionError as error:
            print(error)

    opentix = open_srt.union(open_int)
    normaltix = []
    wrongflow = []
    
    for tix in opentix:

        while True:
            try:
                res = get_tix_details(str(tix))
                
                break
            except ConnectionResetError as __error_:
                print(__error_)

        tixdetails = res['resultData']["rows"][0]
        order_id = tixdetails['orderId']
        tix = tixdetails['orderCode']
        reporter = tixdetails['applyStaffName']

        while True:
            try:
                tasklist = get_last_task_list(order_id)
                
                break
            except ConnectionResetError as err2:
                print(err2)


        monthday = tix[7:11]

        month = monthday[0:2]
        int_month = int(month)

        day = monthday[2:4]
        int_day = int(day)

        year = tix[3:7]
        int_year = int(year)


        date = datetime.datetime(int_year, int_month, int_day)
        month_name = get_word_of_month(date)
        monthwithday = month_name+' '+day+' '+str(int_year)

        second_line_status = [
            "Second-line Handle", "Handle for Technical Support", "Second-line Operate", "IT Confirm"]

        prehandlestatus = ['Pre-Handle', 'ServiceDesk Pre-Handle']

        prehandleguys = ['Claveria . Julius.Monteliza', 'De Leon.Alexandra.Ruiz', 'Peñaranda. Paul Joelix.Astorga', 'Polache . Carlo Enrique .Balongoy', 'zhangshuhai', 'Malinao Rhenz',
                         'Mojica.Ligtas.Van Angelo', 'Marifosque Carlo Antonio Gerolao', 'Claro Carlito', 'Sarabia Evan Jasper', 'Villahermosa Reyn', 'John Luelle Gabales', 'Libaresos James Kenneth',
                         'Sarmiento John Leon Angelo', 'Recarro John Peter Gabrielle', 'Abrugar Paul Bryan', 'ikgonzales', 'Marwin Prendol', 'Calagos Reno', 'Lampitoc Danbrey Jen', 'Michael Angelo Mamano',
                         'Annie Marie Tan', 'Mark Kevin Casimiro', 'Earl Vincent Carolino', 'Manalindo Huzaima', 'Castillo Timothy', 'De Guzman', 'Christian Dave.Graida.Uson']
        currenthandler = tasklist['partyName']

        if tasklist['tacheName'] in prehandlestatus and tasklist['partyName'] != 'OSS_IT_SERVICE_DESK' and tasklist['partyName'].strip() not in prehandleguys:
            if monthwithday in [month["month"] for month in wrongflow]:
                for month in wrongflow:
                    if month["month"] == monthwithday:
                        monthwithday = month
                        new_ticket = {"Ticket": tix, "chandler": currenthandler,
                                      "comment": "Reporter Didnt Assign to SD - Pre handle", "status": tasklist['tacheName']}
                        monthwithday["tickets"].append(new_ticket)
                
            else:
                
                dateadd = {
                    "month": monthwithday,
                    "tickets": [{"Ticket": tix, "chandler": currenthandler, "comment": "Reporter Didnt Assign to SD - Pre handle", "status": tasklist['tacheName']}]
                }
                wrongflow.append(dateadd)

        elif tasklist['tacheName'] in second_line_status and tasklist['partyName'] == reporter:
            if monthwithday in [month["month"] for month in wrongflow]:
                for month in wrongflow:
                    if month["month"] == monthwithday:
                        monthwithday = month
                        monthwithday = month
                        new_ticket = {"Ticket": tix, "chandler": currenthandler,
                                      "comment": "Second-line directly assigned the ticket to reporter", "status": tasklist['tacheName']}
                        monthwithday["tickets"].append(new_ticket)
                

            else:
                
                dateadd = {
                    "month": monthwithday,
                    "tickets": [{"Ticket": tix, "chandler": currenthandler, "comment": "Second-line directly assigned the ticket to reporter", "status": tasklist['tacheName']}]
                }
                wrongflow.append(dateadd)

        elif tasklist['tacheName'] in second_line_status and tasklist['partyName'].strip() in prehandleguys:
            if monthwithday in [month["month"] for month in wrongflow]:
                for month in wrongflow:
                    if month["month"] == monthwithday:
                        monthwithday = month
                        monthwithday = month
                        new_ticket = {"Ticket": tix, "chandler": currenthandler,
                                      "comment": "Second-line directly assign the ticket to SD agent", "status": +tasklist['tacheName']}
                        monthwithday["tickets"].append(new_ticket)
                

            else:
                
                dateadd = {
                    "month": monthwithday,
                    "tickets": [{"Ticket": tix, "chandler": currenthandler, "comment": "Second-line directly assign the ticket to SD agent", "status": tasklist['tacheName']}]
                }
                wrongflow.append(dateadd)

        else:
            if monthwithday in [month["month"] for month in normaltix]:
                for month in normaltix:
                    if month["month"] == monthwithday:
                        monthwithday = month
                        new_ticket = {"Ticket": tix, "chandler": currenthandler,
                                  "comment": "Normal", "status": tasklist['tacheName']}
                        monthwithday["tickets"].append(new_ticket)
                    

                
            else:
                
                dateadd = {
                    "month": monthwithday,
                    "tickets": [{"Ticket": tix, "chandler": currenthandler, "comment": "Normal", "status": tasklist['tacheName']}]
                }
                normaltix.append(dateadd)
                

    end_time = time.time()

    run_time = end_time - start_time

    now = datetime.datetime.now()

    propdate = now.strftime("%B %d, %Y %H:%M")
    stringdata = ""
    stringdata2 = ""
    mention = False
    print(propdate)
    sorted_normaltix = sorted(normaltix, key=lambda x: parse_date(x['month']))

    for item in sorted_normaltix:
        print("")
        stringdata += "\n\n*" + item['month'] + "\n"
        
        for ticket in item["tickets"]:
            stringdata += ticket['Ticket'] + " - " + ticket['chandler'] + "("+ticket['status']+")""\n"

    
    
    if not wrongflow:
        stringdata2 += "NONE"
        mention = False
    else:
        sorted_wrongflow = sorted(wrongflow, key=lambda x: parse_date(x['month']))
        for item in sorted_wrongflow:
            stringdata2 += "*" + item['month'] + "\n"
            for ticket in item["tickets"]:
                stringdata2 += ticket['Ticket'] + " - " + ticket['comment']+"\n"
                mention = True
    
    print(run_time)
    data = {
        'date': propdate,
        'runtime': run_time,
        'mention': mention
    }
    


    send_ding_open_tix(stringdata,stringdata2,data)


def get_last_task_list(order_id):

    cookies = {
        '_tt_enable_cookie': '1',
    }

    headers = header_all

    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryWoWorkOrderList',
        'operator': 'Abrugar Paul Bryan',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryWoWorkOrderList","p0":"{\\"orderId\\":'+str(order_id)+'}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=10)

    res = response.json()
    rows = res['resultData']
    return rows[0]


def get_word_of_month(date):
    month_name = calendar.month_name[date.month]
    return month_name


def run15():
    while True:
        try:
            #get all open tix
            get_open_tix()
            time.sleep(1200)
        except Exception as err:
            _error_ = "An exception occurred:" + \
                str(err)+"\nPlease ignore if error HTTP Time-Out \n---Will Re-run in 30sec---"
            print("An exception occurred:"+str(err) +
                  "\nPlease ignore if http time-out will Re-run in 30sec")
            send_ding_error(_error_)
            time.sleep(30)

#Run function run15()
run15()
