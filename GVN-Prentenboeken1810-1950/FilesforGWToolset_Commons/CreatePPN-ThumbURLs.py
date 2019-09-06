
#Create dict with key = PPN, value = url of thumbnail image (thumb from Commons)

import os, os.path
import json
import requests
import codecs

def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item

def resolveImage(starturl):
    import requests
    r = requests.get(starturl)
    finalurl = r.url
    return finalurl

#outputdirname="output"
current_dir = os.path.dirname(os.path.realpath(__file__))
#outputdir=os.path.join(current_dir)#, outputdirname)
#os.chdir(outputdir)
inputdir=os.path.join(current_dir, "input")
os.chdir(inputdir)

jsonfile="SRUdump_GvN_PRB01_27012017_forGWToolset.json"
with open(jsonfile, encoding="UTF-8") as data_file:
    data = json.load(data_file)

#Open inputfile containing GWT file base titles for each book
ppn_gwtbasetitlefile="PPN_GWTBaseTitle_definitief.json"
with open(ppn_gwtbasetitlefile, encoding="UTF-8") as gwtbasetitlefile:
    gwtbasetitledata = json.load(gwtbasetitlefile)


for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    #============================================================================
#Only use PD images
    date = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcterms:created")

    thumbwidth="600"

    if (str(date)[:3] == "180") or (str(date)[:3] == "181") or (str(date)[:3] == "182") or (str(date)[:3] == "183") or (
                str(date)[:3] == "184") or (str(date)[:3] == "185") or (str(date)[:3] == "186") or (str(date)[:3] == "187") or (
                str(date)[:6] == "ca.180") or (str(date)[:6] == "ca.181") or (str(date)[:6] == "ca.182") or (str(date)[:6] == "ca.183") or (
                str(date)[:6] == "ca.184") or (str(date)[:6] == "ca.185") or (str(date)[:6] == "ca.186") or (str(date)[:6] == "ca.187"):

        ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],
                            "dcx:recordIdentifier")  # PRB01:175094691
        ppn = ppn_long.split(":")[1]  # 175094691
        catalogue_url = "http://www.bibliotheek.nl/catalogus/titel."+ppn+".html"

        title = gwtbasetitle = finditem(gwtbasetitledata,ppn)
        title_us = title.replace(" ", "_") + "_-_PPN_" + str(ppn) + "_-_Image_1.jpeg" #
        image_url = resolveImage("https://commons.wikimedia.org/wiki/Special:Redirect/file/"+ title_us) # Full cover image - https://upload.wikimedia.org/wikipedia/commons/7/7f/Nieuw_A_B_boekje_voor_de_jeugd_-_met_24_gekleurde_plaatjes_-_PPN_139480439_-_Image_1.jpeg

        thumb_url = image_url.replace("/commons/","/commons/thumb/")+"/"+str(thumbwidth)+"px-"+title_us
        print(str(ppn) + " * " + str(catalogue_url)+ " * " +str(thumb_url))
