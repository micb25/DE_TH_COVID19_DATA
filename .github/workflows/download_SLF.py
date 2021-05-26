#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re

DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_SLF" + os.sep


def scrapeSLFPage(url):
    global DATAPATH
    
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    # pattern_date = re.compile(r"<div class=\"content_mitte_datum\sdetail\">([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})</div>")
    pattern_date = re.compile(r"datePublished\"\sdatetime=\"([\d]{2})\.([\d]{2})\.([\d]{4})\"")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find date
        pm_date = pattern_date.findall(src)
        
        if ( len(pm_date) < 1 ):
            return False
        
        datestr = "{}-{}-{}".format(pm_date[0][2], pm_date[0][1], pm_date[0][0])
        filename = "SLF_{}.html".format(datestr)
        fullname = DATAPATH + filename
        
        if not os.path.isfile(fullname):
            
            # save contents
            with open(fullname, 'w') as f:
                f.write(r.text)
            
        return True
    
    except:
        return False
    

def scrapeSLF():
    baseurl = "https://www.kreis-slf.de"
    url = baseurl + "/sport-und-gesundheit/"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    pattern_pm = re.compile(r"<h4>.*?Coronafälle.*?</h4>.*?<a\ [^>]*href=\"([^\"]*?)\"")
    
    try:
        # download the website to get the URL of the document
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find URLs
        pm_urls = pattern_pm.findall(src)
        
        if ( len(pm_urls) < 1 ):
            return False
        
        for url in pm_urls:
            scrapeSLFPage(baseurl + url)            
            
        return True
    
    except:
        return False


scrapeSLF()
