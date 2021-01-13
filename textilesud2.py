#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:15:48 2019

@author: enzo.ramirez
"""

import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd





fieldnames = [u"typeA",
                u"typeA2",
                u"societe",
                u"description",
                u"tel",
                u"email",
                u"produits",
                u"board",
                u"site",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

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
        rep["societe"] = soup.find("div").h1.text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["description"] = soup.find('div', class_="content").text.replace("\n"," ").replace("\xa0","").strip()
        if rep["description"] == "" :
            rep["description"] = "NA"
        else:
            pass
    except:
        rep["description"] = "NA"
    try:
        rep["typeA"] = soup.find('div', class_="info").li.text.strip()
    except:
        rep["typeA"] = "NA"
    try:
        produits = soup.find("div", string ="Produits :").parent.text.strip().split(":")[1].replace(",","\n").split("\n")[3:]
        prod_list = [prod.strip() for prod in produits]
        rep["produits"] = prod_list

    except:
        rep["produits"] = "NA"
    try:
        rep["typeA2"] = soup.find("div", string ="Marchés :").parent.text.strip().split(":")[1].strip().replace("\n"," ").replace(" / "," ").replace("et ","").split(" ")
    except:
        rep["typeA2"] = "NA"
    try:
        rep["board"] = soup.find("div", class_="contact").strong.text.strip()  #+ " - " nettoyage_chaine(soup.find("div", class_="contact").text.replace("\n"," - ").replace("\r"," - "))split("\n")[4].replace("\n","").replace("\xa0","").p.text.strip()
    except:
        rep["board"] = "NA"
    try:
        rep["email"] = soup.find("div", class_="contact").a.text.strip()
    except:
        rep["email"] = "NA"
    try:
        rep["tel"] = soup.find("div", class_="contact").span.text.strip()
    except:
        rep["tel"] = "NA"
    try:
        rep["site"] = soup.find("div", class_="contact").findAll("a")[1].get("href")
    except:
        rep["site"] = "NA"
    try:
        rep["cluster"] = 'textilesud'
    except:
        rep["cluster"] = 'textilesud'
    return(rep)

url_base = "http://www.textilesud.fr/fr/annuaire.php"
i = 1
j = 1

req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("tbody").findAll("a")

for f in fiches:
    url_fiche = f.get("href")
    print( "fiche: {}".format(url_fiche))
    fiche = lecture_exposant(url_fiche)

    csv_df = csv_df.append(fiche, ignore_index=True)

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "
csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "textilesud")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "textilesud.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "textilesud.xlsx")
