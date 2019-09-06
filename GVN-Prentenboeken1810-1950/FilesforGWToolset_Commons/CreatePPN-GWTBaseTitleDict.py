# coding=utf-8

# Create dict with key = ppn, value = full book title
# Once the dict has been created, we hand-modify the value into a GWT base title.
# For instance: truncate it, to be suitable as a base title for a Commons:File:

import os, os.path
import json
import codecs


def finditem(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = finditem(v, key)
            if item is not None:
                return item


#==================
current_dir = os.path.dirname(os.path.realpath(__file__))

#Open json inputfile with book-level (not:page-level) metadata
inputdir=os.path.join(current_dir, "input")
os.chdir(inputdir)
jsonfile="SRUdump_GvN_PRB01_27012017_forGWToolset.json"
with open(jsonfile) as data_file:
    data = json.load(data_file)

#Open inputfile containing number of pages for each book
ppn_npagesfile="PPN_NoOfPages_definitief.json"
with open(ppn_npagesfile) as npagesfile:
    pagesdata = json.load(npagesfile)

#Open inputfile containing GWT file base titles for each book
ppn_gwtbasetitlefile="PPN_GWTBaseTitle_definitief.json"
with open(ppn_gwtbasetitlefile) as gwtbasetitlefile:
    gwtbasetitledata = json.load(gwtbasetitlefile)



aDict={}
FullTitle_GWTBaseTitle_Dict = {}

for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):

    ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],
                        "dcx:recordIdentifier")  # PRB01:175094691
    ppn = ppn_long.split(":")[1]  # 175094691

    date = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcterms:created")

    if (str(date)[:3] == "180") or (str(date)[:3] == "181") or (str(date)[:3] == "182") or (str(date)[:3] == "183") or (
        str(date)[:3] == "184") or (str(date)[:3] == "185") or (str(date)[:3] == "186") or (str(date)[:3] == "187") or (
        str(date)[:6] == "ca.180") or (str(date)[:6] == "ca.181") or (str(date)[:6] == "ca.182") or (str(date)[:6] == "ca.183") or (
        str(date)[:6] == "ca.184") or (str(date)[:6] == "ca.185")  or (str(date)[:6] == "ca.186") or (str(date)[:6] == "ca.187"):
        title = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:title")
        if title:
            title_short=title.split(" / ")[0]
            FullTitle_GWTBaseTitle_Dict[str(ppn)]= str(title_short)

outputdir=os.path.join(current_dir, "output")
os.chdir(outputdir)

with codecs.open('PPN_GWTBaseTitle.json', 'w') as fp:
    json.dump(FullTitle_GWTBaseTitle_Dict, fp, indent=0, ensure_ascii=False)
    fp.close()
