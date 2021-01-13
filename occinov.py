#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:24:44 2019

@author: enzo.ramirez
"""

import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time

fieldnames = [#u"id_societe",
                u"societe",
                u"CP",
                u"Espace d'expo"
]

csv_df = pd.DataFrame(columns=fieldnames)


def nettoyage_chaine(chaine):
    chaine = chaine.strip()
    chaine = re.sub('\s+',' ', chaine)
    return chaine


def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)


    rep = {}
    try:
        rep["societe"] = soup.find("div", class_ = "gv-list-view-title").h3.text.strip().upper()
    except:
        rep["societe"] = ''

    try:
        rep["Espace d'expo"] = soup.find("div", class_ = "gv-field-3-6").li.text.strip()
    except:
        rep["Espace d'expo"] = ''

    try:
        rep["CP"] = soup.find("div", class_ = "view gv-field-3-7.5").text.replace('Code postal :','').strip()
    except:
        rep["CP"] = ''

    return(rep)


url_base = "https://www.occitanie-innov.com/les-exposants/"

i = 1
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "entry-content row").find("div", "gv-list-container").findAll("a")
for f in fiches:
        url_fiche = f.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
       # fiche["id_societe"] = "soc_%d" % i
        #i += 1
        csv_df = csv_df.append(fiche, ignore_index=True)

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "
csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "occi_innov")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "occi_innov.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "occi_innov.xlsx")
