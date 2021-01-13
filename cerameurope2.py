#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:23:52 2019

@author: enzo.ramirez
"""
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import urllib.request

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"description_en",
                u"descri",
                u"adresse",
                u"typeA",
                u"site",
                u"email",
                u"tel",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']



WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
browser = webdriver.Chrome(WEBDRIVER)
browser.get("https://www.cerameurop.com/maps/")
#html = browser.page_source

pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"
pattern_site = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,}(\/\S*)?"

csv_df = pd.DataFrame(columns=fieldnames)


def striplist(l):
    return([x.strip() for x in l])


def remlist(i) :
    if '' in i: i.remove('')
    return i


def nettoyage_chaine(chaine):
    chaine = chaine.strip()
    chaine = re.sub(r'\s+',' ', chaine)
    return chaine


def lecture_exposant(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    #browser.get("https://www.cerameurop.com/adherents/")
    #html = browser.page_source
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)

    rep = {}
    try:
        societe = soup.find('div', "et_pb_text_inner").text.replace('\xa0','').strip()
        rep["societe"] = societe
    except:
        rep["societe"] = np.nan
    try:
        infos = soup.find("div", ["et_pb_row et_pb_row_1"]).text.strip().replace(societe,' ').strip().replace('\n',' ')
        email = re.search(pattern_mail, infos).group()
        infos = infos.replace(email,'')
        infos = infos.replace('Contact','')
        rep["email"] = email
    except:
        rep["email"] = np.nan
    try:
        descri = soup.find("div", ["et_pb_column" , "et_pb_column_1_2"]).text.strip().replace(societe,' ').strip()
        rep["descri"] = descri
    except:
        rep["descri"] = np.nan
    try:
        site = re.search(pattern_site, infos).group()
        infos = infos.replace(site,'')
        rep["site"] = site
    except:
        rep["site"] = np.nan
    try:
        tel = re.search(pattern_phone, infos).group()
        infos = infos.replace(tel,'')
        rep["tel"] = tel
    except:
        rep["tel"] = np.nan
    try:
        typeA = soup.find("div", ["et_pb_row et_pb_row_1"]).find('span', string = 'Catégories').parent.text.replace('Catégories','').strip()
        infos = infos.replace(typeA,'')
        infos = infos.replace('Catégories','')
        rep["typeA"] = typeA
    except:
        rep["typeA"] = np.nan
    try:
        adresse = infos.strip()
        rep["adresse"] = adresse
    except:
        rep["adresse"] = np.nan
    try:
        description = soup.find("div", [" et_pb_row" ,"et_pb_row_2"]).findAll('p')
        try:
            description2 = soup.find("div", [" et_pb_row" ,"et_pb_row_2"]).findAll('ul')
            description = description[0].text.strip() + description2[0].text.strip()
            description = description.replace('\n',' ').replace('\xa0','')
        except :
            description = soup.find("div", [" et_pb_row" ,"et_pb_row_2"]).findAll('p')
            description = description[0].text.strip()
        rep["description"] = description.replace('\xa0','')
    except:
        rep["description"] = np.nan
    try:
        description_en = soup.find("div", [" et_pb_row" ,"et_pb_row_2"]).findAll('p')
        try:
            description_en2 = soup.find("div", [" et_pb_row" ,"et_pb_row_2"]).findAll('ul')
            description_en = description_en[1].text.strip() + description_en2[1].text.strip()
            description_en = description_en.replace('\n',' ').replace('\xa0','')
        except :
            description_en = soup.find("div", [" et_pb_row" ,"et_pb_row_2"]).findAll('p')
            description_en = description_en[1].text.strip()
        rep["description_en"] = description_en.replace('\xa0','')
    except:
        rep["description_en"] = np.nan
    try:
        rep["cluster"] = 'cerameurope'
    except:
        rep["cluster"] = 'cerameurope'

    return(rep)

i = 0

while True :
    result = browser.execute_script("""return mcpherData["cJobject"]["""+ str(i) +"""]["content"]""")
    soup = BeautifulSoup(result)
    sites = soup.findAll('a')
    fiche = sites[1].get("href")
    print(i)
    print(fiche)
    i+=1
    try:
     soc_ad = lecture_exposant(fiche)
    except :
     continue
    csv_df = csv_df.append(soc_ad, ignore_index=True)
    if i ==127:
        break


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "cerameurope")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "cerameurope.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "cerameurope.xlsx")

