import sys
from requestcalls.getdata import get_open_ticket
from requestcalls.getdata import get_tix_details
from requestcalls.getdata import get_task_order
import datetime
import pprint

# staffID = sys.argv[1]

staffID = "26009"
res = get_open_ticket(staffID)

if res['resultData']["total"] <= 0:
    print("AgentID", staffID ,"Invalid or Not Found")
else:
    print("Open tickets of",staffID)
    print("")
    resobj = res['resultData']["rows"]
    for items in resobj:
        ticketnum = items['orderCode']
        tickettype = items['packageName']

        if tickettype == 'IT Service Request' or tickettype == "Incident Management":

            detailsobj = get_tix_details(ticketnum)
            # print(detailsobj)
            if detailsobj['resultData']["total"] <= 0:
                print("Input Error!!! or No record found")
            else:
                samp = detailsobj['resultData']["rows"][0]
                tix = samp['orderCode']
                prio = samp['orderPriority']
                status = samp['tacheName']
                lastDate = samp['taskCreateDate']
                orderID = samp['orderId']
                shardingKey = samp['shardingKey']
                
                # print(tix,shardingKey,lastDate)

                #14/12/2022 14:04:10 REFERENCE
                date_str = lastDate

                format_str = "%d/%m/%Y %H:%M:%S"

                date = datetime.datetime.strptime(date_str, format_str)

                year = date.year
                month = date.month
                day = date.day
                hour = date.hour
                minute = date.minute
                second = date.second

                # Define the two dates and times
                date1 = datetime.datetime(year, month, day, hour, minute, second)
                date2 = datetime.datetime.now()
                difference = date2 - date1
                days = difference.days
                hours = difference.seconds / 3600




                orderIDtrim = orderID
                orderIDs = str(orderIDtrim)
                objremind = []
                res1 = get_task_order(orderIDs,str(shardingKey))
                
                indx = len(res1['resultData'])
                
                data = res1['resultData']




                indxlast = indx-2
                taskdata = res1['resultData'][-indxlast]



                if str(taskdata.get('operStaffId')) == str(staffID):
                    print(tix," - ",prio," - ", status)
                    # for items in data:
                    #     print(items.get('operTypeName'))

                # task_last_touch = taskdata

                # remind_created = task_last_touch["createDate"]
                # doremind = task_last_touch["operStaffName"]

                
                # if "Remind" in task_last_touch["operTypeName"]:
                #     if days == 1:
                #         print(tix,"is pending for",status,"and CHASE has been SENT ALREADY by", doremind, remind_created)
                #     else:
                #         if days == 2:
                #             print(tix,"is pending for",status,"and CHASE has been SENT ALREADY by", doremind, remind_created)
                #         else:
                #             if days == 3:
                #                 print(tix,"is pending for",days,"days last chase sent by",doremind,remind_created)
                #             else:
                #                 if days == 4:
                #                     print(tix,"is pending for ",days," days and has ALREADY reminded by", doremind, remind_created)
                #                 else:    
                #                     if days == 5:
                #                         print(tix,"has been pending for more than", days,"days with status of ",status,"and 3RD CHASE has been SENT ALREADY by", doremind, remind_created)


                # else:
                #     if days == 0:
                #         print(tix,"IS LAST TOUCH TODAY, FOR SENDING 1ST CHASE TOMMOROW")

                #     else:
                #         print(tix,"TICKET NOT YET REMINDED HAS BEEN PENDING FOR", days,"DAYS!!!")
                
                # for item in taskdata:
                #     # print(item['operTypeName'])
                #     if item['operTypeName'] == 'Remind':
                #         objremind.append({"Has Remind": item['createDate']})

                #     else:
                #         objremind.append({"No": item['createDate']})

                #     # for i in item:
                #     #     print(i)
                        
                        
                # print(objremind)


                # print(orderID)

                # if days == 1:
                #     print(tix,"FOR 1ST CHASE!!!!")
                # if days == 2:
                #     print(tix,"FOR 2ND CHASE!!!!")
                # if days == 5:
                #     print(tix,"YOU NEED TO SEND A 1ST CHASE!!!!")




        else:
            print("")


            

        


        
