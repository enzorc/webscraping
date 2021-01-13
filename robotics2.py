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
                u"description",
                u"adresse",
                u"tel",
                u"effectif",
                u"typeA",
                u"site",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)


def list_dict(nest):
    i = 0
    x = []
    for e in nest:
        i+=1
        x.append("tag" + str(i))
        x.append(str(e))

        nested = dict(x[i:i+2] for i in range(0, len(x), 2))
    return nested

def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    print (soup.title.text)

    rep = {}
    try:
        rep["societe"] = soup.find("h1", class_= "fiche-title title pure-u-1").text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["description"] = soup.find('div', class_="txt-fiche").text.replace("\n"," ").replace("\xa0","").strip()
    except:
        rep["description"] = "NA"
    try:
        rep["adresse"] = soup.find("span", string="Adresse : ").parent.text.split(":")[1].strip()
    except:
        rep["adresse"] = "NA"
    try:
        rep["tel"] = soup.find("span", string="Tél : ").parent.text.split(":")[1].strip()
        if rep["tel"] == "" :
            rep["tel"] = "NA"
        else:
            pass
    except:
        rep["tel"] = "NA"
    try:
        rep['effectif'] =  soup.find("span", string='Effectif : ').parent.text.split(":")[1].strip()
        if rep["effectif"] == "" :
            rep["effectif"] = "NA"
        else:
            pass
    except:
        rep['effectif'] = 'NA'
    try:
        tags = "".join(soup.find("span", string = "Compétences : ").parent.text.split(":")[1:]).split(",")
        tags_list = [tag.strip() for tag in tags]
        rep["typeA"] = tags_list
        if rep["typeA"] == """['']""" :
            rep["typeA"] = "NA"
        else:
            pass
    except:
        rep["typeA"] = "NA"
    try:
        rep["site"] = soup.find("div",class_="company-infos whiteBg").find("a").get("href").strip()
        if rep["site"] == "" :
            rep["site"] = "NA"
        else:
            pass
    except:
        rep["site"] = "NA"
    try:
        rep["cluster"] = 'robotics'
    except:
        rep["cluster"] = 'robotics'
    return(rep)

url_base = "https://www.robotics-place.com/annuaire/"
i = 1
j = 1
while True:
    req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    fiches = soup.find("ul", class_ = "pure-u-1").findAll("a", href = re.compile("^https://www.robotics-place.com/"))
    for f in fiches:
            url_fiche = f.get("href")
            print( "fiche: {}".format(url_fiche))
            fiche = lecture_exposant(url_fiche)

            csv_df = csv_df.append(fiche, ignore_index=True)
            time.sleep(0.05)
    try:
            j+=1
            url_base = "https://www.robotics-place.com/annuaire/"+"?fwp_paged=" + str(j)
            print("page: {}".format(url_base))
            if url_base == "https://www.robotics-place.com/annuaire/?fwp_paged=5":
                raise NameError('finish')
    except NameError:
            break

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "robotics")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "robotics.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "robotics.xlsx")
