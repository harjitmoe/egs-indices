#!/usr/bin/env python
# -*- python -*-

# Copyright (c) HarJIT 2014, 2015.
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
#  commercial applications, and to alter and/or distribute it freely in any form,
#  with or without modification, provided that the following conditions are met:
#
#  1. The origin of this work must not be misrepresented; you must not claim that
#     you authored the original work. If you use this work in a product, an
#     acknowledgment in the product documentation would be appreciated but is not
#     required.
#
#  2. Altered versions in any form may not be misrepresented as being the original
#     work, and neither the name of HarJIT nor the names of authors or
#     contributors may be used to endorse or promote products derived from this
#     work without specific prior written permission.
#
#  3. The text of this notice must be included, unaltered, with any distribution.
#

import utility

import os,sys

def handle_strip_record(strip):
    date=strip["Date"]
    #Administrivia about dates and IDs
    utility.find_eid_ookii(strip,sect,date2id)
    #Reactions
    strip["ReactionLinks"]=[]
    if date in classics_db.keys():
        strip["ReactionLinks"].append(classics_db[date])
    if date in suddenlaunch_db.keys():
        strip["ReactionLinks"].append((suddenlaunch_db[date],0))
    #Handle title list
    utility.handle_titles_ookii(strip,sect)
    #Haylo record if applicable
    utility.merge_haylo(strip,haylo_db)
    #Et cetera
    if strip["DateIndexable"]:
        utility.dates_index(strip,dateswork)
    if strip["Id"] in metadataegs:
        strip.update(metadataegs[strip["Id"]])
    if strip["Id"] in reddit_links:
        strip["ReactionLinks"].append(reddit_links[strip["Id"]])
    if strip["Date"] in links_910new:
        utility.merge_reactions(strip["ReactionLinks"],links_910new[strip["Date"]])
    strip["SharedDateIndex"]=0
    #Load specific Ookii DB (i.e. beyond the index card)
    utility.load_ookii_record(strip)
    #Characters
    if strip["Characters"]:
        strip["Characters"]={"Ookii":strip["Characters"]}
    else:
        strip["Characters"]={}
    strip["RecordType"]="Comic"

def handle_line(line):
    map(handle_strip_record,line["Comics"])
    line["RecordType"]="StoryLine"

output=[]

for sect in ("story","np","sketch"):
    locals().update(utility.open_dbs(sect))
    map(handle_line,main_db)
    output.append({"Title":utility.egslink2ookii[sect],"StoryArcs":main_db,"RecordType":"Section"})

open(".build/AllMegaDb.txt","w").write(repr(output))
