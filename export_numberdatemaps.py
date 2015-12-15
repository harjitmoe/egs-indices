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

import utility

alldat=utility.open_alldat()

stdb=utility.specific_section(alldat,"story")["StoryArcs"]
sbdb=utility.specific_section(alldat,"sketch")["StoryArcs"]
npdb=utility.specific_section(alldat,"np")["StoryArcs"]

nem=open(".build/numbereidmap.txt","w")
nom=open(".build/numberoidmap.txt","w")
dim=open(".build/numberdibmap.txt","w")
dfm=open(".build/datefakemap.txt","w")

def munj(id):
    if id==-1:
        return "NONE"
    return id

def print_infos_nem(cd):
    print>>nem, "|-\n|%s||%s||%s"%(cd["Date"],cd["-numberidmap-numero"],munj(cd["Id"]))

def print_infos_nom(cd):
    print>>nom, "|-\n|%s||%s||%s"%(cd["Date"],cd["-numberidmap-numero"],munj(cd["OokiiId"]))

def print_infos_dim(cd):
    print>>dim, "|-\n|%s||%s||%s||%s"%(cd["Date"],cd["-numberidmap-numero"],munj(cd["Id"]),("YES" if cd["DateIndexable"] else "NO"))

def print_infos_dfm(cd):
    print>>dfm, "|-\n|%s||%s||%s"%(munj(cd["Id"]),cd["Date"],cd["DateInBrowserTitle"])

for title,db in (("Main Story",stdb),("Sketchbook",sbdb),("EGS:NP",npdb)):
    print>>nem, "===%s===\n\n{|border=\"1\" cellpadding=\"3\"\n!Date!!Number!!ID (EGSComics)"%title
    print>>nom, "===%s===\n\n{|border=\"1\" cellpadding=\"3\"\n!Date!!Number!!OokiiDB ID"%title
    print>>dim, "===%s===\n\n{|border=\"1\" cellpadding=\"3\"\n!Date!!Number!!ID (EGSComics)!!Date-indexable"%title
    print>>dfm, "===%s===\n\nOnly discrepancies are listed.\n\n{|border=\"1\" cellpadding=\"3\"\n!ID!!ISO Date%s!!Date in browser title"%(title,(" (probable)" if title=="EGS:NP" else " (converted from above comic)"))
    lastid=-40
    lastod=-40
    lastdib=None
    numero=0
    ellipsed_nem=2
    ellipsed_nom=2
    ellipsed_dim=2
    last=None
    lastprinted_nem=None
    lastprinted_nom=None
    lastprinted_dim=None
    for arc in db:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                numero+=1
                comic["-numberidmap-numero"]=numero
                if "DateInBrowserTitle" not in comic.keys():
                    comic["DateInBrowserTitle"]="(Error)"
                if (comic["Id"]!=lastid+1):
                    if (last!=None) and (last!=lastprinted_nem):
                        print_infos_nem(last)
                    print_infos_nem(comic)
                    lastprinted_nem=comic
                    ellipsed_nem=0
                else:
                    if ellipsed_nem==1:
                        print>>nem, "|-\n|...||...||..."
                    ellipsed_nem+=1
                if (comic["OokiiId"]!=lastod+1):
                    if (last!=None) and (last!=lastprinted_nom):
                        print_infos_nom(last)
                    print_infos_nom(comic)
                    lastprinted_nom=comic
                    ellipsed_nom=0
                else:
                    if ellipsed_nom==1:
                        print>>nom, "|-\n|...||...||..."
                    ellipsed_nom+=1
                if (comic["DateIndexable"]!=lastdib):
                    if (last!=None) and (last!=lastprinted_dim):
                        print_infos_dim(last)
                    print_infos_dim(comic)
                    lastprinted_dim=comic
                    ellipsed_dim=0
                else:
                    if ellipsed_dim==1:
                        print>>dim, "|-\n|...||...||...||..."
                    ellipsed_dim+=1
                if (comic["Date"]!=comic["DateInBrowserTitle"]):
                    print_infos_dfm(comic)
                lastod=(comic["OokiiId"] if (comic["OokiiId"]!=-1) else -2)
                lastid=comic["Id"]
                lastdib=comic["DateIndexable"]
                last=comic
    print>>nem, "|}\n\n"
    print>>nom, "|}\n\n"
    print>>dim, "|}\n\n"
    print>>dfm, "|}\n\n"
