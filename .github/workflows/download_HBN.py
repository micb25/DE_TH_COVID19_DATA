#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, os, re

DATAPATH = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + ".." + os.sep + "data_HBN" + os.sep
BASEURL  = "https://www.landkreis-hildburghausen.de"


def scrapeHBNPage(url):
    global DATAPATH
    global BASEURL
    
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    pattern_date = re.compile(r"<small class=\"date\">([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})</small>")
    pattern_pdf  = re.compile(r"<a target=\"_blank\" href=\"([^\"]*?)\" class=\"csslink_PDF\">[^\<]*?</a>")
    
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find date
        pm_date = pattern_date.findall(src)
        
        if ( len(pm_date) < 1 ):
            return False
    
        datestr = "{}-{}-{}".format(pm_date[0][2], pm_date[0][1], pm_date[0][0])
    
        pm_pdf = pattern_pdf.findall(src)
        
        if ( len(pm_pdf) < 1 ):
            return False
        
        elif ( len(pm_pdf) == 1 ):
            
            filename = "HBN_{}.pdf".format(datestr)
            fullname = DATAPATH + filename
            
            if not os.path.isfile(fullname):
            
                p = requests.get(BASEURL + pm_pdf[0], headers=headers, allow_redirects=True, timeout=5.0)
            
                # save contents
                with open(fullname, 'wb') as f:
                    f.write(p.content)
                    
                os.system("( cd {} && pdftotext -layout {} > /dev/null )".format(DATAPATH, filename))
        
        else:
            
            for i, pdfurl in enumerate(pm_pdf):
                
                filename = "HBN_{}_{}.pdf".format(datestr, i+1)
                fullname = DATAPATH + filename
                
                if not os.path.isfile(fullname):
                    
                    p = requests.get(BASEURL + pm_pdf[i], headers=headers, allow_redirects=True, timeout=5.0)
            
                    # save contents
                    with open(fullname, 'wb') as f:
                        f.write(p.content)
                        
                    os.system("( cd {} && pdftotext -layout {} > /dev/null )".format(DATAPATH, filename))
            
        return True
    
    except:
        return False
    

def scrapeHBN():
    global BASEURL
    
    url = BASEURL + "/Aktuelles-Covid-19/Aktuelles-zu-Covid-19-im-Landkreis/Aktuelle-Meldungen-aus-dem-Landkreis"
    headers = { 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }
    pattern_pm = re.compile(r"<a href=\"([^\"]*?)\">[^<]*?Aktuelle (?:Fallzahlen|Zahlen|Lage)[^<]*?</a>")
    
    try:
        # download the website to get the URL of the document
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5.0)
        src = r.text.replace('\n', ' ')
        
        # find URLs
        pm_urls = pattern_pm.findall(src)
        
        if ( len(pm_urls) < 1 ):
            return False
        
        for url in pm_urls:
            scrapeHBNPage(BASEURL + url.replace("&amp;", "&"))            
            
        return True
    
    except:
        return False


scrapeHBN()
