#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re, sys
from datetime import datetime

VERBOSE  = True
DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_SHK" + os.sep
DATE_STR = datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d')
FILENAME1 = "SHK_{}.html".format(DATE_STR)
FILENAME2 = "SHK_Infos_{}.html".format(DATE_STR)
FULLNAME1 = DATAPATH + FILENAME1
FULLNAME2 = DATAPATH + FILENAME2
PICNAME1  = DATAPATH + "SHK_{}.jpg".format(DATE_STR)
URL1  = "https://www.saaleholzlandkreis.de/corona-virus/uebersicht-fall-zahlen/"
URL2  = "https://www.saaleholzlandkreis.de/corona-virus/aktuelle-infos/"

pic1_pattern = re.compile(r"<img\ src=\"(.*?Diagramm.*?)\"")

if os.path.isfile(FULLNAME1):

    if VERBOSE:
        print("The file '{}' exists already.".format(FILENAME1))
        
    sys.exit(0)
    
else:
    
    if VERBOSE:
        print("The file '{}' does not exist.".format(FILENAME1))
        
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    r = requests.get(URL1, headers=headers, allow_redirects=True, timeout=5.0)
    if r.status_code != 200:
        print("Download failed!")
        sys.exit(1)
        
    with open(FULLNAME1, 'wb') as df:
        df.write(r.content)
        df.close()  
        
    pp1 = pic1_pattern.findall(r.text)
    if len(pp1) > 0:
        PICURL1 = "https://www.saaleholzlandkreis.de/" + pp1[0]
        
        p = requests.get(PICURL1, headers=headers, allow_redirects=True, stream=True, timeout=5.0)
        if p.status_code == 200:
            with open(PICNAME1, 'wb') as df:
                df.write(p.content)
                df.close()  
        
    r = requests.get(URL2, headers=headers, allow_redirects=True, timeout=5.0)
    if r.status_code != 200:
        print("Download failed!")
        sys.exit(1)
        
    with open(FULLNAME2, 'wb') as df:
        df.write(r.content)
        df.close()      
