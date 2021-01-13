#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:02:13 2019

@author: enzo.ramirez
"""


import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
#from selenium import webdriver

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"site",
                u"typeA",
                u"tel",
                u"email",
                u"board",
                u"adresse",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

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
    #browser.get("https://www.nautipole.fr/entreprise/atout-bois-66lr/")
    #html = browser.page_source
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)


    rep = {}
    try:
        rep["societe"] = societe[i].text
    except:
        rep["societe"] = np.nan
    try:
        infos = soup.find("div", "vc_column-inner vc_custom_1532359577405").text.replace('\n',' ').strip()
        mail = re.search(pattern_mail, infos).group()
        rep["email"] = mail
        infos = infos.replace(mail, ' ').replace('E-mail :', ' ')
    except:
        rep["email"] = np.nan
    try:
        texte = soup.find('div', "vc_row wpb_row vc_inner vc_row-fluid").find_previous("div").text.strip()
        rep["description"] = texte
    except:
        rep["description"] = np.nan
    try:
        typeA = soup.find('div', "vc_row wpb_row vc_inner vc_row-fluid vc_custom_1532360686780 vc_row-has-fill").find_previous("div").text
        typeA = typeA.replace("Compétences :","").strip().split('\n')
        typeA = striplist(typeA)
        typeA = remlist(typeA)
        rep["typeA"] = typeA
    except:
        rep["typeA"] = np.nan
    try:
        adresse = soup.find("div", "vc_row wpb_row vc_inner vc_row-fluid vc_custom_1532360686780 vc_row-has-fill").find("div", "vc_column-inner vc_custom_1532359565886").p.text.replace('\n',' ').strip()
        rep["adresse"] = adresse
    except:
        rep["adresse"] = np.nan
    try:
        tel = re.search(pattern_phone, infos).group()
        infos = infos.replace(tel, ' ').replace('Tél.', ' ')
        rep["tel"] = tel
    except:
        rep["tel"] = np.nan
    try:
        board = soup.find("div", "vc_row wpb_row vc_inner vc_row-fluid vc_custom_1532360686780 vc_row-has-fill").find("div", "vc_column-inner vc_custom_1532359565886").text.replace('\n',' ').strip()
        board = board.replace(adresse,"").strip()
        rep["board"] = board
    except:
        rep["board"] = np.nan
    try:
        site = re.search(pattern_site, infos).group()
        rep["site"] = site
    except:
        rep["site"] = np.nan
    try:
        rep["cluster"] = 'nautipole'
    except:
        rep["cluster"] = 'nautipole'

    return(rep)

#WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
#browser = webdriver.Chrome(WEBDRIVER)

url_base = "https://www.nautipole.fr/entreprises/"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "content").find("div", "row").findAll("a")
societe = soup.find("div", "content").find("div", "row").findAll("div", "texte")
i=0
for f in fiches:
        url_fiche = f.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
        i+=1

        csv_df = csv_df.append(fiche, ignore_index=True)
PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "
csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "nautipole")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "nautipole.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "nautipole.xlsx")
