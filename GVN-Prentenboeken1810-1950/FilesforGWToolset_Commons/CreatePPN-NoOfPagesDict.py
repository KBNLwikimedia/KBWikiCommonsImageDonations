
#Create dict with key = PPN, value = number of pages in book

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

jsonfile="SRUdump_GvN_PRB01_27012017.json"
with open(jsonfile) as data_file:
    data = json.load(data_file)

#outputdirname="output"
current_dir = os.path.dirname(os.path.realpath(__file__))
outputdir=os.path.join(current_dir)#, outputdirname)
#os.chdir(outputdir)

PPN_NoOfPages_Dict = {}

for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    #============================================================================

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],
                        "dcx:recordIdentifier")  # PRB01:175094691
    ppn = ppn_long.split(":")[1]  # 175094691

    thumbnail=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:thumbnail")
    thumb_url=thumbnail['content'] #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X&role=thumbnail

    maximages=70
    numberofimages=0
    for i in range(0,int(maximages)):
        r = requests.head(thumb_url+"&count="+str(i)+"&role=page")
        if int(r.status_code) == 200:
            numberofimages=numberofimages+1
    print(str(ppn), numberofimages)
    PPN_NoOfPages_Dict.update({ppn:str(numberofimages)})

#newlist =PPN_NoOfPages_Dict.items()
#sortedlist = sorted(newlist, key=lambda s: len(s[0]))
with open('PPN_NoOfPages.json', 'w') as fp:
    json.dump(PPN_NoOfPages_Dict, fp, sort_keys=True, indent=0)
    fp.close()
