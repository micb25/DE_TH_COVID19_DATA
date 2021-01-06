#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re

DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_IK" + os.sep


def scrapeIKPage(url):
    global DATAPATH
        
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    
    pattern_date = re.compile(r"<div class=\"date\">([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})</div>")
    
    try:
        r = requests.get(url.replace("&amp;", "&"), headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find date
        pm_date = pattern_date.findall(src)
        
        if ( len(pm_date) < 1 ):
            return False
                
        datestr = "{}-{}-{}".format(pm_date[0][2], pm_date[0][1], pm_date[0][0])
        filename = "IK_{}.html".format(datestr)
        fullname = DATAPATH + filename
        
        if not os.path.isfile(fullname):
            
            # save contents
            with open(fullname, 'w') as f:
                f.write(r.text)
            
        return True
    
    except:
        return False
    

def scrapeIK():
    baseurl = "https://www.ilm-kreis.de"
    url = baseurl + "/Landkreis/Ver%C3%B6ffentlichungen/"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    pattern_pm = re.compile(r"<a href=\"([^\"]*?)\" title=\"[^\"]*?\">Aktuelle (?:Fallzahlen|Zahlen|Lage)[^<]*?</a>")
    
    try:
        # download the website to get the URL of the document
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find URLs
        pm_urls = pattern_pm.findall(src)
        
        if ( len(pm_urls) < 1 ):
            return False
        
        for url in pm_urls:
            scrapeIKPage(baseurl + url)            
            
        return True
    
    except:
        return False


scrapeIK()
