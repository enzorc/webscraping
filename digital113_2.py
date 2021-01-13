import fitz, copy , re
import pandas as pd
doc = fitz.open("/Users/enzo.ramirez/Documents/adocc/scrap/Z_onlyscrap/pdf/digital113.pdf")

pattern_mail = r"([a-zA-Z0-9_\-\.]+)@(\s)*([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
pattern_phone = r"(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})"
pattern_name =r"^\s*([a-zA-Z0-9]+)\s([a-zA-Z0-9]+){2}"
# x0, y0, x1, y1
## The first two numbers are regarded as the “top left” corner x0,y0 and x1,y1 as the “bottom right” one.



fieldnames = [u"societe",
              u"site",
              u"description",
              u"email",
              u"board",
              u"typeA",
              u"tel",
              u'CP',
              u'Occitanie',
              u'num_dep',
              u'geoloc']

csv_df = pd.DataFrame(columns=fieldnames)


rect1 = {
    "societe" : fitz.Rect(260.0, 0.0, 415.0, 98.0),
    "description_fr" : fitz.Rect(0.0, 0.0, 253.0, 296.0),
    "typeA": fitz.Rect(260.0, 90.0, 415.0, 152.0),
    "infos" : fitz.Rect(260.0, 152.0, 415.0, 296.0)
}
rect2 = {
    "societe" : fitz.Rect(680.0, 0.0, 836.0, 98.0),
    "description_fr" : fitz.Rect(420.0, 0.0, 674.0, 296.0),
    "typeA": fitz.Rect(680.0, 90.0, 836.0, 152.0),
    "infos" : fitz.Rect(680.0, 152.0, 836.0, 296.0)
}
rect3 = {
    "societe" : fitz.Rect(260.0, 298.0, 415.0, 396.0),
    "description_fr" : fitz.Rect(0, 298.0, 253.0, 572.0),
    "typeA": fitz.Rect(260.0, 389.0, 415.0, 450),
    "infos" : fitz.Rect(260.0, 450, 415.0, 594.0)
}
rect4 = {
    "societe" : fitz.Rect(680.0, 413.0, 836.0, 396.0),
    "description_fr" : fitz.Rect(583.0, 413.0, 674.0, 572.0),
    "typeA": fitz.Rect(680.0, 389.0, 836.0, 450),
    "infos" : fitz.Rect(680.0, 450, 836.0, 594.0)
}
rects = [rect1,rect2,rect3,rect4]

def traverse(x, tree_types=(list, tuple)):
    if isinstance(x, tree_types):
        for value in x:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield x

#liste = list(traverse(lines))

def lecture_fiche(numero_page, rect_soc , rect_des , rect_typ , rect_inf):



    # on charge le document et la page
    page=doc.loadPage(numero_page)
    dico = page.getText("dict")



    lines = []
    for block in dico["blocks"]:
        if block["type"] == 0:
            lines.append(block["lines"])


# =============================================================================
#     for i in range(len(rects)):
#         for section,rect in rects[i].items():
#             if section == "societe" :
#                 rect_soc = copy.deepcopy(rect)
#
#             elif section == "description_fr" :
#                 rect_des = copy.deepcopy(rect)
#
#             elif section == "typeA" :
#                 rect_typ = copy.deepcopy(rect)
#
#             elif section == "infos" :
#                 rect_inf = copy.deepcopy(rect)
# =============================================================================
            societe =[]
            description =[]
            contact =[]
            typeA =[]

            for line in lines:
                for word in line:

                                #validée
                                # societe
                            if fitz.Rect(word["bbox"]) in rect_soc:
                                societe.append(word['spans'][0]['text'])
                                print(word['spans'][0]['text'])
                                # validée
                                # description
                            elif fitz.Rect(word["bbox"]) in rect_des:
                                description.append(word['spans'][0]['text'])

                                # validée
                                # typeA
                            elif fitz.Rect(word["bbox"]) in rect_typ:
                                typeA.append(word['spans'][0]['text'])

                                # contacts
                            elif fitz.Rect(word["bbox"]) in rect_inf:
                                contact.append(word['spans'][0]['text'])

            contacts = (" ".join(contact)).replace("Contacts","").strip()
            row = {}
            try:
                row['societe'] = societe[0].replace("Secteur d’activité","").strip()
            except:
                row['societe'] = "NA"

            try:
                row['site'] = societe[1].strip()
            except:
                row['site'] = "NA"

            try:
                row['description'] = (" ".join(description)).strip()
            except:
                row['description'] = "NA"

            try:
                row['typeA'] = (" ".join(typeA)).replace("Secteur d’activité","").strip()
            except:
                row['typeA'] = societe[0]

            try:
                tel = re.search(pattern_phone, contacts).group()
                row['tel'] = tel
            except:
                row['tel'] = "NA"

            try:
                mail = (re.search(pattern_mail, contacts).group())
                row['email'] = mail.replace("@ ","@")
            except:
                row['email'] = "NA"

            try:
                name = contacts.replace(mail,"").replace(tel,"")
                row['board'] = re.search(pattern_name, name).group()
            except:
                row['board'] = "NA"

            #inv_writer.writerow(row)

    return row



def lecture_page(numero_page):
    global csv_df
    j=0
    for section,rect in rects[j].items():
            if section == "societe" :
                rect_soc = copy.deepcopy(rect)

            elif section == "description_fr" :
                rect_des = copy.deepcopy(rect)

            elif section == "typeA" :
                rect_typ = copy.deepcopy(rect)

            elif section == "infos" :
                rect_inf = copy.deepcopy(rect)

    row = lecture_fiche(numero_page, rect_soc , rect_des , rect_typ , rect_inf)
    csv_df = csv_df.append(row, ignore_index=True)

    j+=1
    for section,rect in rects[j].items():
            if section == "societe" :
                rect_soc = copy.deepcopy(rect)

            elif section == "description_fr" :
                rect_des = copy.deepcopy(rect)

            elif section == "typeA" :
                rect_typ = copy.deepcopy(rect)

            elif section == "infos" :
                rect_inf = copy.deepcopy(rect)

    row = lecture_fiche(numero_page, rect_soc , rect_des , rect_typ , rect_inf)
    csv_df = csv_df.append(row, ignore_index=True)

    j+=1
    for section,rect in rects[j].items():
            if section == "societe" :
                rect_soc = copy.deepcopy(rect)

            elif section == "description_fr" :
                rect_des = copy.deepcopy(rect)

            elif section == "typeA" :
                rect_typ = copy.deepcopy(rect)

            elif section == "infos" :
                rect_inf = copy.deepcopy(rect)

    row = lecture_fiche(numero_page, rect_soc , rect_des , rect_typ , rect_inf)
    csv_df = csv_df.append(row, ignore_index=True)

    j+=1
    for section,rect in rects[j].items():
            if section == "societe" :
                rect_soc = copy.deepcopy(rect)

            elif section == "description_fr" :
                rect_des = copy.deepcopy(rect)

            elif section == "typeA" :
                rect_typ = copy.deepcopy(rect)

            elif section == "infos" :
                rect_inf = copy.deepcopy(rect)

    row = lecture_fiche(numero_page, rect_soc , rect_des , rect_typ , rect_inf)
    csv_df = csv_df.append(row, ignore_index=True)

    return csv_df
##########




for i in range(5,78):
    lecture_page(i)

csv_df = csv_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" "," "], regex=True)

csv_df = csv_df.drop_duplicates()
csv_df   = csv_df[csv_df.societe != 'Secteur d’activité']
csv_df   = csv_df[csv_df.societe != '']
csv_df   = csv_df[csv_df.societe != 'NA']

csv_df['cluster']= "digital113"


PATH_FOLDER_CSV_SCRAP = "/Users/enzo.ramirez/sharedocker/csv_scrap/"
#PATH_FOLDER_CSV_SCRAP + "

csv_df = csv_df[pd.notnull(csv_df['societe'])]
csv_df.to_pickle(PATH_FOLDER_CSV_SCRAP + "digital113")

csv_df.to_csv(PATH_FOLDER_CSV_SCRAP + "digital113.csv", sep='\t', encoding='utf-8')
csv_df.to_excel(PATH_FOLDER_CSV_SCRAP + "digital113.xlsx")
