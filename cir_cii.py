#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:40:53 2019

@author: enzo.ramirez
"""

import pandas as pd

PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
PATH_FOLDER_CSV_CLEAN = "/Users/enzo.ramirez/sharedocker/csv_clean/"

#PATH_FOLDER_CSV_SCRAP + "
#PATH_FOLDER_CSV_CLEAN + "


cir = pd.read_csv(PATH_FOLDER_CSV_SCRAP + "cir_cii.csv", engine = 'python' , encoding = 'utf-8' , delimiter = ";")


cir = cir.drop(["Année d'agrément", "Début d'agrément", "Fin d'agrément", "Lien vers la fiche scanR" ,
                  "Unité urbaine", "Commune", "Académie" ,  "Pays", "Code de la région (France)", "Téléphone",
                  "Code de l'académie (France)",  "Département","Code de l'unité urbaine (France)",
                  "Sigle", "Localisation", "Ville","Code commune (France)", "Code du département (France)", "Code postal"], axis=1)


cir.rename(columns={"Numéro SIREN": "siren",
                     "Nom de l'entreprise": "societe",
                     "Base SIRENE : Catégorie de l'établissement siège": "college",
                     "Région": "Occitanie",
                     "Géolocalisation": "geoloc",
                     "Type de structure": "typesociete",
                     "Dispositif": "dispositif",
                     "Base SIRENE : Activité principale exercée (APE) par l'établissement siège": "typeA",
                     "Base SIRENE : Code APE de l'établissement siège": "ape",
                     "Activité" : "domaineA"
                     }, inplace=True)
cir.columns
cir['cluster']= 'circii'
cir['Occitanie']= 'true'
cir.to_csv(PATH_FOLDER_CSV_CLEAN + "cir_cii_final.csv", sep='\t', encoding='utf-8')
cir.to_pickle(PATH_FOLDER_CSV_CLEAN + "cir_cii_final")

