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

import utility,databases
import os,sys

def shared_date(strip_obj,djv,source_strip):
    if source_strip[0] in djv:
        djv[source_strip[0]]["SharedDateIndex"]=1
        djv[source_strip[0]]["SharedDateTotal"][0]+=1
        strip_obj["SharedDateIndex"]=djv[source_strip[0]]["SharedDateTotal"][0]
        strip_obj["SharedDateTotal"]=djv[source_strip[0]]["SharedDateTotal"]
    else:
        strip_obj["SharedDateIndex"]=0
        strip_obj["SharedDateTotal"]=[1] #1-list approximating a pointer.
        djv[source_strip[0]]=strip_obj

def megadb_fetch_newfiles(alldat,reddit_titles,reddit_links,links_910new):
    print (">>> megadb_fetch_newfiles")
    for sect in ("story","np","sketch"):
        mode=databases.titlebank["modes"][sect]
        arcs=[]
        allot={}
        for number,name in mode:
            if name in allot:
                arcs.append(allot[name])
                continue
            newark={"Title":name,"Comics":[],"RecordType":"StoryLine"}
            utility.specific_section(alldat,sect)["StoryArcs"].append(newark)
            arcs.append(newark)
            allot[name]=newark
        djv={}
        for source_strip in sorted(databases.lsdir[sect].keys()):
            if len(databases.lsdir[sect][source_strip])==2:
                source_strip=(source_strip,)+tuple(databases.lsdir[sect][source_strip])
            else:
                source_strip=databases.lsdir[sect][source_strip]
            if (mode[0][0]) and (source_strip[1]<mode[0][0]):
                continue
            strip_obj={}
            shared_date(strip_obj,djv,source_strip)
            strip_obj["Date"]=source_strip[0]
            strip_obj["Id"]=source_strip[1]
            if strip_obj["Id"] in databases.metadataegs[sect]:
                strip_obj.update(utility.recdeentity(databases.metadataegs[sect][strip_obj["Id"]]))
            strip_obj["OokiiId"]=-1
            strip_obj["FileNameTitle"]=source_strip[2]
            strip_obj["Section"]=utility.egslink2ookii[sect]
            strip_obj["Characters"]={}
            strip_obj["ReactionLinks"]=[]
            if strip_obj["Id"] in reddit_links[sect]:
                strip_obj["ReactionLinks"].append(reddit_links[sect][strip_obj["Id"]])
            if strip_obj["Date"] in links_910new[sect]:
                utility.merge_reactions(strip_obj["ReactionLinks"],links_910new[sect][strip_obj["Date"]])
            utility.dates_index(strip_obj,databases.dateswork[sect])
            if source_strip[1] not in reddit_titles[sect]:
                strip_obj["Titles"]={"Filename":strip_obj["FileNameTitle"]} #For now
            else:
                if utility.alphabetical_id(strip_obj["FileNameTitle"])==utility.alphabetical_id(reddit_titles[sect][source_strip[1]][::-1].split("( ",1)[1][::-1]):
                    strip_obj["Titles"]={"Reddit":reddit_titles[sect][source_strip[1]][:-1]+", based on filename)"}
                else:
                    strip_obj["Titles"]={"Reddit":reddit_titles[sect][source_strip[1]]}
            if ("HtmlComicTitle" in strip_obj) and strip_obj["HtmlComicTitle"]:
                strip_obj["Titles"]["Official"]=strip_obj["HtmlComicTitle"]
            strip_obj["RecordType"]="Comic"
            for number,(id,name) in enumerate(mode):
                if strip_obj["Id"]<id:
                    arcs[number-1]["Comics"].append(strip_obj)
                    break
            else:
                #else clause of for-loop, i.e. finished without break
                arcs[-1]["Comics"].append(strip_obj)
    return alldat

if __name__=="__main__":
    reddit_titles=open(".build/reddit_titles.txt","rU")
    reddit_titles=eval(reddit_titles.read())
    reddit_links=open(".build/reddit_threads.txt","rU")
    reddit_links=eval(reddit_links.read())
    links_910new=open(".build/910-new.dat","rU")
    links_910new=eval(links_910new.read())
    utility.save_alldat(megadb_fetch_newfiles(utility.open_alldat(),reddit_titles,reddit_links,links_910new))

