#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 16:27:54 2019

@author: enzo.ramirez
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 09:38:55 2019

@author: enzo.ramirez
"""


import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np

#from urllib.error import HTTPError, URLError

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"typeA",
                u"site",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']
pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"
pattern_site = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,}(\/\S*)?"


csv_df = pd.DataFrame(columns=fieldnames)

def cleanlist(j):
    for a in j:
        a = a.strip()
        try :
            repl = re.search(r'^\w{0,1}$', a).group()
            j.remove(repl)
        except:
            pass
    X = [x.replace('\xa0','').replace('(','').replace(')','').replace('|','').replace('','').replace(':','').strip() for x in j]
    for i in X :
       if len(i) < 2 :
           X.remove(i)
    return X

def remlist(i) :
    if '' in i: i.remove('')
    return i

def nettoyage_chaine(chaine):
    chaine = chaine.strip()
    chaine = re.sub(r'\s+',' ', chaine)
    return chaine


def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)

    rep = {}
    try:
        societe = soup.find("div", "title_subtitle_holder_inner").h1.text.replace('\n',' ').strip()
        rep["societe"] = societe
    except :
        rep["societe"] = np.nan


    try:
        description = soup.find('div' , 'wpb_wrapper').findAll('div' , 'wpb_text_column')[1].text
        rep["description"] = description.replace('\n',' ').strip()
    except:
        rep["description"] = np.nan

    try:
        site = soup.find('div' , 'wpb_wrapper').findAll('div' , 'wpb_wrapper')[1].text
        site = re.search(pattern_site, site).group()
        rep["site"] = site
    except:
        rep["site"] = np.nan

    try:
        typeA = soup.find('div' , 'wpb_wrapper').findAll('div' , 'wpb_wrapper')[1].text
        typeA = typeA.replace(site,'').strip()
        rep["typeA"] = typeA
    except:
        rep["typeA"] = np.nan

    try:
        rep["cluster"] = 'masphere'
    except:
        rep["cluster"] = 'mapshere'

    return(rep)


url_base = "http://www.ma-sphere.eu/adherents/"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "full_width_inner").findAll("a")

fiches = [f.get("href") for f in fiches]
fiches = remlist(fiches)

for f in fiches:
        url_fiche = f
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
#        try:
#            fiche = lecture_exposant(url_fiche)
#        except HTTPError:
#            continue
       # fiche["id_societe"] = "soc_%d" % i
        #i += 1
        csv_df = csv_df.append(fiche, ignore_index=True)


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "masphere")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "masphere.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "masphere.xlsx")
