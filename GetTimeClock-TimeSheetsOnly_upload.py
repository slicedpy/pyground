import requests
import json
import pandas as pd
import datetime
import time
from pathlib import Path


def GetTSheetTimesheet(subdomain,outfile,days_back,delay=3):

    timesheet_url = 'https://'+subdomain+'.tsheets.com/api/v1/'+str(outfile).lower()
    date_today = datetime.datetime.today()
    date_list = [date_today - datetime.timedelta(days=xDays) for xDays in range(days_back)]
    #filepath = str(Path().absolute().parent)
    filepath = ''

    with open(filepath+"\\data\\"+outfile+'.csv','w') as outResults:
        counter = 0
        for eachdate in date_list:
            queryDates = str(eachdate.strftime("%Y-%m-%d"))
            print("Processing " + str(queryDates))
            querystring = {"start_date":queryDates,
                           "on_the_clock":"both"
                           }
            payload = ""

            with open('','r') as api_key:
            #with open(filepath+"\\data\\tsheetkey.txt','r') as api_key:
                headers = {'Authorization': api_key.read()}
                timesheets = requests.request("GET",timesheet_url,data=payload,headers=headers,params=querystring)
                time.sleep(delay)
                GetTimeSheets = timesheets.json()['results'][outfile]
                headcard,details = [],[]

                for elements in GetTimeSheets:
                    for column in GetTimeSheets[elements]:
                        try:
                            headcard.index(column)
                        except:
                            headcard.append(column)
                            
                    if counter == 0:
                            headline = ''
                            for each in headcard:headline+=str(each)+','
                            outResults.write(headline[:-1]+"\n")
                            #print(headline[:-1]+"\n")
                            counter += 1
                            
                    detail_line = ''
                    for each in headcard:
                        detail_line += str(GetTimeSheets[elements][each]).replace(',','|')+','
                    outResults.write(detail_line+"\n")
                    #print(detail_line+"\n")
                
GetTSheetTimesheet('','timesheets',400)

# Project Name: [10] Hindoo
# Hindoo was an outstanding American Thoroughbred race horse who won 30 of his 35 starts, including the Kentucky Derby, the Travers Stakes, and the Clark Handicap. 
# Created 3 March 2020
#
# Purpose: To author an efficient library to fetch and analyze timesheet objects from the T-Sheets API.
# -TCL (tiffanee.lang@optum.com)
#
# API Documentaiton
# https://tsheetsteam.github.io/api_docs/#welcome
#
#
# About these packages:
# request: https://requests.readthedocs.io/en/master/
# json: https://docs.python.org/3/library/json.html
# pandas: https://pandas.pydata.org/
# datetime: https://docs.python.org/3/library/datetime.html
# time: https://docs.python.org/3/library/time.html
# pathlib: https://docs.python.org/3/library/pathlib.html



### Developer's Playground ###
# https://realpython.com/python-encodings-guide/
#   https://files.realpython.com/media/Encodings--Number-Systems_Watermarked.906d62e907dc.jpg
# https://docs.python.org/3/howto/unicode.html
# Encoding: https://docs.python.org/2.4/lib/standard-encodings.html
#
#
#
##    with open(filepath+"\\data\\"+outfile+'.csv','w') as outResults:
##        for each_date in date_list:
##            print(str(each_date.strftime("%Y-%m-%d")))
##
##
##
#
# 2020-03-17
# Things to consider: API key storage--current set up not preferred.
# With this in mind [RH]:Python and Encryption options
# Updated function to be dynamic for any subdomain
#
# Read more about domains: https://moz.com/learn/seo/domain


