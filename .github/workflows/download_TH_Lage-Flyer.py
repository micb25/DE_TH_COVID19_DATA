#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re

DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_TH_Lage-Flyer" + os.sep


def scrapeFlyer(url, pdf):
    global DATAPATH
    
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        fullname = DATAPATH + pdf
        
        if not os.path.isfile(fullname):
            
            # save contents
            with open(fullname, 'wb') as f:
                f.write(r.content)
                
            os.system("( cd {} && pdftotext -layout {} > /dev/null )".format(DATAPATH, pdf))
            
        return True
    
    except:
        return False
    

def scrapeLageFlyer():
    baseurl = "https://corona.thueringen.de/"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    pattern_flyer = re.compile(r"<a href=\"([^\"]*?\.pdf)\"[^>]*?>[^<]*?lyer[^<]*?([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{2,4})[^<]*?</a>")
    
    try:
        # download the website to get the URL of the document
        r = requests.get(baseurl, headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find URLs
        pm_urls = pattern_flyer.findall(src)
        
        if ( len(pm_urls) < 1 ):
            return False
        
        for url in pm_urls:
            datestr = "Lage-Flyer_{}-{}-{}.pdf".format(url[3], url[2], url[1])
            if url[0][:4].lower() == 'http':
                url = url[0]
            else:
                url = baseurl + url[0]
                
            scrapeFlyer(url, datestr)            
            
        return True
    
    except:
        return False


scrapeLageFlyer()
