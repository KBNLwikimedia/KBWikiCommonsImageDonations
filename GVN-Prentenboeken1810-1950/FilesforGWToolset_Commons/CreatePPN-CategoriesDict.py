# coding=utf-8

# Create dict with key = ppn, value = homecat + list of parentcats
# HomeCat = Name of a unique Commons category per book title, where the individual image files for that book go into
# Parentcats: the (parent) Commons categories the Homeat can be classiefied under - can be more than 1 cat
# Once the dict has been generated:
# 1) we hand-modify the HomeCat (to make sure it is unique (=does not yet exists on Commons, descriptive, concise and not too long,
# 2) We manually add the parent categories


import os, os.path
import json
import codecs
import itertools

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

#Open json inputfile with book-level (not:page-level) metadata
jsonfile="SRUdump_GvN_PRB01_27012017_forGWToolset.json"
with open(jsonfile) as data_file:
    data = json.load(data_file)

#Open inputfile containing GWT file base titles for each book
ppn_gwtbasetitlefile="PPN_GWTBaseTitle_definitief.json"
with open(ppn_gwtbasetitlefile) as gwtbasetitlefile:
    gwtbasetitledata = json.load(gwtbasetitlefile)

Categories_Dict = {}

for i in range(len(gwtbasetitledata)):
    ppn = list(gwtbasetitledata.keys())[i]

    subjectstring     = ""
    annotationstring  = ""
    alternativestring = ""
    descriptionstring = ""
    uitgeverstring    = ""
    drukkerstring     = ""
    auteurstring      = ""

    auteurlist        = []
    drukkerlist       = []
    uitgeverlist      = []
    auteurnamenlist   = []
    drukkernamenlist  = []
    uitgevernamenlist = []

    for book in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):
        ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcx:recordIdentifier")#PRB01:175094691
        ppn2 = ppn_long.split(":")[1]#175094691

        if ppn2 == ppn:

            subjectlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:subject")
            #subjectlist can either be a string or a list[] of strings -- http://www.decalage.info/en/python/print_list
            if str(subjectlist) != "None":
                if isinstance(subjectlist, str): #subjectlist is een string
                    subjectstring=str(subjectlist)
                else: #subjectlist is een list[] of strings
                    subjectstring = ' // '.join(map(str, subjectlist))

            annotationlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:annotation")
            if str(annotationlist) != "None":
                if isinstance(annotationlist, str):
                    annotationstring=str(annotationlist)
                else:
                    annotationstring = ' // '.join(map(str,  annotationlist))

            alternativelist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:alternative")
            if str(alternativelist) != "None":
                if isinstance(alternativelist, str):
                    alternativestring = str(alternativelist)
                else:
                    alternativestring = ' // '.join(map(str, alternativelist))

            descriptionlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:description")
            if str(descriptionlist) != "None":
                if isinstance(descriptionlist, str):
                    descriptionstring = str(descriptionlist)
                else:
                    descriptionstring = ' // '.join(map(str, descriptionlist))

            contributorlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:contributor")
            if str(contributorlist) != "None":
                if isinstance(contributorlist, dict): # contributorlist = dict
                    if contributorlist['dcx:role'] == "uitgever":
                        uitgeverstring=contributorlist['content']
                    elif contributorlist['dcx:role'] == "drukker":
                        drukkerstring=contributorlist['content']
                    elif contributorlist['dcx:role'] == "auteur":
                        auteurstring=contributorlist['content']
                    else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")

                else: # contributorlist = list of dicts
                    for dic in contributorlist:
                     if dic['dcx:role'] == "uitgever": #a book can have multiple publishers, printers, authors
                         uitgeverlist.append(dic['content'])
                         uitgevernamenlist=[" ".join(uitgever.split(", ")[::-1]) for uitgever in uitgeverlist]
                     if dic['dcx:role'] == "drukker":
                         drukkerlist.append(dic['content'])
                         drukkernamenlist=[" ".join(drukker.split(", ")[::-1]) for drukker in drukkerlist]
                     if dic['dcx:role'] == "auteur":
                         auteurlist.append(dic['content'])
                         auteurnamenlist=[" ".join(auteur.split(", ")[::-1]) for auteur in auteurlist]
                     else: print("BBBBBBBBBBBaAAAAAA")


                     auteurstring=' // '.join(map(str, auteurnamenlist))
                     drukkerstring=' // '.join(map(str, drukkernamenlist))
                     uitgeverstring=' // '.join(map(str, uitgevernamenlist))

            Categories_Dict[str(ppn)]={"HomeCat":gwtbasetitledata[ppn]}
            if str(auteurnamenlist) != "[]":
                Categories_Dict[str(ppn)].update({"AuteurCats": auteurstring})
            if str(drukkernamenlist) != "[]":
                Categories_Dict[str(ppn)].update({"DrukkerCats": drukkerstring})
            if str(uitgevernamenlist) != "[]":
                Categories_Dict[str(ppn)].update({"UitgeverCats": uitgeverstring})
            if str(subjectlist) != "None":
                Categories_Dict[str(ppn)].update({"SubjectCats": subjectstring})
            if str(annotationlist) != "None":
                Categories_Dict[str(ppn)].update({"AnnotationCats": annotationstring})
            if str(alternativelist) != "None":
                Categories_Dict[str(ppn)].update({"AlternativeCats": alternativestring})
            if str(descriptionlist) != "None":
                Categories_Dict[str(ppn)].update({"DescriptionCats": descriptionstring})

outputdir=os.path.join(current_dir, "output")
os.chdir(outputdir)

with codecs.open('PPN_Categories.json', 'w') as fp:
    json.dump(Categories_Dict, fp, indent=0, ensure_ascii=False)
    fp.close()
