#!/usr/bin/env python
# -*- python -*-

# Copyright (c) Thomas Hori 2015.
#
#  THIS WORK IS PROVIDED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES,
#  INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT WILL THE AUTHORS OR CONTRIBUTORS
#  BE HELD LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE),
#  ARISING IN ANY WAY OUT OF THE USE OF THIS WORK, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
#  Permission is granted to anyone to use this work for any purpose, including
#  commercial applications, and to alter it and/or redistribute it freely in any
#  form, with or without modification, subject to the following restrictions:
#
#  1. The origin of this work must not be misrepresented; you must not claim that
#     you authored the original work. If you use this work in a product, an
#     acknowledgment in the product documentation would be appreciated but is not
#     required.
#
#  2. Altered versions in any form must not be misrepresented as being the 
#     original work, and neither the name of Thomas Hori nor the names of authors or
#     contributors may be used to endorse or promote products derived from this
#     work without specific prior written permission.
#
#  3. The text of this notice must be included, unaltered, with any distribution.
#

import utility
import databases

def merge_haylo(strip,haylo_db):
    if strip["Date"] in haylo_db:
        date,title2,fora=haylo_db[strip["Date"]]
        title2=title2.replace("Animi-Style","Anim\xe9-Style".decode("cp1252").encode("utf8"))
        for el in databases.titlebank["haylo_errorlinks"]:
            if el in [i[0] for i in fora]:
                #Apparantly an error in the Haylo list.  Made up for by Herald Loveall list.
                del fora[[i[0] for i in fora].index(el)]
        utility.merge_reactions(strip["ReactionLinks"],fora)
        if "Ookii" in strip["Titles"]:
            strip["Titles"]["Haylo"]=title2.split("-")[-1].strip()

def handle_titles_ookii(strip,sect):
    if "untitled" in strip["Title"].lower():
        strip["Titles"]={"Ookii":strip["Title"].split("-",1)[-1].strip()}
    else:
        strip["Titles"]={"Official":strip["Title"]}
    del strip["Title"]
    if sect=="sketch":
        if strip["Id"] in databases.titlebank["datitles"]:
            strip["Titles"]["DeviantArt"]=databases.titlebank["datitles"][strip["Id"]]
        strip["SharedDateIndex"]=0

def find_eid_ookii(strip,sect,date2id):
    if (sect=="np") and (strip["Date"]=="2005-08-15"):
        strip["Date"]="2005-08-16" #Error somewhere? It's 16
    strip["OokiiId"]=strip["Id"]
    strip["SpecialUrl"]=None
    strip["DateIndexable"]=1
    try:
        strip["Id"]=date2id[sect][strip["Date"]]
    except KeyError:
        strip["Id"]=-1#i.e. error
        if (sect=="sketch") and (strip["Date"] in ("2007-06-26","2007-06-28","2007-06-30")):
            #Dead multi-image entries which did not transfer off Keenspot and have no
            #parallel in the present archives exist and are listed in the Ookii database.
            #Fortunately, the Wayback Machine has us covered.
            strip["SpecialUrl"]="http://wayback.archive.org/web/20081222223622/egscomics.com/Filler/d/"+strip["Date"].replace("-","")+".html"
            strip["DateIndexable"]=0
        elif (sect=="sketch") and (strip["Date"] in ("2012-11-27",)):
            #For some bizarre reason, this one is no longer available and lacks a modern lookup ID.
            #It is fortunately displayed on Dan's Tumblr in its entirity.
            strip["SpecialUrl"]="http://danshive.tumblr.com/post/36647880400/site-link-watching-star-trek-ii-whats-funny"
            strip["DateIndexable"]=0
        else:
            print>>sys.stderr,"Error: cannot find date-id mapping for %s"%strip["Date"]

def handle_strip_record(strip,sect,classics_db,haylo_db,reddit_links,links_910new):
    date=strip["Date"]
    #Administrivia about dates and IDs
    find_eid_ookii(strip,sect,databases.date2id)
    #Reactions
    strip["ReactionLinks"]=[]
    if date in classics_db[sect].keys():
        strip["ReactionLinks"].append(classics_db[sect][date])
    if date in databases.suddenlaunch_db[sect].keys():
        strip["ReactionLinks"].append((databases.suddenlaunch_db[sect][date],0))
    #Handle title list
    handle_titles_ookii(strip,sect)
    #Haylo record if applicable
    if sect=="story":
        merge_haylo(strip,haylo_db)
    #Et cetera
    if strip["DateIndexable"]:
        utility.dates_index(strip,databases.dateswork[sect])
    if strip["Id"] in databases.metadataegs[sect]:
        strip.update(utility.recdeentity(databases.metadataegs[sect][strip["Id"]]))
    if strip["Id"] in reddit_links[sect]:
        strip["ReactionLinks"].append(reddit_links[sect][strip["Id"]])
    if strip["Date"] in links_910new[sect]:
        utility.merge_reactions(strip["ReactionLinks"],links_910new[sect][strip["Date"]])
    strip["SharedDateIndex"]=0
    #Load specific Ookii DB (i.e. beyond the index card)
    databases.load_ookii_record(strip)
    #Characters
    if strip["Characters"]:
        strip["Characters"]={"Ookii":strip["Characters"]}
    else:
        strip["Characters"]={}
    strip["RecordType"]="Comic"

def handle_line(line,sect,classics_db,haylo_db,reddit_links,links_910new):
    for comic in line["Comics"]:
        handle_strip_record(comic,sect,classics_db,haylo_db,reddit_links,links_910new)
    line["RecordType"]="StoryLine"

def megadb_generate_initial(classics_db,haylo_db,reddit_links,links_910new):
    print (">>> megadb_generate_initial")
    output=[]
    for sect in ("story","np","sketch"):
        dat=databases.main_db[sect]
        for line in dat:
            handle_line(line,sect,classics_db,haylo_db,reddit_links,links_910new)
        output.append({"Title":utility.egslink2ookii[sect],"StoryArcs":dat,"RecordType":"Section"})
    return output

if __name__=="__main__":
    classics_db=open(".build/classics_910.txt","rU")
    classics_db=eval(classics_db.read())
    links_910new=open(".build/910-new.dat","rU")
    links_910new=eval(links_910new.read())
    utility.save_alldat(megadb_generate_initial(classics_db,haylo_db,reddit_links,links_910new))
