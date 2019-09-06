
import os, os.path, glob
import json
from pprint import pprint
from lxml import html
import requests

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item


#config paths/ urls
current_dir = os.path.dirname(os.path.realpath(__file__))
imagedir= current_dir + "\\images\\"
images_base_url="https://www.kb.nl/kbhtml/kopiewapenboek/"

#transcription_base_url = "http://localhost:8080/page_" #Mongoose webservertje op C:\temp\webserver aanzetten - in de subfolder ""browse" staan de trancriptie-bestanden (de htmls)

homepage = "https://www.kb.nl/themas/middeleeuwen/wapenboek-beyeren-1405"
sourcetemplate = "{{Koninklijke Bibliotheek}}"
provider = "Koninklijke Bibliotheek"


# {{Artwork}} template on Commons, as stated in GWToolset
# accessionnumber =	"" (=ppn)
# artist =	""
# author =	""
# creditline =	""
# date =	""
# demo =		""
# department =		""
# description =		""
# dimensions =		""
# exhibitionhistory =	""
# inscriptions =		""
# institution =		""
# medium =		""
# notes =		""
# objecthistory =	""
# objecttype =		""
# otherfields =		""
# otherversions =		""
# permission =		""
# placeofcreation =		""
# placeofdiscovery =		""
# references =		""
# source =		""
# strict =		""
# title =		""
# wikidata =
# wikidatacat =	""
# GWToolsettitle =	""
# URLtothemediafile =""

#---------------------------
#DUMP uit KB-cat

#                         Titel: Wapenboek / samengesteld door heraut Beyeren
#                                [Claes Heynenz. (ca. 1345-1414)]
#                                Wapenboek Beyeren
#                        Auteur: ... Gelre heraut (ca. 1345-1414)
#             Vroegere eigenaar: Anton Willem den Beer Poortugael (1864-1940);
#                                Pallio di Rinco; Amersfoort, Archief Eemland;
#                                Amersfoort, Museum Flehite
#                          Jaar: [ca. 1600]
#                  Localisering: [Zuidelijke Nederlanden?]
#                     Annotatie: Kopie van het zgn. Wapenboek Beyeren uit 1405
#                                (thans Den Haag, KB : 79 K 21)
#                                Datering band: 1600
#                                1096 ingekleurde wapenschilden
#                 Bevat / omvat: Bevat 1096 ingekleurde wapenschilden, met
#                                bijschriften in het Frans: - I (p. 1-23): 337
#                                wapens van deelnemers aan een toernooi te
#                                Compiègne; februari 1238; - II (p. 23-36):
#                                191 wapens van deelnemers aan een toernooi in
#                                Mons; 1310; - III (p. 36-62): 404 wapens van
#                                deelnemers aan een expeditie tegen de Friezen
#                                in Kuinre; 1396; - IV (p. 62-69): 122 wapens
#                                van deelnemers aan het beleg van Gorinchem;
#                                1402; - V (p. 70-74): 14 series van 3 'besten'
# Annotatie primaire verwerving: In 2007 gekocht van Museum Flehite in
#                                Amersfoort
#          Herkomstgeschiedenis: Pallio de Rinco (1665). In 1941 gelegateerd
#                                door A.W. den Beer Poortugael; door Museum
#                                Flehite in Amersfoort ondergebracht in Archief
#                                Eemland in Amersfoort
#----------------------

accessionnumber = "310865379"
institution = provider
medium = "Illustrations (coat of arms) on paper"
dimensions = "{{Size|mm|251|187}}"
permission = "{{PD-art|PD-old-70-1923}}"
source = sourcetemplate
date = "This copy armorial is from ca. 1600. The [[:w:nl:Wapenboek_Beyeren|original]] is from 1405." # nog navragen bij EvdV
#-artist = "Binder: [[:w:en:Lodewijk_Elzevir|Lodewijk Elzevier I]] (ca. 1547-1617)"
author = "The scribe of this copy of the Beyeren armorial is unknown. The orignal armorial was made by [[:w:nl:Claes_Heynensoon|Claes Heynensoon]] / heraut Beyeren voorheen Gelre (ca. 1345-1414) {{Creator:Claes Heynenzoon}}"
title = "[[:w:nl:Wapenboek_Beyeren|Wapenboek Beyeren]] (armorial)"
placeofcreation = "Southern Netherlands?"
#-wikidata = "Q3372028"
inscriptions = "The inscriptions are explained (transcribed) in the orginal armorial, see [https://galerij.kb.nl/kb.html#/nl/wapenboek/ the digitised manuscript] on the website of the KB"
otherversions =		"The [[:Category:Digitised_version_of_Armorial_de_Beyeren|orginal version of the Beyeren armorial]] from 1405 on Wikimedia Commons"


#f = open('transcriptions.txt','w')
XMLoutputfile = open("kopie-wapenboekbeyeren.xml", "w")

XMLoutputfile.write("<?xml version='1.0' encoding='UTF-8'?>\n")
XMLoutputfile.write("<records>\n")

for infile in glob.glob(os.path.join(imagedir, '*.jpg')):
    picname=infile.replace(imagedir, "") #"KB76K16_p02.jpg"
    print(picname)
    picname_trunc=picname.replace(".jpg", "") #"KB79K16_p02"
    # split in 2 parts: KB79K16 + p02
    if picname_trunc != "KB79K16_omslagvoor":
        page = picname_trunc.split("_p")[1] #02
        signatuur= picname_trunc.split("_")[0] #KB79K16


    XMLoutputfile.write("   <record>\n")
    XMLoutputfile.write("       <accessionnumber>Description of this copy of the Beyeren armorial in the catalogue of the KB: http://opc4.kb.nl/PPN?PPN="+ accessionnumber +"</accessionnumber>\n")
    XMLoutputfile.write("       <dimensions>" + dimensions + "</dimensions>\n")
    XMLoutputfile.write("       <Institution>" + institution + "</Institution>\n")
    XMLoutputfile.write("       <permission>"+permission+"</permission>\n")
    XMLoutputfile.write("       <source>"+source+"</source>\n")
    # XMLoutputfile.write("       <page>"+str(picname_trunc)+"</page>\n")
    XMLoutputfile.write("       <author>"+ str(author) + "</author>\n")
    # XMLoutputfile.write("       <artist>"+ str(artist) + "</artist>\n")
    XMLoutputfile.write("       <date>" + str(date) + "</date>\n")
    XMLoutputfile.write("       <placeofcreation>"+str(placeofcreation)+"</placeofcreation>\n")
    # XMLoutputfile.write("       <wikidata>"+str(wikidata)+"</wikidata>\n")

#Exceptions for non-typical pages
    if picname_trunc == "KB79K16_omslagvoor":
        XMLoutputfile.write("       <description>Parchment binding from ca. 1600 with handwritten text ''Ecussons d'armes enluminees de ceux qui se sont trouves en divers tournois en France, Flandres et Haynaut''</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Parchment binding from ca. 1600 with handwritten text - Copy of Wapenboek Beyeren (armorial)</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>Parchment binding from ca. 1600 with handwritten text ''Ecussons d'armes enluminees de ceux qui se sont trouves en divers tournois en France, Flandres et Haynaut'' from a copy of "+ title + "</title>\n")
        XMLoutputfile.write("       <medium>Parchment binding with handwritten text</medium>\n")
        XMLoutputfile.write("       <otherversions>"+ otherversions + "</otherversions>\n")

#the typical pages
    else:
        XMLoutputfile.write("       <description>Page " + page + " from a copy of the Beyeren armorial / [[:w:nl:Wapenboek_Beyeren|Wapenboek Beyeren]] from ca. 1600. The original Beyeren armorial from 1405 can be viewed at the [" +homepage + " website of the KB]</description>\n")
        XMLoutputfile.write("       <URLtothemediafile>"+images_base_url+str(picname)+"</URLtothemediafile>\n")
        XMLoutputfile.write("       <GWToolsettitle>Page " + page +" from a copy of Wapenboek Beyeren (armorial) from ca. 1600</GWToolsettitle>\n")
        XMLoutputfile.write("       <title>Page " + page +" from a copy of "+ title +" </title>\n")
        XMLoutputfile.write("       <medium>"+ medium +"</medium>\n")
        XMLoutputfile.write("       <otherversions>"+ otherversions + "</otherversions>\n")
        XMLoutputfile.write("       <inscriptions>"+ inscriptions + "</inscriptions>\n")
    XMLoutputfile.write("   </record>\n")
XMLoutputfile.write("</records>\n")

XMLoutputfile.close()
