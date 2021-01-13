#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:15:48 2019

@author: enzo.ramirez
"""

import re
from bs4 import BeautifulSoup

import pandas as pd
from selenium import webdriver



fieldnames = [u"societe",
                u"slogan",
                u"tags",
                u"typeA",
                u"description",
                u"tel",
                u"fax",
                u"email",
                u"produits",
                u"site",
                u"fb",
                u"adresse",
                u"twitter",
                u"effectif",
                u"productcat",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)


def nettoyage_chaine(chaine):
    chaine = chaine.strip()
    chaine = re.sub('\s+',' ', chaine)
    return chaine


def lecture_exposant(url):
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html)

    rep = {}

    try:
        rep["societe"] = soup.find("header", class_ = "exhibitor-header").h1.text.strip()
    except:
        rep["societe"] = "NA"
    try:
        rep["slogan"] = soup.find("header", class_ = "exhibitor-header").h2.text.strip()
    except:
        rep["slogan"] = "NA"
    try:
        tags = soup.find("dl").dd.text.replace("\n","").replace("\r","").replace(",","").split("-")[1:]
        tags_list = [tag.strip() for tag in tags]
        rep["tags"] = tags_list
        if rep["tags"] == "[]" :
            rep["tags"] = "NA"
        else:
            pass
    except:
        rep["tags"] = "NA"
    try:
        rep["description"] = soup.find('div', class_="profile-description").text.replace("\n"," ").strip()
    except:
        rep["description"] = "NA"
    try:
        rep["typeA"] = soup.find('dl', class_="icon icon-hersteller exhibitor-fact").dt.text.strip()
    except:
        rep["typeA"] = "NA"
    try:
        products = soup.find("div", class_="products-wrapper").findAll("div", class_ = "products-content")
        products_list = [product.h3.text.strip() for product in products]
        rep["produits"] = products_list
        if rep["produits"] == """[""]""" :
            rep["produits"] = "NA"
        else:
            pass
    except:
        rep["produits"] = "NA"
    try:
        rep["adresse"] = soup.find("p", class_="f-default contact-info").text.strip().replace("\n"," ")  #+ " - " nettoyage_chaine(soup.find("div", class_="contact").text.replace("\n"," - ").replace("\r"," - "))split("\n")[4].replace("\n","").replace("\xa0","").p.text.strip()
    except:
        rep["adresse"] = "NA"
    try:
        rep["email"] = soup.find("section", class_="M03704").find("div", class_ = "rowInner").find("p", class_ = "f-default contact-info").text.replace("\n"," ").strip()
    except:
        rep["email"] = "NA"
    try:
        rep["tel"] = soup.find("span", itemprop="phone").a.text.strip()
    except:
        rep["tel"] = "NA"
    try:
        rep["fax"] = soup.find("span", itemprop="fax").text.split(":")[1].strip()
    except:
        rep["fax"] = "NA"
    try:
        rep["site"] = soup.find("span", itemprop="phone").parent.find("a",itemprop="url").get("href").strip()
    except:
        rep["site"] = "NA"
    try:
        rep["fb"] = soup.find("section", "M069 social-media-links").findAll("a")[0].get("href").strip()
    except:
        rep["fb"] = "NA"
    try:
        rep["twitter"] = soup.find("section", "M069 social-media-links").findAll("a")[1].get("href").strip()
    except:
        rep["twitter"] = "NA"
    try:
        rep["effectif"] = soup.find('dl', class_="icon icon-vcard exhibitor-fact").dt.text.strip()
    except:
        rep["effectif"] = "NA"
    try:
        tproducts = soup.find("div", "swiper-wrapper").findAll('ul', class_="product-groups")
        tproducts_list = [tproduct.li.text.replace("\n","").strip() for tproduct in tproducts]
        rep["productcat"] = tproducts_list
        if rep["productcat"] == """[""]""" :
            rep["productcat"] = "NA"
        else:
            pass
    except:
        rep["productcat"] = "NA"

    return(rep)



WEBDRIVER = '/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver'
browser = webdriver.Chrome(WEBDRIVER)
browser.get("https://www.hannovermesse.de/en/exhibition/exhibitors-products/exhibitor-index/")

i = 1
j=2
while True:
    html = browser.page_source
    soup = BeautifulSoup(html)
    fiches = soup.find("section", "M109 M10902 M1090204").findAll("a", "overview-link")
    for f in fiches:
            url_fiche = "https://www.hannovermesse.de" + f.get("href")
            print( "fiche: {}".format(url_fiche))
            fiche = lecture_exposant(url_fiche)

            csv_df = csv_df.append(fiche, ignore_index=True)
            #time.sleep(0.1)

#################

    try:
            browser.get("https://www.hannovermesse.de/en/exhibition/exhibitors-products/exhibitor-index/")
            browser.find_element_by_xpath('//*[@id="j_idt100:j_idt104"]/section[2]/div/div/div/ul/li[' + str(j) + ']/a').click()
            #time.sleep(0.1)
            j+=1
    except:
            print("Last Page!")
            break

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "hannover_p2")

#csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "hannover.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "hannover.xlsx")


browser.close()
