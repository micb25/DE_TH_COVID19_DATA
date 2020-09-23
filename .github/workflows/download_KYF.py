#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re, sys
from datetime import datetime

VERBOSE  = True
DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_KYF" + os.sep

def save_KYF_PDFs():
    url = "https://www.kyffhaeuser.de/kyf/index.php/landkreis.html"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    try:
        # download the website to get the URL of the document
        src = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0).text
        
        # find the URL of the document
        pattern_pdf = re.compile(r"<a\ href=\"index.php/landkreis.html\?file=(tl_files/download/Infomaterial/corona/[^/]*?Zahlen[^/]*?.pdf)\"") # title=\"PM v. (.*?)\"")
        date_pattern = re.compile(r".*?/([0-9]{4})-([0-9]{2})-([0-9]{2}).*?")
        pdfsrc = pattern_pdf.findall(src)
                
        if ( len(pdfsrc) < 1 ):
            return False
        
        for file in pdfsrc:
            dg = date_pattern.match(file)
            if dg:
                pdf_name = "KYF_{}-{}-{}.pdf".format(dg.group(1), dg.group(2), dg.group(3))
                pdf_url = "https://www.kyffhaeuser.de/kyf/index.php/landkreis.html?file=" + file

                # check if document exists and is not empty
                pdf_local = DATAPATH + pdf_name
                try:
                    fs = os.path.getsize(pdf_local)
                except:
                    fs = 0
                
                if ( fs > 0 ):
                    continue
        
                # do the request
                pdf_data = requests.get(pdf_url, headers=headers, allow_redirects=True, timeout=5.0)
                
                if pdf_data.status_code != 200:
                    continue
                
                # save the document        
                with open(pdf_local, 'wb') as f:
                    f.write(pdf_data.content)
                    
                os.system("( cd {} && pdftotext -layout {} > /dev/null )".format(DATAPATH, pdf_name))
                
        return True
        
    except:
        return False
    
save_KYF_PDFs()
