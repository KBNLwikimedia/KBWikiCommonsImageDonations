# coding=utf-8
# Script to create categories related to the prentenboeken on Wikimedia Commons, to be more precise:

#1: Create Homecat: the cat in which the individual images go, one Homecat per book.

#2: Also create Book template in this cat - # see e.g. https://commons.wikimedia.org/wiki/Category:De_Nieuwe_Rijschool

#3: Add Glamorous reuse stats link for Homecat

#4: Create parentcats, in which the Homecat goes. The default is Category:Picture books from Koninklijke Bibliotheek.
#In addition, there can be 0,1,2,.. or more extra parentcats per book

import os, os.path
import json
import requests

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

current_dir = os.path.dirname(os.path.realpath(__file__))
inputdirname = "input"
#outputdirname = "output"
inputdir = os.path.join(current_dir, inputdirname)
os.chdir(inputdir)

jsonfile="SRUdump_GvN_PRB01_27012017_forGWToolset.json"
with open(jsonfile,encoding="utf-8") as data_file:
    data = json.load(data_file)

ppn_catsfile = "PPN_Categories_definitief.json"
#ppn_catsfile = "PPN_Categories_definitief.json"
with open(ppn_catsfile,encoding="utf-8") as catsfile:
    catsdata = json.load(catsfile)

#Open inputfile containing number of pages for each book
ppn_npagesfile="PPN_NoOfPages_definitief.json"
with open(ppn_npagesfile,encoding="utf-8") as npagesfile:
    pagesdata = json.load(npagesfile)

#Open inputfile containing GWT file base titles for each book
ppn_gwtbasetitlefile="PPN_GWTBaseTitle_definitief.json"
with open(ppn_gwtbasetitlefile,encoding="utf-8") as gwtbasetitlefile:
    gwtbasetitledata = json.load(gwtbasetitlefile)

#Login to the MediaWiki API to write categories to Commons - Code from https://www.mediawiki.org/wiki/API:Edit/Editing_with_Python

username = 'OlafJanssen'
password = 'WACHTWOORD'
baseurl = 'https://commons.wikimedia.org/w/'
#baseurl = 'https://test.wikipedia.org/w/'

# Login request
payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
r1 = requests.post(baseurl + 'api.php', data=payload)

# login confirm
login_token = r1.json()['query']['tokens']['logintoken']
payload = {'action': 'login', 'format': 'json', 'utf8': '', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token}
r2 = requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

# get edit token2
params3 = '?format=json&action=query&meta=tokens&continue='
r3 = requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
edit_token = r3.json()['query']['tokens']['csrftoken']

edit_cookie = r2.cookies.copy()
edit_cookie.update(r3.cookies)

#for loop over alle 600+ boeken (ook niet PD)
pd_counter = 0

for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    title=""
    summary=""
    glamorous=""
    message=""

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:recordIdentifier")  # PRB01:175094691
    #print("ppn_long: "+ ppn_long)
    ppn = ppn_long.split(":")[1]  # 175094691 #length is always 9 chars
    if ppn in catsdata.keys():
        pd_counter += 1
        commonsHomeCat=catsdata[ppn]["HomeCat"] # See http://stackoverflow.com/questions/17322668/typeerror-dict-keys-object-does-not-support   -indexing

        commonsHomeCat_trunc = commonsHomeCat.split(":")[1] #take the part after 'Category:'
        sorter=""
        if commonsHomeCat_trunc.startswith("De "): #Starting with "De "
            sorter = commonsHomeCat_trunc[3:]
        if commonsHomeCat_trunc.startswith("Het "):#Starting with "Het "
            sorter = commonsHomeCat_trunc[4:]
        if commonsHomeCat_trunc.startswith("Een "):#Starting with "Een "
            sorter = commonsHomeCat_trunc[4:]
        #print(sorter)

        # Write parent categories ==
        ## Default parent cats
        parentcats = ""
        if sorter != "":
            parentcats += '[[Category:Picture books from Koninklijke Bibliotheek|' + sorter + ']]\n'
        else:
            parentcats += '[[Category:Picture books from Koninklijke Bibliotheek]]\n'

        ## Optional parent cats
        if "SubjectCats" in catsdata[ppn]:
            commonsSubjectCat = catsdata[ppn]["SubjectCats"]
            if sorter != "":
                parentcats += '[[' + commonsSubjectCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsSubjectCat + ']]\n'

        if "AnnotationCats" in catsdata[ppn]:
            commonsAnnotationCat = catsdata[ppn]["AnnotationCats"]
            if sorter != "":
                parentcats += '[[' + commonsAnnotationCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsAnnotationCat + ']]\n'

        if "AuteurCats" in catsdata[ppn]:
            commonsAuteurCat = catsdata[ppn]["AuteurCats"]
            if sorter != "":
                parentcats += '[[' + commonsAuteurCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsAuteurCat + ']]\n'

        if "UitgeverCats" in catsdata[ppn]:
            commonsUitgeverCat = catsdata[ppn]["UitgeverCats"]
            if sorter != "":
                parentcats += '[[' + commonsUitgeverCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsUitgeverCat + ']]\n'

        if "DescriptionCats" in catsdata[ppn]:
            commonsDescriptionCat = catsdata[ppn]["DescriptionCats"]
            if sorter != "":
                parentcats += '[[' + commonsDescriptionCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsDescriptionCat + ']]\n'

        if "AlternativeCats" in catsdata[ppn]:
            commonsAlternativeCat = catsdata[ppn]["AlternativeCats"]
            if sorter != "":
                parentcats += '[[' + commonsAlternativeCat + '|' + sorter + ']]\n'
            else:
                parentcats += '[[' + commonsAlternativeCat + ']]\n'

        #Write Glamorous page stats ==
        glamorous = "[http://tools.wmflabs.org/glamtools/glamorous.php?doit=1&category=" + commonsHomeCat.split(":")[1].replace(" ","+") + "&use_globalusage=1&ns0=1&show_details=1&projectss&#91;wikipedia&#93;=1 Image uptake stats]\n\n"

        # ======================================================
        # Create Book template in every Homecat # See e.g. https://commons.wikimedia.org/wiki/Category:De_Nieuwe_Rijschool

        BookTemplate = ""
        BookTemplate += "{{Book\n"
        BookTemplate += " |Accession number = Description of the book in the Dutch library catalogue: http://www.bibliotheek.nl/catalogus/titel." + str(ppn) + ".html\n"
        BookTemplate += " |Source = Digitized book on [http://resolver.kb.nl/resolve?urn=urn:gvn:" + str(ppn_long) + " Geheugen van Nederland / Memory of the Netherlands] website" + "\n"

        BookTemplate += " |Language = Dutch\n"
        BookTemplate += " |Pageoverview = "
        gwtbasetitle = finditem(gwtbasetitledata, ppn)
        npages = finditem(pagesdata, ppn)
        for i in range(int(npages)):
            BookTemplate += "[[:File:" + str(gwtbasetitle) + " - PPN " + str(ppn) + " - Image " + str(i + 1) + ".jpeg|" + str(i + 1) + "]]"
            if i == int(npages) - 1:  # if it's the last pagenumber, don't print the divider "--"
                BookTemplate += ""
            else:
                BookTemplate += " -- "
        BookTemplate += "\n"
        BookTemplate += " |Image = " + str(gwtbasetitle) + " - PPN " + str(ppn) + " - Image 1.jpeg\n"

        fulltitle = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:title")
        if fulltitle:
            BookTemplate += " |Title = "+ str(fulltitle) + "\n"

        date = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:created")
        if date:
            BookTemplate += " |Date = "+ str(date) + "\n"

        objectholder = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:recordRights") #in welke collectie/instelling bevindt het boek zich?
        if objectholder == "Koninklijke Bibliotheek":
            references = "This book was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) book is also in the collection of the [[:w:en:National_Library_of_the_Netherlands|National library of the Netherlands]]"
        elif objectholder == "Gemeentebibliotheek, Rotterdam":
            references = "This book was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) book is in the collection of the {{Institution:Bibliotheek Rotterdam}}"
        elif objectholder == "Openbare bibliotheek, Amsterdam":
            references = "This book was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) book is in the collection of the {{Institution:Openbare Bibliotheek Amsterdam - Centrale bibliotheek}}"
        elif objectholder == "Athenaeumbibliotheek, Deventer":
            references = "This book was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) book is in the collection of the {{Institution:Stadsarchief en Athenaeumbibliotheek}}"
        else:
            references = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            institution = "uyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
        BookTemplate += " |References = "+ str(references) +  "\n"

        booksize = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcterms:extent")
        if booksize:
            BookTemplate += " |Other_fields = {{Information field|name=Book dimensions|value=" + str(booksize)+ "}}\n"


        descriptionlist = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:description")
        descriptionstring = ""
        if str(descriptionlist) != "None":
            if isinstance(descriptionlist, str):
                descriptionstring = str(descriptionlist)
            else:
                descriptionstring = ' // '.join(map(str, descriptionlist))

        taglist = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:subject")
        tagstring = ""
        # #taglist can either be a string or a list[] of strings
        # #http://www.decalage.info/en/python/print_list
        if str(taglist) != "None":
            if isinstance(taglist, str):  # taglist is een string
                tagstring = str(taglist)
            else:  # taglist is een list[] of strings
                tagstring = ' // '.join(map(str, taglist))

        alternativelist = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcterms:alternative")
        alternativestring = ""
        if str(alternativelist) != "None":
            if isinstance(alternativelist, str):
                alternativestring = str(alternativelist)
            else:
                alternativestring = ' // '.join(map(str, alternativelist))

        annotationlist = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcx:annotation")
        annotationstring = ""
        if str(annotationlist) != "None":
            if isinstance(annotationlist, str):
                annotationstring = str(annotationlist)
            else:
                annotationstring = ' // '.join(map(str, annotationlist))

        BookTemplate += " |Description = "
        if descriptionstring:
            BookTemplate += "* " + str(descriptionstring) + "\n"
        if alternativestring:
            BookTemplate += "* " + str(alternativestring) + "\n"
        if annotationstring:
            BookTemplate +="* " + str(annotationstring) + "\n"
        if tagstring:
            BookTemplate += "* " + str(tagstring) + "\n"

        contributorlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:contributor")
        #contributor can be: (authors), (placeofprint:printer), (placesofpublication:publisher)
        uitgeverlist=[]
        uitgevernaamlist=[]
        uitgeverplaatslist=[]
        uitgevernaam=""
        uitgeverplaats=""

        drukkerlist=[]
        drukkernaamlist=[]
        drukkerplaatslist=[]
        drukkernaam=""
        drukkerplaats=""

        auteurlist=[]
        auteursnamenlist=[]
        auteurstring=""

        if str(contributorlist) != "None":
            if isinstance(contributorlist, dict): # contributorlist = dict
                if contributorlist['dcx:role'] == "uitgever":
                    #switch around lastname and firstname of drukker, uitgever, author - see http://stackoverflow.com/questions/15704943/switch-lastname-firstname-to-firstname-lastname-inside-list
                    #uitgeverstring=" / ".join(contributorlist['content'].split(": ")[::-1])
                    uitgevernaam = contributorlist['content'].split(": ")[1]
                    uitgeverplaats = contributorlist['content'].split(": ")[0]
                elif contributorlist['dcx:role'] == "drukker":
                    drukkernaam = contributorlist['content'].split(": ")[1]
                    drukkerplaats = contributorlist['content'].split(": ")[0]
                elif contributorlist['dcx:role'] == "auteur":
                    auteurstring=" ".join(contributorlist['content'].split(", ")[::-1])
                else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")
            else: # contributorlist = list of dicts
                for dic in contributorlist:
                    if dic['dcx:role'] == "uitgever": #a book can have multiple publishers, printers, authors
                        uitgeverlist.append(dic['content'])
                        uitgevernaamlist=[uitgever.split(": ")[1] for uitgever in uitgeverlist]
                        uitgeverplaatslist=[uitgever.split(": ")[0] for uitgever in uitgeverlist]
                    elif dic['dcx:role'] == "drukker":
                        drukkerlist.append(dic['content'])
                        drukkernaamlist=[drukker.split(": ")[1] for drukker in drukkerlist]
                        drukkerplaatslist=[drukker.split(": ")[0] for drukker in drukkerlist]
                    elif dic['dcx:role'] == "auteur":
                        auteurlist.append(dic['content'])
                        auteursnamenlist=[" ".join(auteur.split(", ")[::-1]) for auteur in auteurlist]
                    else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")

                uitgevernaam=' // '.join(map(str, uitgevernaamlist))
                uitgeverplaats=' // '.join(map(str, uitgeverplaatslist))
                drukkernaam=' // '.join(map(str, drukkernaamlist))
                drukkerplaats=' // '.join(map(str, drukkerplaatslist))
                auteurstring=' // '.join(map(str, auteursnamenlist))

                if auteurstring:
                    BookTemplate += " |Author = " + str(auteurstring) + "\n"
                if drukkerplaats:
                    BookTemplate += " |Printer = " + str(drukkernaam)+" in "+str(drukkerplaats) + "\n"
                elif drukkernaam:
                    BookTemplate += " |Printer = " + str(drukkernaam) + "\n"
                if uitgevernaam:
                    BookTemplate += " |Publisher = " + str(uitgevernaam) + "\n"
                if uitgeverplaats:
                    BookTemplate += " |City = " + str(uitgeverplaats) + "\n"
        BookTemplate += "}}\n\n"


    #================================================================
    # Write final strings to API

        # 1-- Title van de Homecat
        title = str(commonsHomeCat) #eg. Category:Moeder Hubbard en haar hond
        # 2--Wat er in de bewerkingsaamenvatting zou komen
        summary = 'Creating ' + commonsHomeCat
        # 3-- Tekstuele inhoud van de Homecat
        message += BookTemplate + glamorous + parentcats

        #print('PDCounter: ' + str(pd_counter))
        #print('PPN: '+ ppn)
        print('Homecat: ' + title)
        print('Summary: ' + summary)
        print("Message: " + message)
        print("=======================================")

        #Schrijf naar de Commons-API
        payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'appendtext': message,'summary': summary, 'title': title, 'token': edit_token}
        r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
        print (r4.text)

print("Number of PD books: "+str(pd_counter))
data_file.close()
catsfile.close()
npagesfile.close()
gwtbasetitlefile.close()