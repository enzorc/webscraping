#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:30:19 2019

@author: enzo.ramirez
"""

PATH_FOLDER_GROUPED = "/Users/enzo.ramirez/sharedocker/"
PATH_FOLDER_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
PATH_WEBDRIVER = "/Users/enzo.ramirez/Documents/adocc/selenium/chromedriver"


import re
from bs4 import BeautifulSoup

import pandas as pd
from selenium import webdriver


def nettoyage_chaine(chaine):
    chaine = chaine.strip()
    chaine = re.sub('\s+',' ', chaine)
    return chaine


def recup_info(societe):
    #html = browser.page_source
    #soup = BeautifulSoup(html)

    rep = {}

    try:
        rep["societe"] = societe
    except:
        pass

    try:
        catjur = browser.find_element_by_xpath('//*[@id="collapse-0"]/div/div[2]/p[2]').text.replace("Catégorie juridique :","").strip()
        catjurl= catjur.split("-")
        rep["code_categorie_juridique"] = catjurl[0].strip()
        rep["categorie_juridique"] = catjurl[1].strip()
    except:
        pass

    try:
        ape = browser.find_element_by_xpath('//*[@id="collapse-0"]/div/div[2]/p[7]').text.replace("Activité principale exercée :","").strip()
        apel= ape.split("-")
        rep["codeape"] = apel[0].strip()
        rep["ape"] = apel[1].strip()
    except:
        pass

    try:
        rep["siret"] = browser.find_element_by_xpath('//*[@id="collapse-0"]/div/div[2]/p[6]').text.replace("Siret du siège :","").strip()
    except:
        pass

    try:
        catent = browser.find_element_by_xpath('//*[@id="collapse-0"]/div/div[2]/p[10]').text.replace("Catégorie d’entreprise :","").strip()
        catentl = catent.split("-")
        rep["acronyme_categorie_entreprise"] = catentl[0].strip()
        rep["categorie_entreprise"] = catentl[1].strip()
    except:
        pass

    try:
        rep["CP_conf"] = browser.find_element_by_xpath('//*[@id="page1"]/div/div[1]/a/span[2]/p[2]').text
    except:
        pass


    return(rep)



WEBDRIVER = PATH_WEBDRIVER
browser = webdriver.Chrome(WEBDRIVER)

fieldnames = [u"societe",
                u"code_categorie_juridique",
                u"categorie_juridique",
                u"codeape",
                u"ape",
                u"siret",
                u"acronyme_categorie_entreprise",
                u"categorie_entreprise",
                u"CP_conf"]

csv_df = pd.DataFrame(columns=fieldnames)

file_1 = pd.read_json(PATH_FOLDER_GROUPED + "CONCAT_FINAL_grouped.json", orient = 'records')
file_1.loc[0,'societe'] = "100Transitions"

for societe1, CP1, num_dep in zip(file_1.societe, file_1.CP, file_1.num_dep):
    print(societe1,CP1)
    browser.get("https://www.sirene.fr/sirene/public/recherche")

    try:
        browser.find_element_by_xpath('//*[@id="rsQuery"]').send_keys(societe1)
        browser.find_element_by_xpath('//*[@id="communeQuery"]').send_keys(CP1[0])
        browser.find_element_by_xpath('//*[@id="btn-search"]').click()
        browser.find_element_by_xpath('//*[@id="page1"]/div[1]/div[1]/a/span[2]')
    except:
        browser.find_element_by_xpath('//*[@id="rsQuery"]').clear()
        browser.find_element_by_xpath('//*[@id="communeQuery"]').clear()
        try:
            browser.find_element_by_xpath('//*[@id="rsQuery"]').send_keys(societe1)
            browser.find_element_by_xpath('//*[@id="communeQuery"]').send_keys(num_dep[0])
            browser.find_element_by_xpath('//*[@id="btn-search"]').click()
            browser.find_element_by_xpath('//*[@id="page1"]/div[1]/div[1]/a/span[2]')
        except:
            browser.find_element_by_xpath('//*[@id="rsQuery"]').clear()
            browser.find_element_by_xpath('//*[@id="communeQuery"]').clear()
            try:
                browser.find_element_by_xpath('//*[@id="rsQuery"]').send_keys(societe1)
                browser.find_element_by_xpath('//*[@id="btn-search"]').click()
            except:
                pass

    fiche = recup_info(societe1)
    print(societe1)
    csv_df = csv_df.append(fiche, ignore_index=True)

# =============================================================================
#
#
# csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_SCRAP + "moreinfo")
# csv_df.to_csv(PATH_FOLDER_SCRAP + "moreinfo.csv", sep="\t", encoding = 'utf-8')
#
# browser.close()
# =============================================================================
