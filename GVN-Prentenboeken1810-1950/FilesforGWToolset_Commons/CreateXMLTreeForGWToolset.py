#Make an XML tree as input for the GWToolset. One XML-records  = one image/page from a book
# Book template: https://commons.wikimedia.org/wiki/Template:Book

import json
import os.path

#import requests
#from bs4 import BeautifulSoup

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

#==================
current_dir = os.path.dirname(os.path.realpath(__file__))
inputdirname="input"
outputdirname="output"

#Open json inputfile with book-level (not:page-level) metadata
inputdir=os.path.join(current_dir, inputdirname)
os.chdir(inputdir)
#jsonfile="SRUdump_GvN_PRB01_27012017_forGWToolset_testje.json"
jsonfile="SRUdump_GvN_PRB01_27012017_forGWToolset.json"
with open(jsonfile) as data_file:
    data = json.load(data_file)

# Open inputfile containing number of pages for each book
ppn_npagesfile="PPN_NoOfPages_definitief.json"
with open(ppn_npagesfile) as npagesfile:
    pagesdata = json.load(npagesfile)

#Open inputfile containing GWT file base titles for each book
ppn_gwtbasetitlefile="PPN_GWTBaseTitle_definitief.json"
with open(ppn_gwtbasetitlefile) as gwtbasetitlefile:
    gwtbasetitledata = json.load(gwtbasetitlefile)

#Open inputfile containing Home and parent categories for each book
ppn_catsfile="PPN_Categories_definitief.json"
with open(ppn_catsfile) as catsfile:
    catsdata = json.load(catsfile)

#Open target output XML file
outputdir=os.path.join(current_dir, outputdirname)
os.chdir(outputdir)
#outputfile="PrentenboekenXML_GvN_PD_forGWToolset_testje.xml"
outputfile="PrentenboekenXML_GvN_PD_forGWToolset.xml"

#==============

XMLoutputfile = open(outputfile, "w")
XMLoutputfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
XMLoutputfile.write("<records>\n")

pd_counter=0 #Count number of public domain books
recordcounter=0 #count total number of records created

for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):
    #============================================================================

    permission = "{{PD-art|PD-old-70-1923}}"
    language="Dutch"

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcx:recordIdentifier")#PRB01:175094691
    print(ppn_long)
    ppn = ppn_long.split(":")[1]#175094691 #length is always 9 chars

    fulltitle = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:title")
    #title_short = fulltitle.split(" / ")[0]

    gwtbasetitle = finditem(gwtbasetitledata,ppn)

    date = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:created")

    objectholder = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:recordRights") #in welke collectie/instelling bevindt het boek zich?

    if objectholder == "Koninklijke Bibliotheek":
        references = "This image was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) image is also in the collection of the [[:w:en:National_Library_of_the_Netherlands|National library of the Netherlands]]"

    elif objectholder == "Gemeentebibliotheek, Rotterdam":
        references = "This image was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) image is in the collection of the {{Institution:Bibliotheek Rotterdam}}"

    elif objectholder == "Openbare bibliotheek, Amsterdam":
        references = "This image was digitized by the {{Institution:Koninklijke Bibliotheek}}The original (paper) image is in the collection of the {{Institution:Openbare Bibliotheek Amsterdam - Centrale bibliotheek}}"

    elif objectholder == "Athenaeumbibliotheek, Deventer":
        references = "This image was digitized by the {{Institution:Koninklijke Bibliotheek}} The original (paper) image is in the collection of the {{Institution:Stadsarchief en Athenaeumbibliotheek}}"
    else:
        references = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        institution = "uyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

    booksize = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcterms:extent")

    thumbnail=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:thumbnail")
    thumb_url=thumbnail['content']        #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X&role=thumbnail
    thumb_baseurl=thumb_url.split("&")[0] #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X

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

    descriptionlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:description")
    descriptionstring = ""
    if str(descriptionlist) != "None":
        if isinstance(descriptionlist, str):
            descriptionstring=str(descriptionlist)
        else:
            descriptionstring=' // '.join(map(str, descriptionlist))

    taglist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:subject")
    tagstring = ""
    # #taglist can either be a string or a list[] of strings
    # #http://www.decalage.info/en/python/print_list
    if str(taglist) != "None":
        if isinstance(taglist, str): #taglist is een string
            tagstring=str(taglist)
        else: #taglist is een list[] of strings
            tagstring=' // '.join(map(str, taglist))

    alternativelist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:alternative")
    alternativestring = ""
    if str(alternativelist) != "None":
        if isinstance(alternativelist, str):
            alternativestring=str(alternativelist)
        else:
            alternativestring=' // '.join(map(str, alternativelist))

    annotationlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:annotation")
    annotationstring = ""
    if str(annotationlist) != "None":
        if isinstance(annotationlist, str):
            annotationstring=str(annotationlist)
        else:
            annotationstring=' // '.join(map(str, annotationlist))

    #====== BUILD XML-TREE ==================================================

    if (str(date)[:3] == "180") or (str(date)[:3] == "181") or (str(date)[:3] == "182") or (str(date)[:3] == "183") or (
        str(date)[:3] == "184") or (str(date)[:3] == "185") or (str(date)[:3] == "186") or (str(date)[:3] == "187") or (
        str(date)[:6] == "ca.180") or (str(date)[:6] == "ca.181") or (str(date)[:6] == "ca.182") or (str(date)[:6] == "ca.183") or (
        str(date)[:6] == "ca.184") or (str(date)[:6] == "ca.185")  or (str(date)[:6] == "ca.186") or (str(date)[:6] == "ca.187"):
        pd_counter +=1
        npages = finditem(pagesdata,ppn)
        #print(npages)
        for i in range(int(npages)):
            recordcounter +=1

            XMLoutputfile.write("<record>\n")
            XMLoutputfile.write("<recordID>"+str(recordcounter)+":"+ str(ppn)+":" + str(i+1) + "</recordID>\n")#DONE

            if auteurstring:
                XMLoutputfile.write("<author>"+str(auteurstring)+"</author>\n")#DONE

            if drukkerplaats:
                XMLoutputfile.write("<printer>"+str(drukkernaam)+" in "+str(drukkerplaats)+"</printer>\n")#DONE
            elif drukkernaam:
                XMLoutputfile.write("<printer>"+str(drukkernaam)+"</printer>\n")#DONE

            if uitgevernaam:
                XMLoutputfile.write("<publisher_name>"+str(uitgevernaam)+"</publisher_name>\n")#DONE
            if uitgeverplaats:
                XMLoutputfile.write("<city>"+str(uitgeverplaats)+"</city>\n")#DONE

            if booksize:
                XMLoutputfile.write("<other_fields>{{Information field|name=Book dimensions|value="+str(booksize)+"}}</other_fields>\n")#DONE

            if fulltitle:
                XMLoutputfile.write("<title>"+str(fulltitle) + "</title>\n")#DONE

            XMLoutputfile.write("<date>" + str(date) + "</date>\n")

            XMLoutputfile.write("<language>"+str(language)+"</language>\n")

            XMLoutputfile.write("<description lang='nl'>\n")
            if descriptionstring:
                XMLoutputfile.write("* " + str(descriptionstring)+"\n")
            if alternativestring:
                XMLoutputfile.write("* " + str(alternativestring)+"\n")
            if annotationstring:
                XMLoutputfile.write("* " + str(annotationstring)+"\n")
            if tagstring:
                XMLoutputfile.write("* "+ str(tagstring)+"\n")
            XMLoutputfile.write("</description>\n")

            source = "{{Koninklijke Bibliotheek}}"
            XMLoutputfile.write("<source>"+str(source)+"</source>\n")#DONE

            XMLoutputfile.write("<permission>"+str(permission)+"</permission>\n")#DONE

            XMLoutputfile.write("<pageoverview>")
            for j in range(int(npages)):
                if i == j: # print the number of the current page/file not as a link
                    XMLoutputfile.write(str(j+1))
                else:
                    XMLoutputfile.write("[[:File:"+str(gwtbasetitle)+" - PPN "+str(ppn)+" - Image "+ str(j+1)+".jpeg|"+str(j+1)+"]]")
                if j == int(npages)-1: # if it's the last pagenumber, don't print the divider "--"
                    XMLoutputfile.write("")
                else:
                    XMLoutputfile.write(" -- ")
            XMLoutputfile.write("</pageoverview>\n")

            if references:
                XMLoutputfile.write("<references>"+str(references)+"</references>\n")#DONE

            XMLoutputfile.write("<accessionnumber>* You can see this image on the [http://resolver.kb.nl/resolve?urn=urn:gvn:" + str(
                ppn_long) + " Geheugen van Nederland / Memory of the Netherlands] website (go to image " + str(
                i + 1) + ")\n")
            XMLoutputfile.write("* Description of the book in the Dutch library catalogue: http://www.bibliotheek.nl/catalogus/titel."+ppn+".html" + "</accessionnumber>\n")

            XMLoutputfile.write("<GWToolsettitle>"+str(gwtbasetitle)+" - PPN "+str(ppn)+" - Image "+ str(i+1)+"</GWToolsettitle>\n")

            XMLoutputfile.write("<URLtothemediafile>"+thumb_baseurl+"&amp;role=page&amp;count="+ str(i+1)+"&amp;size=large</URLtothemediafile>\n")

            commonsHomeCat = finditem(catsdata[ppn], "HomeCat").split(":")[1] #strip prefix "Category:" from Homecat
            XMLoutputfile.write("<commonsHomecat>"+str(commonsHomeCat)+"</commonsHomecat>\n")


#===========================
# In deze upload gebruiken we de volgende velden niet:
# XMLoutputfile.write("<wikisource>"+"" + "</wikisource>\n")
# XMLoutputfile.write("<subtitle>"+"" + "</subtitle>\n")
# XMLoutputfile.write("<image>"+"cover van het boekje" + "</image>\n")
# XMLoutputfile.write("<imagepage>"+"" + "</imagepage>\n")#DONE
# XMLoutputfile.write("<homecat>"+"" + "</homecat>\n")
# XMLoutputfile.write("<otherversions>"+"" + "</otherversions>\n")
# XMLoutputfile.write("<isbn>"+"" + "</isbn>\n")
# XMLoutputfile.write("<lccn>"+"" + "</lccn>\n")
# XMLoutputfile.write("<oclc>"+"" + "</oclc>\n")
# XMLoutputfile.write("<linkback>"+""+"</linkback>\n")
# XMLoutputfile.write("<wikidata>"+"wikidata"+"</wikidata>\n")
# XMLoutputfile.write("<translator>"+"" + "</translator>\n")
# XMLoutputfile.write("<editor>"+"" + "</editor>\n")
# XMLoutputfile.write("<illustrator>"+"" + "</illustrator>\n")
# XMLoutputfile.write("<seriestitle>"+""+ "</seriestitle>\n")
# XMLoutputfile.write("<volume>"+"" + "</volume>\n")
# XMLoutputfile.write("<edition>"+"" + "</edition>\n")

            XMLoutputfile.write("</record>\n")
XMLoutputfile.write("</records>\n")

XMLoutputfile.close()
data_file.close()
npagesfile.close()
gwtbasetitlefile.close()

#===========================
#Replace "&" with "&amp;' in XML-file
# See: http://stackoverflow.com/questions/37868881/how-to-search-and-replace-text-in-an-xml-file-using-python
#import lxml.etree as ET
#with open('PrentenboekenXML_GvN_PD_forGWToolset_tmp.xml', encoding="utf8") as f:
#    tree = ET.parse(f)
#    root = tree.getroot()
#    for elem in root.getiterator():
#        try:
#            elem.text = elem.text.replace('&', '&amp;')
#        except AttributeError:
#            pass
#tree.write('PrentenboekenXML_GvN_PD_forGWToolset.xml', xml_declaration=True, method='xml', encoding="utf8")
#======================

print("Number of PD books: "+str(pd_counter))
print("Number of records created: "+str(recordcounter))

