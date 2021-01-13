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
from selenium import webdriver

fieldnames = [#u"id_societe",
                u"societe",
                u"description",
                u"tel",
                u"email",
                u"site",
                u"produits",
                u"fax",
                u"board",
                u"adresse",
                u"certifications",
                u"domaineA",
                u"typeA",
                u"cluster",
                u"ca",
                u"effectif",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"


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
    #req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html)


    rep = {}
    try:
        rep["societe"] = soup.find('div', attrs={"id" : "pdfapp_comp___name_ro"}).text
    except:
        rep["societe"] = np.nan
    try:
        texte = soup.find('div', attrs={"id" : "pdfapp_comp___rail_activities_ro"}).text
        texte_2 = soup.find('div', attrs={"id" : "pdfapp_comp___products_ro"}).text
        rep["description"] = texte + ' ' + texte_2
    except:
        rep["description"] = np.nan
    try:
        produit = soup.find("div", "row-fluid").find("div", "row-fluid").find("div", "row-fluid").text.replace("Principaux produits ferroviaires","")
        produit = produit.replace("\n","").split("•")
        produit = striplist(produit)
        produit = remlist(produit)
        rep["produits"] = produit
    except:
        rep["produits"] = np.nan
    try:
        rep["adresse"] = soup.find("div", "col-lg-3").find_next("div", "col-lg-3").text.strip()
    except:
        rep["adresse"] = np.nan
    try:
        tel = soup.find("div", attrs={"id":"pdfapp_comp___tel_ro"}).text
        tel = re.search(pattern_phone, tel).group()
        rep["tel"] = tel
    except:
        rep["tel"] = np.nan
    try:
        fax = soup.find("div", attrs={"id":"pdfapp_comp___fax_ro"}).text
        fax = re.search(pattern_phone, fax).group()
        rep["fax"] = fax
    except:
        rep["fax"] = np.nan
    try:
        board = soup.find("div", attrs={"id":"pdfapp_comp___contact_ro"}).text
        board = board.replace("Contact : ","")
        rep["board"] = board
    except:
        rep["board"] = np.nan
    try:
        email = soup.find("div", attrs={"id":"pdfapp_comp___email_ro"}).span.a.text
        rep["email"] = email
    except:
        rep["email"] = np.nan
    try:
        site = soup.find("div", attrs={"id":"pdfapp_comp___website_ro"}).text
        rep["site"] = site
    except:
        rep["site"] = np.nan
    try:
        effectif = soup.find("div", attrs={"id":"pdfapp_comp___employees_ro"}).text
        rep["effectif"] = effectif
    except:
        rep["effectif"] = np.nan
    try:
        #ca1 = soup.find("div", attrs={"id":"pdfapp_comp___ca_ro"}).text
        ca2 = soup.find("div", attrs={"id":"pdfapp_comp___ca_ro"}).find_next().text
        ca3 = soup.find("div", "col-lg-6").find_next("div", "col-lg-6").text
        ca4 = ca3.replace(ca2,"").replace('()',"").replace('CA Annuel',"").replace('€',"")
        ca = ca4.strip()
        if 'k' in ca:
            ca = ca.replace("k",'000')
        rep["ca"] = ca
    except:
        rep["ca"] = np.nan

    try:
        certifications = soup.find("div", "row-fluid col-lg-4 colspemmb").find('div', 'row-fluid col-lg-12').find_next("div","row-fluid col-lg-12").text
        certifications = certifications.replace('Certifications','').replace('\n','').split('•')
        certifications = remlist(certifications)
        certifications = striplist(certifications)
        rep["certifications"] = certifications
    except:
        rep["certifications"] = np.nan

    try:
        domaineA = soup.find("h3", string = "Marchés").parent.text
        domaineA = domaineA.replace('Marchés','').replace('\n','').split('•')
        domaineA = remlist(domaineA)
        domaineA = striplist(domaineA)
        rep["domaineA"] = domaineA
    except:
        rep["domaineA"] = np.nan

    try:
        typeA = soup.find("div", "row-fluid col-lg-12 orbloc").text
        typeA = typeA.replace('Spécialisation','').replace('Compétences métier','').replace('\n','').split('-')
        typeA = striplist(typeA)
        typeA = remlist(typeA)
        rep["typeA"] = typeA
    except:
        rep["typeA"] = np.nan

    try:
        rep["cluster"] = 'mipirail'
    except:
        rep["cluster"] = 'mipirail'

    return(rep)

WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
browser = webdriver.Chrome(WEBDRIVER)


url_base = "https://www.mipirail.com/fr/membres"
req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html)
fiches = soup.find("div", "fabrik_groupdata").findAll("a")
for f in fiches:
        url_ext = f.get("href")
        url_fiche = "https://www.mipirail.com/" + url_ext
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
       # fiche["id_societe"] = "soc_%d" % i
        #i += 1
        csv_df = csv_df.append(fiche, ignore_index=True)
PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "
csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "mipirail")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "mipirail.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "mipirail.xlsx")
