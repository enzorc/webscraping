#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:02:59 2019

@author: enzo.ramirez
"""

# packages needed are imported
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time



fieldnames = [u"societe",
                u"groupe",
                u"typeA",
                u"descri",
                u"description",
                u"adresse",
                u"email",
                u"tel",
                u"fax",
                u"site",
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
        rep["societe"] = soup.find("h1", class_ = "entry-title").text.split("/")[1].strip() # find get the only (firstNA) element for tag div and class top-area-container it finds, then get the text in the h2 text as we are interested in it
    except:
        rep["societe"] = "NA"
    try:
        groups = soup.find("h4", string="Groupe : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip().split(" et ") # find get the only (firstNA) element for tag div and class top-area-container it finds, then get the text in the h2 text as we are interested in it
        rep["groupe"] = groups
        if rep["groupe"] == """[""]""" :
            rep["groupe"] = "NA"
        else:
            pass
    except:
        rep["groupe"] = "NA"
    try:
        rep["typeA"] = soup.find("h4", string="Secteur : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip().split(" et ")
        if rep["typeA"] == """[""]""" :
            rep["typeA"] = "NA"
        else:
            pass
    except:
        rep["typeA"] = "NA"
    try:
        rep["descri"] = soup.find("h4", string=u"Activité principale : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip() # find get the only (firstNA) element for tag div and class top-area-container it finds, then get the text in the h2 text as we are interested in it
    except:
        rep["descri"] = "NA"
    try:
        rep["adresse"] = soup.find("h4", string="Adresse : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip()
    except:
        rep["adresse"] = "NA"
    try:
        rep["email"] = soup.find("h4", string="E-mail : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip()
    except:
        rep["email"] = "NA"
    try:
        rep["tel"] = soup.find("h4", string="Tél : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip()
    except:
        rep["tel"] = "NA"
    try:
        rep["fax"] = soup.find("h4", string="Fax : ").parent.text.replace("\n","").replace("\t","").split(":")[1].strip()
    except:
        rep["fax"] = "NA"
    try:
        rep["site"] = "http:" + soup.find("div", class_="vert_block").findAll("a", class_="btn_lien")[1].text.replace("\n","").replace("\t","").split(":")[1].strip()
    except:
        rep["site"] = "NA"
    try:
        rep["description"] = soup.find('div', class_="ligne_2").text.replace("\n"," ").replace("\xa0","").replace("Fiche de présentation","").strip()
    except:
        rep["description"] = "NA"
    try:
        rep["cluster"] = 'biomed'
    except:
        rep["cluster"] = 'biomed'

    return(rep)

url_base = "https://www.biomedicalalliance.com/entreprises/"
i = 1
while True:
   req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
   html = urllib.request.urlopen(req).read()
   soup = BeautifulSoup(html)
   fiches = soup.find("div", class_ = "contentgauche").findAll("a", class_ = "lienficheentreprise")

   for f in fiches:
        url_fiche = f.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)

        csv_df = csv_df.append(fiche, ignore_index=True)
        time.sleep(0.5)
   try:
        url_base = soup.find("div", class_ = "nav-next").a.get("href")
        print("page: {}".format(url_base))
   except:
        break


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "biomed")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "biomed.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "biomed.xlsx")
