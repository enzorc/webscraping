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

def striplist(l):
    return([x.strip() for x in l])

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
        infos = soup.find("div", "miniword").findAll('a')
        societe = infos[i].text
        print(societe)
        rep["societe"] = societe
    except :
        rep["societe"] = np.nan


    try:
        description = soup.find(string = societe).parent.find_next(string =True).find_next(string =True)
        description = description.replace(',' , '').strip()
        rep["description"] = description
    except:
        rep["description"] = np.nan

    try:
        site = infos[i].get('href')
        rep["site"] = site
    except:
        rep["site"] = np.nan

    try:
        rep["cluster"] = 'trimatec'
    except:
        rep["cluster"] = 'trimatec'

    return(rep)


url_base = "http://www.pole-trimatec.fr/article/les_entreprises_et_associations_d_entreprises_membres"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)

i=0
while True :
    try:
        fiche = lecture_exposant(url_base)
        i+=1
        print(i)
    except:
        break

    if i ==67 :
        break
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
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "trimatec")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "trimatec.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "trimatec.xlsx")
