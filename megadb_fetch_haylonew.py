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
from databases import *

def megadb_fetch_haylonew(main_db):
    print (">>> megadb_fetch_haylonew")
    for name,dates in haylo_additional_hierarchy["story"]:
        db={"Title":": ".join(name.split(" - ",1)),"RecordType":"StoryLine"}
        comics=[]
        for date in dates:
            date,title,fora=haylo_db["story"][date]
            strip={}
            if title.split("-")[-1].strip():
                #Would rather \x96 but...
                strip["Titles"]={"Haylo":title.split("-")[-1].strip().replace("&ndash;","-")}
            else:
                strip["Titles"]={}
            strip["Date"]=date
            try:
                strip["Id"]=date2id["story"][date]
            except:
                strip["Id"]=-1#i.e. error
                print>>sys.stderr,"Error: cannot find date-id mapping for %s"%date
            strip["OokiiId"]=-1
            strip["ReactionLinks"]=fora
            if strip["Date"] in links_910new["story"]:
                utility.merge_reactions(strip["ReactionLinks"],links_910new["story"][strip["Date"]])
            #Date indexing
            strip["DateIndexable"]=False
            if strip["Id"] in dateswork["story"]:
                dsi=dateswork["story"][strip["Id"]]
                for crit in ('WorksInternal','WorksExternal'):
                    if crit in dsi.keys():
                        works,date=dsi[crit]
                        if works:
                            if date!=strip["Date"]:
                                raise AssertionError
                            strip["DateIndexable"]=True
            if strip["Id"] in metadataegs["story"]:
                strip.update(metadataegs["story"][strip["Id"]])
            strip["SharedDateIndex"]=0
            strip["FileNameTitle"]=None
            strip["Section"]="Story"
            strip["Characters"]=None
            strip["RecordType"]="Comic"
            comics.append(strip)
        db["Comics"]=comics
        utility.specific_section(main_db,"story")["StoryArcs"].append(db)
    return main_db

if __name__=="__main__":
    utility.save_alldat(megadb_fetch_haylonew(utility.open_alldat()))

