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
                u"tel",
                u"site",
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
pattern_teri = r"^(\s|\.)?[Contact]\s*(?:\S[\t ]*){4,}"

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


def striplist(l):
    return([x.strip() for x in l])

def remlist(i) :
    if '' in i: i.remove('')
    return i

def cleanteri(i,j):
        for element in i:
            if element in j:
                i.remove(element)
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
        texte = soup.find('div', "responsive-handler fr-view breakable").text.replace('\xa0','').strip()
        tel_ = re.search(pattern_phone, texte).group()
        texte = texte.replace(tel_,'')
        tel = tel_.replace('-', ' ')
        texte = texte.replace(tel,'')
        try :
            tel2 = re.search(pattern_phone, texte).group()
            texte = texte.replace(tel2,'')
            tel = [tel +'  ' + tel2]
            rep["tel"] = tel
        except :
            pass
        rep["tel"] = tel
    except:
        rep["tel"] = np.nan
    try:
        rep["societe"] = soup.find("div", "col-xs-12 text-center").text.strip()
    except:
        rep["societe"] = np.nan
    try:
        board = soup.find("strong", string = "Contact").next_element.next_element.replace('\xa0','').replace(':','').replace('(','').strip()
        texte = texte.replace(board,"").strip()
        texte = texte.replace('http://', ' http://')
        rep["board"] = board
    except:
        rep["board"] = np.nan
    try:
        email = re.search(pattern_mail, texte).group()
        texte = texte.replace(email,'').replace('()','').replace('|','')
        try :
            email2 = re.search(pattern_mail, texte).group()
            texte = texte.replace(email2,'')
            email = [email , email2]
            rep["email"] = email
        except :
            pass
        rep["email"] = email
    except:
        rep["email"] = np.nan

    try:
        rep["cluster"] = 'terinov'
    except:
        rep["cluster"] = 'terinov'
    try:
        sites = texte.split('Contact')[1]
        sites = sites.replace('http://', ' http://')
        sites = sites.replace('.com/', '.com/ ')
        site = cleanteri(sites , email)
        site = re.search(pattern_site, sites).group()
        texte = texte.replace(site,"").strip()
        rep["site"] = site
    except:
        rep["site"] = np.nan
    try:
        description = texte.split('Contact')[0]
        texte = texte.replace("\r", "").replace("\n", "").replace(description, "")
        rep["description"] = description
    except:
       rep["description"] = np.nan
    try:
        adresse1 = soup.find("strong", string = "Contact").find_all_next(string=True)
        adresse2 = soup.find("footer", "global_footer footer_2").find_all_next(string=True)
        adresse = set(adresse1) - set(adresse2)
        adresse =list(adresse)
        try:
            adresse = cleanteri(adresse, site)
        except:
            pass
        try:
            adresse = cleanteri(adresse, board)
        except:
            pass
        try:
            adresse = cleanteri(adresse, email)
        except:
            pass
        try:
            adresse = cleanteri(adresse, tel)
        except:
            pass
        try:
            adresse = cleanteri(adresse, tel_)
        except:
            pass
        try:
            adresse = cleanteri(adresse, site)
        except:
            pass
        try:
            adresse = cleanlist(adresse)
        except:
            pass
        try:
            adresse = cleanteri(adresse, site)
        except:
            pass
        try:
            adresse = cleanteri(adresse, board)
        except:
            pass
        try:
            adresse = cleanteri(adresse, email)
        except:
            pass
        try:
            adresse = cleanteri(adresse, tel)
        except:
            pass
        try:
            adresse = cleanteri(adresse, site)
        except:
            pass
        for i in adresse:
            if bool(re.search(pattern_mail, i)) ==True :
                print(i)
                adresse.remove(i)
        for i in adresse:
            if bool(re.search(pattern_phone, i)) ==True :
                print(i)
                adresse.remove(i)
        for i in adresse:
            if bool(re.search(pattern_site, i)) ==True :
                print(i)
                adresse.remove(i)
        adresse = ' '.join(adresse)
        adresse
        rep["adresse"] = adresse
    except:
        rep["adresse"] = np.nan
    try:
        site = re.search(pattern_site, adresse).group()
        rep["site"] = site
    except:
        rep["site"] = np.nan


    return(rep)

#WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
#browser = webdriver.Chrome(WEBDRIVER)

url_base = "https://www.terinov.com/"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "site_container").ul.find("ul", "site-dropdown-menu").findAll("a")
for f in fiches:
        url_fiche = 'https://www.terinov.com' + f.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)

        csv_df = csv_df.append(fiche, ignore_index=True)

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "terinov")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "terinov.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "terinov.xlsx")
print(' Saved ! ')
