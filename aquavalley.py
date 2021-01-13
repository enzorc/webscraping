#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:11:49 2019

@author: enzo.ramirez
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:29:58 2019

@author: enzo.ramirez

SCRAPING AQUA VALLEY

"""
# packages need are imported
import re
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


fieldnames = [u"societe",
                u"adresse",
                u"email",
                u"tel",
                u"typeA",
                u"site",
                u"description",
                u"typesociete",
                u"cluster",
                u'CP',
                u'Occitanie',
                u'num_dep',
                u'geoloc']


csv_df = pd.DataFrame(columns=fieldnames)



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
#1 This function will takes the url of the page we want to scrap
#2 then it will read it and use beautifulsoup to parse it (in order to read and get element)
#3 therefore it will create a dictionnary
#  After, by using try-except block for each field, it stores the data of each field for a company in the dictionnary
#  The try-except block specify in the try where we get the information ( which div and which class) if it can't find the html source code for this information the except return a "NA"
#  In the case of multiple elements for a field that we don't want to store as a unique value (key word for example)
    ## we specify in try except block that we create a json list containing separately each element
#  Finally the function return our dictionnary
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})    #1
    html = urllib.request.urlopen(req).read()   #2
    soup = BeautifulSoup(html)  #2
    print (soup.title.text)

    rep = {}    #3
    try:
        rep["societe"] = soup.find("div", attrs={"id":u"main_col"}).h1.text # find get the only (firstNA) element for tag div and class top-area-container it finds, then get the text in the h2 text as we are interested in it
    except:
        rep["societe"] = "NA"
    try:
        rep["adresse"] = soup.find("p", attrs={"class":u"address"}).text.strip().replace("\n", " ")
    except:
        rep["adresse"] = "NA"
# =============================================================================
#     try:
#         location = geolocator.geocode( soup.find("p", attrs={"class":u"address"}).text.strip().replace("\n", " ") )
#         rep["adresseN"] = location.address
#         rep["geoloc"] = str(location.latitude) + ',' + str(location.longitude)
#     except:
#         rep["adresseN"] = "NA"
#         rep["geoloc"] = "NA"
# =============================================================================
    try:
        rep["email"] = soup.findAll("p", attrs={"class":u"tel"})[1].text.strip()
    except:
        rep["email"] = "NA"
    try:
        rep["tel"] = soup.findAll("p", attrs={"class":u"tel"})[0].text.split(":")[1].strip()
    except:
        rep["tel"] = "NA"
    try:
        tags = soup.find("ul", attrs={"class":u"col"}).findAll("li")[-1].findAll("strong")
        tags_list = ((' '.join([tag.text for tag in tags])).replace(",","")).split(" ")
        #tag_dict = list_dict(tags_list)
        rep["typeA"] = tags_list
    except:
        rep["typeA"] = "NA"
    try:
        rep["site"] = soup.find("p",attrs={"class":"link"}).a.get("href")
    except:
        rep["site"] = "NA"
    try:
        rep["description"] = soup.find('p', attrs={"id":u"synopsis"}).text.strip()
    except:
        rep["description"] = "NA"
    try:
        rep["typesociete"] = soup.find('li', attrs={"class":u"colleges"}).strong.text
    except:
        rep["typesociete"] = "NA"
    try:
        rep["cluster"] = 'aquavalley'
    except:
        rep["cluster"] = 'aquavalley'

    return(rep)

# url_base define the website from where we start
# in other words from where we can get access to all of the "subwebsites"/"subpages"
# my words might not be the exact terminology of what it means but i think you can get the idea
url_base = "http://www.pole-eau.com/Les-Services/Annuaire-des-membres/(list)/list"
#i = 1
while True:
# As long as true we get the url of the website we open it and read it then we parse it with BeautifulSoup
    req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
# fiches variable description
# We use the method find to get the tag (here <div) and the class (here class = "listing-holder") where we will have all the informations on companies and to access "subpages"
# Then we use findall method on it to get all the specific block for each company, here the tag used is "<a" and the class is "listing-item" ( the tag "a" and the class"listing-item" are specific block/container for each company)
# To sum up, in fiches we will find the html code specific for each company ( it's specific block of information has been selected thanks to find find all method)
    #fiches = soup.findAll("a", attrs={"class":"in-flex"})
    fiches = soup.find("div", attrs={"id":u"members_list"}).findAll("h2")
# here is the loop which uses the fiches created just before
# This loop is going to go through all blocks we got from fiches and from each block get (exctract) the href (which means the link of the "subpage" specific to each company)
    for f in fiches:
        url_fiche = "http://www.pole-eau.com"+ f.a.get("href")
        print( "fiche: {}".format(url_fiche))
        fiche = lecture_exposant(url_fiche)
        #fiche["id_societe"] = "soc_%d" % i
        #i += 1
        csv_df = csv_df.append(fiche, ignore_index=True)
        #time.sleep(10)
    try:
        url_ext = soup.find("a", {"class":"next"}).get("href")
        url_base = "http://www.pole-eau.com"+url_ext
        print("page: {}".format(url_base))
    except:
        break


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "aqua_valley")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "aqua_valley.csv", sep='\t', encoding='utf-8')
#csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "aqua_valley.xlsx")
