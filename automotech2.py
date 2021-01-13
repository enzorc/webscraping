#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:02:59 2019

@author: enzo.ramirez
"""

import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time


fieldnames = [u"societe",
                u"typeA",
                u"description",
                u"contact",
                u"adresse",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)


def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    print (soup.title.text)

    rep = {}
    try:
        rep["societe"] = soup.find("div", class_="raison_sociale").legend.text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["typeA"] = soup.find("b", string="Secteur d'activité: ").parent.parent.text.replace("\n"," ").replace("\t"," ").split(":")[1].strip()
    except:
        rep["typeA"] = "NA"
    try:
        rep["description"] = soup.find('b', string="Activité: ").parent.parent.text.replace("\n"," ").replace("\xa0","").split("Activité:  ")[1].strip()
    except:
        rep["description"] = "NA"
    try:
        rep["contact"] = soup.find("b", string="Nom du contact : ").parent.parent.text.split(":")[1].strip()
    except:
        rep["contact"] = "NA"
    try:
        rep["adresse"] = soup.find("b", string="Adresse : ").parent.parent.text.replace("\n"," ").split(":")[1].strip().replace("Département","")
    except:
        rep["adresse"] = "NA"
    try:
        rep["cluster"] = 'automotech'
    except:
        rep["cluster"] = 'automotech'
    return(rep)

url_base = "https://www.automotech.fr/spip.php?page=liste-adherants&ta=1"
i = 1
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("table", class_ = "resultats").findAll("a", href = re.compile("^spip.php"))[2:]
for f in fiches:
        url_fiche = "https://www.automotech.fr/" + f.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
        csv_df = csv_df.append(fiche, ignore_index=True)
        time.sleep(0.05)


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "automotech")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "automotech.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "automotech.xlsx")
