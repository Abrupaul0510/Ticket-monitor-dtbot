import requests

def get_tix_details(ticketn):
    tixnumstrim = ticketn
    ticketnumber = tixnumstrim.strip()
    cookies = {
}

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
    'X-CSRF-TOKEN': '30d7be0b-8a27-4a2c-a1bd-ecb3720da833',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

    data = {
    'serviceName': 'ptoOrderServiceBean',
    'methodName': 'queryOrderMonitorList',
    'moduleName': 'taskflow',
    'param': '{"serviceName":"ptoOrderServiceBean","method":"queryOrderMonitorList","p0":"{\\"orderState\\":\\"UNFINISHED\\",\\"orderCode\\":\\"\\",\\"orderCodeOrTitle\\":\\"'+ticketnumber+'\\",\\"packageId\\":null,\\"pageIndex\\":1,\\"pageSize\\":20,\\"resetPage\\":true,\\"qryOrgRegion\\":null,\\"notTicketType\\":[\\"PNAT\\"]}"}',
}

    response = requests.post(
    'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
    cookies=cookies,
    headers=headers,
    data=data,
)
    res = response.json()
    return res



def get_open_ticket(staffID):


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': 'b633e246-ec67-4e6c-b7e4-40670c593034',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'serviceName': 'ptoWorkOrderServiceBean',
        'methodName': 'queryOrderByParam',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ptoWorkOrderServiceBean","method":"queryOrderByParam","p0":"{\\"operationType\\":\\"mytask-processed\\",\\"workOrderState\\":\\"10F\\",\\"isFinished\\":false,\\"sortList\\":[],\\"pageIndex\\":1,\\"orderState\\":null,\\"pageSize\\":20,\\"siteRoomCable\\":\\"\\",\\"staffId\\":'+staffID+',\\"workOrderTitle\\":\\"\\",\\"notTicketType\\":[\\"PNAT\\"]}"}',
    }
    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        headers=headers,
        data=data,
        timeout=200
    )

    res = response.json()

    return res


def get_task_order(orderIDs,shardingKey):

    

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': '97f3e7e3-c9a2-4a57-b613-19fea5339bd5',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'serviceName': 'ossOperRecordServiceBean',
        'methodName': 'selectOssOperRecordByMap',
        'moduleName': 'taskflow',
        'param': '{"serviceName":"ossOperRecordServiceBean","method":"selectOssOperRecordByMap","p0":"{\\"orderId\\":'+orderIDs+',\\"shardingKey\\":'+shardingKey+'}"}',
    }

    response = requests.post(
        'https://portal.dito.ph/oss-eoms-taskflow/executeService/execute.do',
        headers=headers,
        data=data,
    timeout=200)
    res = response.json()

    return res

