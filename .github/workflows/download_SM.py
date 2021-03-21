#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re, sys
from datetime import datetime

VERBOSE  = True
DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_SM" + os.sep
DATE_STR = datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d')
FILENAME = "SM_{}.pdf".format(DATE_STR)
FULLNAME = DATAPATH + FILENAME

def saveSMNumbers():
    url = "https://www.lra-sm.de/?p=26273"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    DATE_STR = datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d')
    
    try:
        # download the website to get the URL of the document
        src = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text
        
        # find the URL of the document
        pattern_pdf = re.compile(r"<a\ href=\"https\:\/\/www.lra-sm.de/(.*(?:Lage|Stand|TLB|Bulletin).*\.pdf)\"\>")        
        pdfsrc = pattern_pdf.findall(src)
        
        if ( len(pdfsrc) < 1 ):
            return False
            
        # get the document
        pdf_url = "https://www.lra-sm.de/" + pdfsrc[0]
            
        filename_pattern = re.compile(r"\/([^\/]*\.pdf)$")
        filename = filename_pattern.findall(pdf_url)
        
        if (len(filename) < 1):
            return False
        
        # check if document exists and is not empty
        pdf_local = DATAPATH + "SM_{}.pdf".format(DATE_STR)
        try:
            fs = os.path.getsize(pdf_local)
        except:
            fs = 0
        
        if ( fs > 0 ):
            return False
        
        # do the request
        pdf_data = requests.get(pdf_url, headers=headers, allow_redirects=True, timeout=5.0)
        
        if pdf_data.status_code != 200:
            return False
        
        # save the document        
        with open(pdf_local, 'wb') as f:
            f.write(pdf_data.content)
            
        os.system("( cd {} && pdftotext -layout {} > /dev/null )".format(DATAPATH, "SM_{}.pdf".format(DATE_STR)))
                
        return True
        
    except:
        return False

if os.path.isfile(FULLNAME):

    if VERBOSE:
        print("The file '{}' exists already.".format(FILENAME))
        
    sys.exit(0)
    
else:
    
    if VERBOSE:
        print("The file '{}' does not exist.".format(FILENAME))
        
    saveSMNumbers()   
