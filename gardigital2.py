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
import numpy as np

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"site",
                u"adresse",
                u"board",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)
pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"
pattern_site = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,}(\/\S*)?"
pattern_linkedin = r"((https?:\/\/)?((www|\w\w)\.)?linkedin\.com\/)((([\w]{2,3})?)|([^\/]+\/(([\w|\d-&#?=])+\/?){1,}))"




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
        rep["societe"] = soup.find("div", "shortdesc").text.strip()
    except:
        rep["societe"] = np.nan
    try:
        adresse = soup.find(string = ' ADRESSE').find_next('p').text.strip()
        rep["adresse"] = adresse
    except:
        rep["adresse"] = np.nan
    try:
        description = soup.find(string = ' ACTIVITE').find_next('p').text.strip()
        rep["description"] = description
    except:
        rep["description"] = np.nan
    try:
        repl = soup.find('div', attrs={"id":u"product_description"}).text.strip()
        repl = repl.replace(" ADHERENTS","").replace(" ADHERENT","").replace(" ADRESSE","").replace(" ACTIVITE","").replace("Description","").replace(" SITE INTERNET","").strip()
        repl = repl.replace(adresse, '').replace(description, '')
        infos = repl.split('\n\n')
        rep["board"] = infos[0].split(',')
    except:
        rep["board"] = np.nan
    try:
        rep["site"] = soup.find('div', attrs={"id":u"product_description"}).find('a').get('href')
    except:
        rep["site"] = np.nan
    try:
        rep["cluster"] = 'gardigital'
    except:
        rep["cluster"] = 'gardigital'

    return(rep)


url_base = "https://www.gardigital.com/entreprises-digital-annuaire-gard/"
while True:
    req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    fiches = soup.find("div", "cs-content").find("div", ["product-list", "grid"]).findAll('a')
    for f in fiches:
            url_fiche = f.get("href")
            print( "fiche: {}".format(url_fiche))
            fiche = lecture_exposant(url_fiche)
           # fiche["id_societe"] = "soc_%d" % i
            #i += 1
            csv_df = csv_df.append(fiche, ignore_index=True)
    try:
        url_base = soup.find("li", "next-page").a.get("href")
        print("page: {}".format(url_base))
    except:
        break


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "gardigital")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "gardigital.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "gardigital.xlsx")
