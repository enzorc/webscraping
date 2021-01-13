#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:08:59 2019

@author: enzo.ramirez
"""

import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from selenium import webdriver
import time



pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7}))"
pattern_site = r"(https?:\/\/)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[\w]{2,}(\/\S*)?"

fieldnames = [u"societe",
                u"adresse",
                u"email",
                u"tel",
                u"emplacement",
                u"presence",
                u"typeA",
                u"site",
                u"description",
                u"board",
                u"salon",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']


def nettoyage_chaine(chaine):
    chaine = chaine.strip()
    chaine = re.sub('\s+',' ', chaine)
    return chaine.encode("utf-8")


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

    rep = {}
    try:
        rep["societe"] = soup.find("div", attrs={"class":u"colorP"}).text.strip() # find get the only (firstNA) element for tag div and class top-area-container it finds, then get the text in the h2 text as we are interested in it
    except:
        rep["societe"] = "NA"
    try:
        addresse_tel = soup.find("div", attrs={"class":u"col-xs-11 col-sm-11 col-md-10"}).text.replace("\n", " ").replace("\t", " ").replace("(0)","").strip()
        tel = re.search(pattern_phone, addresse_tel).group()
        rep["tel"] = tel
    except:
        rep["tel"] = "NA"
    try:
        addresse_site = soup.find("div", attrs={"class":u"col-xs-11 col-sm-11 col-md-10"}).text.replace("\n", " ").replace("\t", " ").strip()
        site = re.search(pattern_site, addresse_site).group()
        rep["site"] = site
    except:
        rep["site"] = "NA"
    try:
        rep["adresse"] = addresse_tel.replace(tel,"").replace(site,"").strip()
    except:
        rep["adresse"] = "NA"
    try:
        rep["email"] = soup.findAll("p", attrs={"class":u"tel"})[1].text.strip()
    except:
        rep["email"] = "NA"
    try:
        tags =  soup.find("div", attrs={"class":u"padL15"}).findAll("div","margT10")
        activite = [re.sub("\s+"," ", tag.text.strip().replace("\n\n"," : ") ) for tag in tags]
        rep["typeA"] = activite
    except:
        rep["typeA"] = "NA"
    try:
        boards = soup.find("div",attrs={"class":"col-xs-12 responsables"}).text.strip().split("\n")
        rep["board"] = boards
    except:
        rep["board"] = "NA"
    try:
        rep["description"] = soup.find('div', attrs={"style":u"padding:15px"}).text.strip()
    except:
        rep["description"] = "NA"
    try:
        emplacement = soup.find('div', attrs={"class":u"colorS margT5 entree"}).span.text.strip()
        rep["emplacement"] = emplacement
    except:
        rep["emplacement"] = "NA"
    try:
        rep["presence"] = soup.find('div', attrs={"class":u"colorS margT5 entree"}).text.replace(emplacement,"").strip()
    except:
        rep["presence"] = "NA"
    try:
        rep["salon"] = 'bourget_2019'
    except:
        rep["salon"] = 'bourget_2019'

    return(rep)

csv_df = pd.DataFrame(columns=fieldnames)



url_base2 = "https://publications.siae.fr/publication.php?lang=fr"
WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
browser = webdriver.Chrome(WEBDRIVER)
browser.get(url_base2)
time.sleep(3)

i = 1
j=0

while True:

    html = browser.page_source
    soup = BeautifulSoup(html)
    #time.sleep(1)

    fiches = soup.findAll("div", attrs={"data-test":u"2"})
    print("on va scrappé la page " , j)
    print(i)
    #time.sleep(0.5)


    for f in fiches:
        fin_url = f.find("a", attrs={"title":u"Voir la fiche"}).get("href")
        url_fiche = "https://publications.siae.fr/"+ fin_url
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)

        csv_df = csv_df.append(fiche, ignore_index=True)


    print("on vient de scrappé " , j)
    print(i, " et on va l'augmenté")

    if i<4 :
        j+=1
        i+=2
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif i == 5 :
        i+=4
        j+=1
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif j == 7:
        i+=2
        j+=1
        time.sleep(1)
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif j == 8:
        i-=2
        j+=1
        time.sleep(1)
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif j == 159 :
        i-=2
        j+=1
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif 158 < j < 166 :
        i+=2
        j+=1
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif i == 15 :
        i+=0
        j+=1
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()

    elif i < 17:
        i+=2
        j+=1
        browser.find_element_by_xpath("""//*[@id="pagination"]/span["""+ str(i) + """]""").click()


    else :
        break


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "


csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "bourget2019")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "bourget2019.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "bourget2019.xlsx")
