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

import json, tarfile

_ookii=tarfile.open("Ookii.dat","r:")
def open_lib(path,mode="r",*args):
    return _ookii.extractfile(path.replace("\\","/"))

def scour(obj): #MSLatin1 to UTF-8, works properly on Python 2 only
    if type(obj)==type({}):
        d={}
        for k,v in obj.items():
            d[scour(k)]=scour(v)
        return d
    elif type(obj)==type([]):
        return map(scour,obj)
    elif type(obj)==type(()):
        return map(scour,obj)
    elif type(obj)==type(""):
        if "\x9d" in obj:
            return obj
        else:
            return obj.decode("cp1252").encode("utf8").replace("\xc3\x83\xc2\xbc","\xc3\xbc")
    else:
        return obj

def parse_suddenlaunch(sect):
    suddenlaunch_db={}
    f=open("suddenlaunch.dat","rU")
    b=f.read().split("\n")
    f.close()
    for record in b:
        url,section,date=record.split(" ")
        if section in {"sketch":("Filler",),"story":("Story","Comic")}[sect]:
            month,day,year=date.split("/") #MM/DD/YYYY (middle endian)
            date="-".join((year,month,day)) #YYYY-MM-DD (big endian)
            suddenlaunch_db[date]=url
    return suddenlaunch_db

def fakejsonloads(dat):
    null=None
    true=True
    false=False
    return eval(dat,locals())

date2id=open("Date2Id.txt","rU")
date2id=json.loads(date2id.read())
metadataegs=open("metadataegs3.txt","rU")
metadataegs=eval(metadataegs.read())
dateswork=open("DatesWorkProcessed.txt","rU")
dateswork=eval(dateswork.read())
classics_db=open(".build/classics_910.txt","rU")
classics_db=eval(classics_db.read())
lsdir=open("NewFiles.txt","rU")
lsdir=json.loads(lsdir.read())
reddit_titles=open(".build/reddit_titles.txt","rU")
reddit_titles=eval(reddit_titles.read())
reddit_links=open(".build/reddit_threads.txt","rU")
reddit_links=eval(reddit_links.read())
links_910new=open(".build/910-new.dat","rU")
links_910new=eval(links_910new.read())

main_db={}
for sect in ("story","sketch","np"):
    main_db[sect]=open_lib(r"Ookii\ComicIndices\egscomicapi_%d.txt"%([None,"story","np","sketch"].index(sect)),"rU")
    main_db[sect]=scour(fakejsonloads(main_db[sect].read()))

haylo_db={}
haylo_db["story"]=open(".build/HayloListMini.txt","rU")
haylo_db["story"]=eval(haylo_db["story"].read())
haylo_db["sketch"]={}
haylo_db["np"]={}
haylo_additional_hierarchy={}
haylo_additional_hierarchy["story"]=open(".build/HayloHierarchyAdditional.txt","rU")
haylo_additional_hierarchy["story"]=eval(haylo_additional_hierarchy["story"].read())
haylo_additional_hierarchy["sketch"]=None
haylo_additional_hierarchy["np"]=None

suddenlaunch_db={}
suddenlaunch_db["story"]=parse_suddenlaunch("story")
suddenlaunch_db["sketch"]=parse_suddenlaunch("sketch")
suddenlaunch_db["np"]={}


