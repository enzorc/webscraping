#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:47:49 2019

@author: enzo.ramirez
"""

import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time



fieldnames = [u"societe",
                u"adresse",
                u"tel",
                u"fax",
                u"site",
                "cluster",
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
        rep["societe"] = soup.find("div", class_= "col_main").h1.text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["adresse"] = "".join(soup.find("div", class_="contour_fiche").strong.parent.text.split("-")[1:]).strip()
    except:
        rep["adresse"] = "NA"
    try:
        rep["tel"] = soup.find("div", class_="contour_fiche").findAll("p")[1].text.split("-")[0].split(":")[1].strip()
        if rep["tel"] == "N/A" or rep["tel"] =="":
            rep["tel"] = "NA"
        else:
            pass
    except:
        rep["tel"] = "NA"
    try:
        rep["fax"] = soup.find("div", class_="contour_fiche").findAll("p")[1].text.split("-")[1].split(":")[1].strip()
        if rep["fax"] == "N/A" or rep["fax"] == "":
            rep["fax"] = "NA"
        else:
            pass
    except:
        rep["fax"] = "NA"
    try:
        rep["site"] = soup.find("div", class_="contour_fiche").findAll("p")[2].find("a").get("href").strip()
        if rep["site"] == "N/A" or rep["site"] ==  "":
            rep["site"] = "NA"
        else:
            pass
    except:
        rep["site"] = "NA"
    try:
        rep["cluster"] = 'chimieverte'
    except:
        rep["cluster"] = 'chimieverte'
    return(rep)

url_base = "https://www.clusterchimieverte.fr/nos-outils/annuaires-des-membres/"
i = 1
j = 1
while True:
    req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    fiches = soup.find("ul", class_ = "liste_annuaire").findAll("a", href = re.compile("^https://www.clusterchimieverte.fr/"))
    for f in fiches:
            url_fiche = f.get("href")
            print( "fiche: {}".format(url_fiche))
            fiche = lecture_exposant(url_fiche)
           # fiche["id_societe"] = "soc_%d" % i
            #i += 1
            csv_df = csv_df.append(fiche, ignore_index=True)
            time.sleep(0.05)
    try:
            url_base = soup.find("a", class_ = "next page-numbers").get("href")
            print("page: {}".format(url_base))
    except:
        break

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "



csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "chimieverte")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "chimieverte.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "chimieverte.xlsx")
