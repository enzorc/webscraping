#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 13:47:15 2019

@author: enzo.ramirez
"""


from bs4 import BeautifulSoup
import urllib.request
import pandas as pd



fieldnames = [u"typeA",
                u"societe",
                u"description",
                u"tel",
                u"mobile",
                u"email",
                u"site",
                u"adresse",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)



def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    print (soup.title.text)


    rep = {}
    try:
        rep["societe"] = soup.find("div", class_ = "page-header-content").text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["description"] = soup.find('div', class_="sabai-directory-body").text.replace("\n"," ").replace("\xa0","").replace("\x85"," ").replace("\x9c","").strip()
    except:
        rep["description"] = "NA"
    try:
        typeA = soup.find("div", class_="sabai-directory-category").findAll("a")
        tags_list = [tag.text.strip() for tag in typeA]
        rep["typeA"] = tags_list
        if rep["typeA"] == """[""]""" :
            rep["typeA"] = "NA"
        else:
            pass
    except:
        rep["typeA"] = "NA"
    try:
        rep["email"] = soup.find("div", class_="sabai-directory-contact-email").text.strip()
    except:
        rep["email"] = "NA"
    try:
        rep["site"] = soup.find("div", class_="sabai-directory-contact-website").text.strip()
    except:
        rep["site"] = "NA"
    try:
        rep["tel"] = soup.find("div", class_="sabai-directory-contact-tel").a.text.strip()
    except:
        rep["tel"] = "NA"
    try:
        rep["mobile"] = soup.find("div", class_="sabai-directory-contact-mobile").a.text.strip()
    except:
        rep["mobile"] = "NA"
    try:
        rep["adresse"] = soup.find("div", class_="sabai-directory-location").text.strip()
    except:
        rep["adresse"] = "NA"
    try:
        rep["cluster"] = 'vinseo'
    except:
        rep["cluster"] = 'vinseo'
    return(rep)

url_base = "http://www.vinseo.com/les-membres/directory/"
i = 1
j = 1

req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", class_ = "sabai-directory-listings-container").find("div", class_ = "sabai-row").findAll("div", class_ ="sabai-directory-photos")

for f in fiches:
    url_fiche = f.a.get("href")
    print( "fiche: {}".format(url_fiche))
    fiche = lecture_exposant(url_fiche)

    csv_df = csv_df.append(fiche, ignore_index=True)

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "vinseo")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "vinseo.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "vinseo.xlsx")
