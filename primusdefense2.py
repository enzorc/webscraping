#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 09:38:55 2019

@author: enzo.ramirez
"""


import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np

from urllib.error import HTTPError, URLError

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"description_en",
                u"tel",
                u"email",
                u"site",
                u"adresse",
                u"fax",
                u"effectif",
                u"ca",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']
pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"
pattern_site = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,}(\/\S*)?"


csv_df = pd.DataFrame(columns=fieldnames)

def cleanlist(j):
    for a in j:
        a = a.strip()
        try :
            repl = re.search(r'^\w{0,1}$', a).group()
            j.remove(repl)
        except:
            pass
    X = [x.replace('\xa0','').replace('(','').replace(')','').replace('|','').replace('','').replace(':','').strip() for x in j]
    for i in X :
       if len(i) < 2 :
           X.remove(i)
    return X


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
        societe = soup.find("div", "fusion-column-wrapper").h1.text.replace('\n',' ').strip()
        rep["societe"] = societe
    except AttributeError:
        try :
            societe = soup.find("div", "post-content").h2.text.replace('\n',' ').strip()
            rep["societe"] = societe
        except AttributeError:
            try :
                societe = soup.find("div", "fusion-two-third fusion-layout-column fusion-spacing-yes").h1.text.replace('\n',' ').strip()
                rep["societe"] = societe
            except :
                rep["societe"] = np.nan

    try:
        description_en1 = soup.find("div", "fusion-column-wrapper").find(string = 'Fields of expertise').find_previous('p').find_previous().find_all_next(string=True)
        description_en2 = soup.find("div", "fusion-column-wrapper").find(string = 'Références/References').find_all_next(string=True)
        description_en = set(description_en1) - set(description_en2)
        description_en =list(description_en)
        description_en = cleanlist(description_en)
        description_en = ' '.join(description_en)
        rep["description_en"] = description_en.replace('Références/References','').replace('\n',' ').strip()
    except:
        rep["description_en"] = np.nan

    try:
        description1 = soup.find("div", "fusion-column-wrapper").find(string = 'Fields of expertise').find_previous('p').find_previous().find_all_previous(string=True)
        description2 = soup.find("div", "fusion-column-wrapper").h1.find_all_previous(string=True)
        description = set(description1) - set(description2)
        description =list(description)
        description = cleanlist(description)
        description = ' '.join(description)
        rep["description"] = description.replace('Références/References','').replace('\n',' ').strip()
    except:
        rep["description"] = np.nan

    try:
        tel = soup.find('div' , 'sidepanel ci first-part').find(string = 'Tél.').parent.parent.text
        tel = tel.replace('Tél.','')
        rep["tel"] = tel.replace('\n',' ').strip()
    except:
        rep["tel"] = np.nan
    try:
        fax = soup.find('div' , 'sidepanel ci first-part').find(string = 'Fax.').parent.parent.text
        fax = fax.replace('Fax.','')
        rep["fax"] = fax.replace('\n',' ').strip()
    except:
        rep["fax"] = np.nan
    try:
        site = soup.find('div' , 'sidepanel ci first-part').find(string = 'URL').parent.parent.text
        site = site.replace('URL','')
        rep["site"] = site.replace('\n',' ').strip()
    except:
        rep["site"] = np.nan

    try:
        email = soup.find('div' , 'sidepanel ci first-part').text
        email = re.search(pattern_mail, email).group()
        rep["email"] = email.replace('\n',' ').strip()
    except:
        rep["email"] = np.nan

    try:
        adresse = soup.find('div' , 'sidepanel ci first-part').find(string = 'Siège').parent.parent.text
        adresse = adresse.replace('Siège','')
        rep["adresse"] = adresse.replace('\n',' ').strip()
    except:
        rep["adresse"] = np.nan
    try:
        effectif = soup.find('div' , 'sidepanel ci first-part').find(string = 'Effectif').parent.parent.text
        effectif = effectif.replace('Effectif','')
        rep["effectif"] = effectif.replace('\n',' ').strip()
    except:
        rep["effectif"] = np.nan
    try:
        ca = soup.find('div' , 'sidepanel ci first-part').strong.next_element.next_element.next_element
        ca = ca.replace('€','').replace('M','000000').replace('K','000')
        rep["ca"] = ca.replace('\n',' ').strip()
    except:
        rep["ca"] = np.nan

    try:
        rep["cluster"] = 'primusdefense'
    except:
        rep["cluster"] = 'primusdefense'

    return(rep)


url_base = "http://www.primusdefensesecurite.fr/nos-membres/"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "fusion-content-boxes").findAll("a")
for f in fiches:
        url_fiche = f.get("href")
        print( "fiche: {}".format(url_fiche))
        try:
            fiche = lecture_exposant(url_fiche)
        except HTTPError:
            continue
       # fiche["id_societe"] = "soc_%d" % i
        #i += 1
        csv_df = csv_df.append(fiche, ignore_index=True)

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "primusdefense")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "primusdefense.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "primusdefense.xlsx")
