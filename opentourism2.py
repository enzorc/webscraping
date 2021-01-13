#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:27:02 2019

@author: enzo.ramirez
"""

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time



fieldnames = [u"societe",
                u"description",
                u"tel",
                u"email",
                u"site",
                u"board",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)


# req = urllib.request.Request("https://www.opentourismelab.com/les-startups/item/dahub.html", headers={'User-Agent': 'Mozilla/5.0'})

def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    print (soup.title.text)

    rep = {}
    try:
        rep["societe"] = soup.find("h1").text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["description"] = soup.find('div', class_="uk-margin element element-textarea").text.replace("\n"," ").replace("\xa0","").strip()
    except:
        rep["description"] = "NA"
    try:
        rep["tel"] = soup.find("li", class_="tel").text.strip()
    except:
        rep["tel"] = "NA"
    try:
        rep["email"] = soup.find("li", class_="email").text.strip()
    except:
        rep["email"] = "NA"
    try:
        rep["site"] = soup.find("li", class_="site").text.strip()
    except:
        rep["site"] = "NA"
    try:
        names = soup.find("ul", class_="uk-grid element element-relateditems").findAll("h4", class_ ="uk-margin-remove")
        names_list = [name.text.strip() for name in names]
        postes = soup.find("ul", class_="uk-grid element element-relateditems").findAll("li", class_ ="element element-text")
        poste_list = [poste.text.strip() for poste in postes]
        board = [names_list[i]+ " - " + poste_list[i] for i in range(len(poste_list))]
        rep["board"] = board
        if rep["board"] == """[""]""" :
            rep["board"] = "NA"
        else:
            pass
    except:
        rep["board"] = "NA"
    try:
        rep["cluster"] = 'opentourism'
    except:
        rep["cluster"] = 'opentourism'
    return(rep)

url_base = "https://www.opentourismelab.com/les-startups.html"
i = 1
j = 1

req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", class_ = "uk-panel uk-panel-box").findAll("a", class_ ="read-more")

for f in fiches:
    url_fiche = "https://www.opentourismelab.com" + f.get("href")
    print( "fiche: {}".format(url_fiche))
    fiche = lecture_exposant(url_fiche)

    csv_df = csv_df.append(fiche, ignore_index=True)
    time.sleep(0.05)

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "opentourism")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "opentourism.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "opentourism.xlsx")


