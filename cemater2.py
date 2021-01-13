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
import time
#from selenium import webdriver
#from urllib.error import HTTPError, URLError

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"email",
                u"site",
                u"tel",
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
    #browser.get("https://www.cemater.fr/entreprise/atout-bois-66lr/")
    #html = browser.page_source

    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)


    rep = {}
    try:
        rep["societe"] = soup.find('div', 'top-page').h1.text
    except:
        rep["societe"] = np.nan
    try:
        description = soup.find('div', "span-11").find("div", "span-7 first").text.strip()
        rep["description"] = description
    except:
        rep["description"] = np.nan
    try:
        email = soup.find("div", attrs = {'id' :'sidebar'}).find('div','element').a.get('href').replace('mailto:','')
        rep["email"] = email
    except:
        rep["email"] = np.nan
    try:
        infos = soup.find("div", attrs = {'id' :'sidebar'}).findAll('div','element')[1].text
        tel = re.search(pattern_phone, infos).group()
        rep["tel"] = tel
    except:
        rep["tel"] = np.nan
    try:
        adresse = soup.find("div", attrs = {'id' :'sidebar'}).findAll('div','element')[1].text
        adresse = adresse.replace('Tél :','').replace(tel,'').strip()
        rep["adresse"] = adresse
    except:
        rep["adresse"] = np.nan
    try:
        board = soup.find("div", attrs = {'id' :'sidebar'}).find('div','element').text.replace('Contact : ',' ').replace(email,'').strip()
        rep["board"] = board
    except:
        rep["board"] = np.nan
    try:
        site = soup.find('div', 'span-4 last').a.get('href')
        rep["site"] = site
    except:
        rep["site"] = np.nan
    try:
        rep["cluster"] = 'cemater'
    except:
        rep["cluster"] = 'cemater'

    return(rep)

#WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
#browser = webdriver.Chrome(WEBDRIVER)

url_base = "http://cemater.com/cemater-entreprises/liste-entreprises"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)

while True:
    req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    fiches = soup.find("div", "span-12 first").findAll("div", "span-3 first nom")

    for f in fiches:
            url_fiche = f.a.get("href")
            print( "fiche: {}".format(url_fiche))
            fiche = lecture_exposant(url_fiche)

            csv_df = csv_df.append(fiche, ignore_index=True)
    time.sleep(2)
    try:
        url_base = soup.find('div', 'wp-pagenavi').find('a', 'nextpostslink').get('href')
    except:
        break

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "cemater")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "cemater.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "cemater.xlsx")
print('saved!')
