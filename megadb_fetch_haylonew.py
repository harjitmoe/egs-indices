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

import sys,utility,databases

def megadb_fetch_haylonew(main_db,haylo_additional_hierarchy,haylo_db,links_910new):
    print (">>> megadb_fetch_haylonew")
    for name,dates in haylo_additional_hierarchy:
        db={"Title":": ".join(name.split(" - ",1)),"RecordType":"StoryLine"}
        comics=[]
        for date in dates:
            date,title,fora=haylo_db[date]
            strip={}
            if title.split("-")[-1].strip():
                #Would rather \x96 but...
                strip["Titles"]={"Haylo":title.split("-")[-1].strip()}
            else:
                strip["Titles"]={}
            strip["Date"]=date
            try:
                strip["Id"]=databases.date2id["story"][date]
            except:
                strip["Id"]=-1#i.e. error
                print("Error: cannot find date-id mapping for %s"%date, file=sys.stderr)
            strip["OokiiId"]=-1
            strip["ReactionLinks"]=fora
            if strip["Date"] in links_910new["story"]:
                utility.merge_reactions(strip["ReactionLinks"],links_910new["story"][strip["Date"]])
            #Date indexing (XXX)
            utility.dates_index(strip,databases.dateswork["story"])
            if strip["Id"] in databases.metadataegs["story"]:
                strip.update(utility.recdeentity(databases.metadataegs["story"][strip["Id"]]))
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
    links_910new=open(".build/910-new.dat","rU")
    links_910new=eval(links_910new.read())
    haylo_db=open(".build/HayloListMini.txt","rU")
    haylo_db=eval(haylo_db.read())
    haylo_additional_hierarchy=open(".build/HayloHierarchyAdditional.txt","rU")
    haylo_additional_hierarchy=eval(haylo_additional_hierarchy.read())
    utility.save_alldat(megadb_fetch_haylonew(utility.open_alldat(),haylo_additional_hierarchy,haylo_db,links_910new))

