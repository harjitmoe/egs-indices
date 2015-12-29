# Copyright (c) HarJIT 2015.
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
#     original work, and neither the name of HarJIT nor the names of authors or
#     contributors may be used to endorse or promote products derived from this
#     work without specific prior written permission.
#
#  3. The text of this notice must be included, unaltered, with any distribution.
#

import re
import utility

def slice_characters(s):
    curchar=""
    depth=0
    for c in s.rstrip():
        if c=="(":
            depth+=1
            curchar+=c
        elif c==")":
            depth-=1
            curchar+=c
        elif c=="," and depth==0:
            yield curchar
            curchar=""
        elif c==" " and curchar=="":
            pass
        else:
            curchar+=c
    yield curchar

def megadb_fetch_zorua(alldat):
    print (">>> megadb_fetch_zorua")
    f=open("zorua_db.dat","rU")
    db=[]
    charobjs={}
    for line in f: #Very rare that I actually do this
        if not line.startswith("Page "):
            continue
        #NB: Someday in the distant future I might parse it properly
        #rather than doing this
        ldb={}
        line=line.split("//",1)[0]
        line=line[len("Page "):]
        line=line.split(" ",1)[1]
        if line.startswith("(NON-CANON): "):
            line=line[len("(NON-CANON): "):]
        title=""
        date=None
        if re.match(r"\(?[0123456789][0123456789]?/[0123456789][0123456789]?/[0123456789][0123456789]?\)?", line):
            date,line=line.split(" ",1)
            if date[0]=="(":
                date=date[1:-1]
            #Convert from middle-endian no-leading-zeros slashes
            #to big-endian fixed-digits hyphens
            month,day,year=date.split("/")
            month=int(month,10)
            day=int(day,10)
            year=int(year,10)+2000
            date="%04d-%02d-%02d"%(year,month,day)
        if line.startswith('"'):
            line=line[1:]
            #Should be fairly reliable
            while not line.startswith('"'):
                title+=line[0]
                line=line[1:]
            while not line.startswith(':'):
                title+=line[0]
                line=line[1:]
            title=title[:-1]
            line=line.split(" ",1)[1]
        if date:
            ldb["Date"]=date
        ldb["Title"]=title
        ldb["Characters"]=[]
        line=slice_characters(line)
        line=[i.split("(",1)[0].rstrip() for i in line]
        map={"tess":"tedd","tedd/tess":"tedd"}
        for name in line:
            #if name.lower() in ("np debut)","debut)"):
            #    continue
            nom=map[name.lower()] if name.lower() in map else name.lower()
            if nom in charobjs:
                charobjs[nom]["count"]+=1
            else:
                charobjs[nom]={"count":1}
            ldb["Characters"].append({'CharacterName':name,'AppearanceNumber':charobjs[nom]["count"]})
        db.append(ldb)
    for arc in utility.specific_section(alldat,"np")["StoryArcs"]:
        for strip in arc['Comics']:
            if db:
                ldb=db.pop(0)
                if "Date" in ldb:
                    print strip['Date'],ldb["Date"]
                if ldb["Title"].strip():
                    strip['Titles']["Zorua"]=ldb["Title"]
                if ldb["Characters"]:
                    strip['Characters']["Zorua"]=ldb["Characters"]
    return alldat

if __name__=="__main__":
    utility.save_alldat(megadb_fetch_zorua(utility.open_alldat()))
