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

import utility, os, sys

from databases import *

def handle_strip_record(strip,sect):
    date=strip["Date"]
    #Administrivia about dates and IDs
    utility.find_eid_ookii(strip,sect,date2id)
    #Reactions
    strip["ReactionLinks"]=[]
    if date in classics_db[sect].keys():
        strip["ReactionLinks"].append(classics_db[sect][date])
    if date in suddenlaunch_db[sect].keys():
        strip["ReactionLinks"].append((suddenlaunch_db[sect][date],0))
    #Handle title list
    utility.handle_titles_ookii(strip,sect)
    #Haylo record if applicable
    utility.merge_haylo(strip,haylo_db[sect])
    #Et cetera
    if strip["DateIndexable"]:
        utility.dates_index(strip,dateswork[sect])
    if strip["Id"] in metadataegs[sect]:
        strip.update(metadataegs[sect][strip["Id"]])
    if strip["Id"] in reddit_links[sect]:
        strip["ReactionLinks"].append(reddit_links[sect][strip["Id"]])
    if strip["Date"] in links_910new[sect]:
        utility.merge_reactions(strip["ReactionLinks"],links_910new[sect][strip["Date"]])
    strip["SharedDateIndex"]=0
    #Load specific Ookii DB (i.e. beyond the index card)
    utility.load_ookii_record(strip)
    #Characters
    if strip["Characters"]:
        strip["Characters"]={"Ookii":strip["Characters"]}
    else:
        strip["Characters"]={}
    strip["RecordType"]="Comic"

def handle_line(line,sect):
    map(handle_strip_record,line["Comics"],[sect]*len(line["Comics"]))
    line["RecordType"]="StoryLine"

def megadb_generate_initial():
    print (">>> megadb_generate_initial")
    output=[]
    for sect in ("story","np","sketch"):
        dat=main_db[sect]
        map(handle_line,dat,[sect]*len(dat))
        output.append({"Title":utility.egslink2ookii[sect],"StoryArcs":dat,"RecordType":"Section"})
    return output

if __name__=="__main__":
    utility.save_alldat(megadb_generate_initial())
