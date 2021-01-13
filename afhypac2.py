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
                u"description",
                u"tel",
                u"email",
                u"site",
                u"college",
                u"adresse",
                u"board",
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
        rep["societe"] = soup.find("div", class_ = "col-md-9 col-md-push-3 col-sm-12").h1.text.strip().upper()
    except:
        rep["societe"] = "NA"
    try:
        repl = soup.find('div', "col-md-11 col-md-offset-1 corps").find("div", "well").text
        desc = soup.find('div', "col-md-11 col-md-offset-1 corps").text
        rep["description"] = desc.replace(repl, "").replace("\n\n Liste des membres", "").replace("\n"," ").strip()
    except AttributeError:
        rep["description"] = soup.find('div', "col-md-11 col-md-offset-1 corps").p.text.replace("\n"," ").strip()
    except:
        rep["description"] = "NA"
    try:
        rep["board"] = soup.find('div', class_="col-sm-9 col-xs-12").find(string = "Représentant").parent.parent.text.replace("Représentant", "").strip()
    except:
        rep["board"] = "NA"
    try:
        rep["adresse"] = re.sub(  r"(?<=[a-zA-Z])(?=\d)" ," ", soup.find('div', class_="col-sm-9 col-xs-12").find(string = "Adresse").parent.parent.text.replace("Adresse", " ").strip())
    except:
        rep["adresse"] = "NA"
    try:

        rep["email"] = soup.find('div', class_="col-sm-9 col-xs-12").find(string = "E-mail").parent.parent.text.replace("E-mail", "").strip()
    except:
        rep["email"] = "NA"
    try:
        rep["tel"] = soup.find('div', class_="col-sm-9 col-xs-12").find(string = "Téléphone").parent.parent.text.replace("Téléphone", "").strip()
    except:
        rep["tel"] = "NA"
    try:
        rep["site"] = soup.find('div', class_="col-sm-9 col-xs-12").find(string = "Site").parent.parent.text.replace("Site", "").strip()
    except:
        rep["site"] = "NA"
    try:
        rep["college"] = soup.find('div', class_="col-sm-9 col-xs-12").find(string = "Collège").parent.parent.text.replace("Collège", "").split(", ")
        if rep["college"] == """[""]""" :
            rep["college"] = "NA"
        else:
            pass
    except:
        rep["college"] = "NA"
    try:
        rep["cluster"] = 'afhypac'
    except:
        rep["cluster"] = 'afhypac'

    return(rep)


url_base = "http://www.afhypac.org/association/membres/"

i = 1
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "panel-group").findAll("a", "membre")
for f in fiches:
        url_fiche = "http://www.afhypac.org" + f.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
       # fiche["id_societe"] = "soc_%d" % i
        #i += 1
        csv_df = csv_df.append(fiche, ignore_index=True)
        time.sleep(0.05)


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP +"afhypac")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "afhypac.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "afhypac.xlsx")
