import calendar
import datetime
from dateutil import parser
import pprint
import pandas as pd
from requestcalls.getdata import get_tix_details


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
        date_string = samp['finishDate']
        date = parser.parse(date_string)
        output_string = date.strftime("%m/%d/%Y")
        print(tix," CLOSED @ ",date_string," - ",output_string)
        return
    return


def pen_ac22():

    df = pd.read_excel('rawdata.xlsx', sheet_name="2023 Ticket Tracker")
    data = df[df['Status'] == 'Pending-customer confirm']
    my_dict = data.to_dict(orient = 'records')


    df1 = pd.read_excel('rawdata.xlsx', sheet_name="2023 Ticket Tracker")
    data1 = df1[df1['Status'] == 'Pending-customer action']
    my_dict1 = data1.to_dict(orient = 'records')


    df2 = pd.read_excel('rawdata.xlsx', sheet_name="2023 Ticket Tracker")
    data2 = df2[df2['Status'] == 'Second-line handle']
    my_dict2 = data2.to_dict(orient = 'records')


    df3 = pd.read_excel('rawdata.xlsx', sheet_name="2022 Ticket Tracker")
    data3 = df3[df3['Status'] == 'Pending-customer confirm']
    my_dict3 = data3.to_dict(orient = 'records')


    df4 = pd.read_excel('rawdata.xlsx', sheet_name="2022 Ticket Tracker")
    data4 = df4[df4['Status'] == 'Pending-customer action']
    my_dict4 = data4.to_dict(orient = 'records')


    df5 = pd.read_excel('rawdata.xlsx', sheet_name="2022 Ticket Tracker")
    data5 = df5[df5['Status'] == 'Second-line handle']
    my_dict5 = data5.to_dict(orient = 'records')


    my_dict.extend(my_dict1)
    my_dict.extend(my_dict2)
    my_dict.extend(my_dict3)
    my_dict.extend(my_dict4)
    my_dict.extend(my_dict5)

    # pprint.pprint(my_dict)

    tixnum_ar = [d['Case No.'].strip() for d in my_dict]
    dataobj=[]

    for tixnum in tixnum_ar:
        tixnumstrim = tixnum
        tixnumclean = tixnumstrim.strip()
        checkticket(tixnumclean,dataobj)




pen_ac22()


