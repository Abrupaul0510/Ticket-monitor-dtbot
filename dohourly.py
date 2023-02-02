import calendar
import datetime
import pandas as pd
from requestcalls.getdata import get_tix_details
from requestcalls.getdata import get_task_order


##checking ticket thru OFM
def checkticket(tixnumclean,dataobj):

    res = get_tix_details(tixnumclean)


                                    #REFERENCE
                                    # orderID = samp['orderId']   #UNIQUE ID
                                    # handler = samp['partyStaffNames'] #HANDLER
                                    # handlerorg = samp['partyOrgNames'] #HANDLER ORG
                                    # status = samp['tacheName'] #STATUS
                                    # # reporter = samp['applyStaffName'] #REPORTER/APPLICANT
                                    # # lastDate = samp['taskCreateDate'] # TIME TICKET LAST MOVEMENT


    #IF TICKET IS ALREADY CLOSED!
    if res['resultData']["total"] <= 0:
        print(tixnumclean, "Input Error!!! or No record found")
        return

    samp = res['resultData']["rows"][0]

    tix = samp['orderCode'] #TIXNUM
    status = samp['tacheName']

    if not status :
        print(tix, "is CLOSED! ***removing from the report***")
        return

    #Initiating other vars
    reporter = samp['applyStaffName']#REPORTER
    status = samp['tacheName'] #STATUS
    handler = samp['partyStaffNames'] #HANDLER
    orgName = samp['partyRoleNames'] 
    handlerorg = samp['partyOrgNames'] #HANDLER ORG
    orderId = samp['orderId'] #HANDLER ORG
    shardingKey = samp['shardingKey']

    

    
    # get_sd_prehandle_date = get_task_order(str(orderId),str(shardingKey))

    # print(get_sd_prehandle_date)

    # checkout_date = createDate

    


    #IF TICKET IS ON WRONG FLOW!
    if handler == reporter and status == "Handle for Technical Support":
        print(tix, "IS WRONG FLOW!! PLEASE CHECK!!")
        return
    if handler == reporter and status == "Second-line Operate":
        print(tix, "IS WRONG FLOW!! PLEASE CHECK!!")
        return
    if handler == reporter and status == "Second-line Handle":
        print(tix, "IS WRONG FLOW!! PLEASE CHECK!!")
        return

    #IF TICKET IS ALREADY FOR CONFIRMATION!
    if status =="Applicant Confirm" or status == "Confirm(Creator)" or status == "Callback":
        print(tix +" is now on "+ status,"!! ***removing from the report***")
        return

    #IF TICKET IS CURRENTLY ON SD QUE!
    if status == "Confirm(Service Desk)":
        print(tix ,  'is currently handling by', handler )
        return

    else:
        #getting the dates from ticket var
        monthday = tix[7:11] 
        #month
        month = monthday[0:2]
        int_month = int(month)
        #day
        day = monthday[2:4]
        int_day = int(day)
        #combining for report format
        date = datetime.datetime(2022,int_month,int_day)
        month_name = get_word_of_month(date)
        monthwithday = month_name+' '+day

        #check if monthandday exist in dataobj
        if monthwithday in [month["month"] for month in dataobj]:
            for month in dataobj:
                if month["month"] == monthwithday:
                    monthwithday = month
                    new_ticket = {"Ticket": tix, "handler": handler, "orgName": orgName, "handlerorg" : handlerorg}
                    monthwithday["tickets"].append(new_ticket)
                    print("Done checking",tix +" with status of "+ status," ("+handler+")")
                    return
        else:
            print("Done checking",tix +" with status of "+ status,"("+handler+")")
            dateadd = {
                    "month": monthwithday,
                    "tickets": [{"Ticket": tix, "handler": handler, "orgName": orgName, "handlerorg" : handlerorg}]
                    }
            dataobj.append(dateadd)
            return


#GETTING MONTN NAME
def get_word_of_month(date):
    month_name = calendar.month_name[date.month]
    return month_name



###MAIN###
print("Extracing data from excel...")
df = pd.read_excel('rawdata.xlsx', sheet_name="2023 Ticket Tracker")

data = df[df['Status'] == 'Second-line handle']

#GETTING ALL DATA ===Second line in records format
my_dict = data.to_dict(orient = 'records')

#Extracting only ticket number with SL status
tixnum_ar = [d['Case No.'].strip() for d in my_dict]
print("Getting All Tix.....")
dataobj=[]
for tixnum in tixnum_ar:
    tixnumstrim = tixnum
    tixnumclean = tixnumstrim.strip()
    checkticket(tixnumclean,dataobj)

#OUTPUTING ALL DATA
print("")
print("")
print("Generating...")
for month in dataobj:
    print("")
    print("*"+month["month"] + "")
    for ticket in month["tickets"]:
        if not ticket["handler"]:
            print(ticket["Ticket"] + " - " + ticket["orgName"])
        else:
            print(ticket["Ticket"] + " - " + ticket["handlerorg"] +" | "+ ticket["handler"])




