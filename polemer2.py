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
from selenium import webdriver
from urllib.error import HTTPError, URLError

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"email",
                u"site",
                u"tel",
                u"board",
                u"adresse",
                u"siren",
                u"ape",
                u"effectif",
                u"fax",
                u"capital",
                u"typesociete",
                u"domaineA",
                u"clients",
                u"produits",
                u"sous_traitance_realise",
                u"sous_traitance_confie",
                u"certifications",
                u"ca",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"
pattern_site = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,}(\/\S*)?"

SCROLL_PAUSE_TIME = 0.5


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
        rep["societe"] = soup.find('div', 'fusion-page-title-captions').h1.text.strip()
    except:
        rep["societe"] = np.nan
    try:
        typeA = soup.find('div', "fiche-entreprise").find(string = 'Secteur(s) : ').parent.parent.text.strip()
        typeA = typeA.replace('Secteur(s) : ','').strip()
        typeA = remlist(striplist(typeA.split(',')))
        rep["typeA"] = typeA
    except:
        rep["typeA"] = np.nan
    try:
        email = soup.find('div', "fiche-entreprise").find(string = 'Courriel : ').parent.parent.text.strip()
        email = email.replace('Courriel : ','').strip()
        rep["email"] = email
    except:
        rep["email"] = np.nan
    try:
        site = soup.find('div', "fiche-entreprise").find(string = 'Web : ').parent.parent.text.strip()
        site = site.replace('Web : ','').strip()
        rep["site"] = site
    except:
        rep["site"] = np.nan

    try:
        tel = soup.find('div', "fiche-entreprise").find(string = 'Téléphone : ').parent.parent.text.strip()
        tel = tel.replace('Téléphone : ','').strip()
        rep["tel"] = tel
    except:
        rep["tel"] = np.nan

    try:
        board = soup.find('div', "fiche-entreprise").findAll('div', 'fusion-separator fusion-full-width-sep sep-double')[1].find_next('ul').findAll('li')
        board = [ i.text.strip() for i in board ]
        rep["board"] = board
    except:
        rep["board"] = np.nan

    try:
        adresse = soup.find('div', "fiche-entreprise").find(string = 'Adresse : ').parent.parent.text.strip()
        adresse = adresse.replace('Adresse : ','').strip()
        rep["adresse"] = adresse
    except:
        rep["adresse"] = np.nan

    try:
        siren = soup.find('div', "fiche-entreprise").find(string = 'Siren : ').parent.parent.text.strip()
        siren = siren.replace('Siren : ','').strip()
        rep["siren"] = siren
    except:
        rep["siren"] = np.nan

    try:
        ape = soup.find('div', "fiche-entreprise").find(string = 'Ape : ').parent.parent.text.strip()
        ape = ape.replace('Ape : ','').strip()
        rep["ape"] = ape
    except:
        rep["ape"] = np.nan

    try:
        effectif = soup.find('div', "fiche-entreprise").find(string = 'Effectif : ').parent.parent.text.strip()
        effectif = effectif.replace('Effectif : ','').strip()
        rep["effectif"] = effectif
    except:
        rep["effectif"] = np.nan

    try:
        description = soup.find('div', "fiche-entreprise").find(string = 'Savoir-faire : ').parent.parent.text.strip()
        description = description.replace('Savoir-faire : ','').strip()
        rep["description"] = description
    except:
        rep["description"] = np.nan


    try:
        fax = soup.find('div', "fiche-entreprise").find(string = 'Télécopie: ').parent.parent.text.strip()
        fax = fax.replace('Télécopie: ','').strip()
        rep["fax"] = fax
    except:
        rep["fax"] = np.nan


    try:
        capital = soup.find('div', "fiche-entreprise").find(string = 'Capital : ').parent.parent.text.strip()
        capital = capital.replace('Capital : ','').replace('€','').strip()
        rep["capital"] = capital
    except:
        rep["capital"] = np.nan


    try:
        typesociete = soup.find('div', "fiche-entreprise").find(string = 'Forme Juridique : ').parent.parent.text.strip()
        typesociete = typesociete.replace('Forme Juridique : ','').strip()
        rep["typesociete"] = typesociete
    except:
        rep["typesociete"] = np.nan


    try:
        domaineA = soup.find('div', "fiche-entreprise").find(string = 'Marchés : ').parent.parent.text.strip()
        domaineA = domaineA.replace('Marchés : ','').replace(".","").strip()
        if   bool(re.search(r',',domaineA)) == True:
            domaineA = remlist(striplist(domaineA.split(',')))
        elif bool(re.search(r'-',domaineA)) == True:
            domaineA = remlist(striplist(domaineA.split('-')))
        elif bool(re.search(r';',domaineA)) == True:
            domaineA = remlist(striplist(domaineA.split(';')))
        rep["domaineA"] = domaineA
    except:
        rep["domaineA"] = np.nan


    try:
        clients = soup.find('div', "fiche-entreprise").find(string = 'Clients : ').parent.parent.text.strip()
        clients = clients.replace('Clients : ','').replace(".","").strip()
        if   bool(re.search(r'-',clients)) == True:
            clients = remlist(striplist(clients.split('-')))
        elif bool(re.search(r'/',clients)) == True:
            clients = remlist(striplist(clients.split('/')))
        elif bool(re.search(r';',clients)) == True:
            clients = remlist(striplist(clients.split(';')))
        elif bool(re.search(r',',clients)) == True:
            clients = remlist(striplist(clients.split(',')))

        rep["clients"] = clients
    except:
        rep["clients"] = np.nan


    try:
        produits = soup.find('div', "fiche-entreprise").find(string = 'Produits propres : ').parent.parent.text.strip()
        produits = produits.replace('Produits propres : ','').strip()
        if   bool(re.search(r',',produits)) == True:
            produits = remlist(striplist(produits.split(',')))
        elif bool(re.search(r'/',produits)) == True:
            produits = remlist(striplist(produits.split('/')))

        rep["produits"] = produits
    except:
        rep["produits"] = np.nan


    try:
        sous_traitance_realise = soup.find('div', "fiche-entreprise").find(string = 'Sous-traitance réalisée : ').parent.parent.text.strip()
        sous_traitance_realise = sous_traitance_realise.replace('Sous-traitance réalisée : ','').strip()
        rep["sous_traitance_realise"] = sous_traitance_realise
    except:
        rep["sous_traitance_realise"] = np.nan


    try:
        sous_traitance_confie = soup.find('div', "fiche-entreprise").find(string = 'Sous-traitance confiée : ').parent.parent.text.strip()
        sous_traitance_confie = sous_traitance_confie.replace('Sous-traitance confiée : ','').strip()
        rep["sous_traitance_confie"] = sous_traitance_confie
    except:
        rep["sous_traitance_confie"] = np.nan


    try:
        certifications = soup.find('div', "fiche-entreprise").find(string = 'Certification : ').parent.parent.text.strip()
        certifications = certifications.replace('Certification : ','').replace('.','').strip()
        if   bool(re.search(r',',certifications)) == True:
            certifications = remlist(striplist(certifications.split(',')))
        elif bool(re.search(r'/',certifications)) == True:
            certifications = remlist(striplist(certifications.split('/')))
        elif bool(re.search(r'\n',certifications)) == True:
            certifications = remlist(striplist(certifications.split('\n')))
        rep["certifications"] = certifications
    except:
        rep["certifications"] = np.nan

    try:
        ca = soup.find('div', "fiche-entreprise").find(string = '''Chiffre d'affaires : ''').parent.parent.text.strip()
        ca = ca.replace('''Chiffre d'affaires : ''','').strip()
        rep["ca"] = ca
    except:
        rep["ca"] = np.nan


    try:
        rep["cluster"] = 'polemer'
    except:
        rep["cluster"] = 'polemer'

    return(rep)



WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
browser = webdriver.Chrome(WEBDRIVER)
browser.get("https://www.polemermediterranee.com/Reseau/Annuaire-des-membres")
while True:
    try:
        browser.find_element_by_xpath('''//*[@id="annuaire"]/div/div[4]/p/a''').click()
        time.sleep(0.5)
    except:
        break


html = browser.page_source
soup = BeautifulSoup(html)
fiches = soup.find("div", "fusion-portfolio-wrapper").findAll("div", "fusion-portfolio-content")

for f in fiches:
        url_fiche = f.a.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)

        csv_df = csv_df.append(fiche, ignore_index=True)


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "polemer")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "polemer.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "polemer.xlsx")
print('saved!')

