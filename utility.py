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

import sys,os

#so as to pass JSON to eval
null=None
false=False
true=True

class SimpleNamespace(object): pass

titlebank=SimpleNamespace()
titlebanf=open("titlebank.dat","rU")
titlebank.__dict__.update(eval(titlebanf.read()))
titlebanf.close()
sys.modules["titlebank"]=titlebank

import pickle
def open_alldat():
    f=open(".build/AllMegaDb.pickle","rb")
    b=pickle.load(f)
    f.close()
    return b
def save_alldat(b):
    f=open(".build/AllMegaDb.pickle","wb")
    pickle.dump(b,f)
    f.close()
    return b

#Use a tarfile: due to the sheer number of small files, the Ookii subdirectory was taking a
#disproportionately long time (for its file size) to copy to backup, and taking a disproportionate
#drive footprint.  Using a tarfile fixes this problem.
import tarfile
ookii=tarfile.open("Ookii.dat","r:")
def open_lib(path,mode="r",*args):
    if path.replace("\\","/").startswith("Ookii/"):
        if mode.startswith("r"):
            return ookii.extractfile(path.replace("\\","/"))
    return open(path,mode,*args)

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

def month2number(month):
    #Just a TAD NEUROTIC?
    if month[:3]=="Qui": month="Jul" #Quinctilis=July
    if month[:3]=="Sex": month="Aug" #Sextilis=August
    return "%02d"%[None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(month[:3])

def number2month(month):
    return [None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(month)]

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

def open_dbs(sect):
    date2id=open("Date2Id.txt","rU")
    date2id=eval(date2id.read())[sect]
    metadataegs=open("metadataegs3.txt","rU")
    metadataegs=eval(metadataegs.read())[sect]
    dateswork=open("DatesWorkProcessed.txt","rU")
    dateswork=eval(dateswork.read())[sect]
    classics_db=open(".build/classics_910.txt","rU")
    classics_db=eval(classics_db.read())[sect]
    lsdir=open("NewFiles.txt","rU")
    lsdir=eval(lsdir.read())[sect]
    reddit_titles=open(".build/reddit_titles.txt","rU")
    reddit_titles=eval(reddit_titles.read())[sect]
    reddit_links=open(".build/reddit_threads.txt","rU")
    reddit_links=eval(reddit_links.read())[sect]
    links_910new=open(".build/910-new.dat","rU")
    links_910new=eval(links_910new.read())[sect]
    main_db=open_lib(r"Ookii\ComicIndices\egscomicapi_%d.txt"%([None,"story","np","sketch"].index(sect)),"rU")
    main_db=scour(eval(main_db.read()))
    if sect=="story":
        haylo_db=open(".build/HayloListMini.txt","rU")
        haylo_db=eval(haylo_db.read())
        haylo_additional_hierarchy=open(".build/HayloHierarchyAdditional.txt","rU")
        haylo_additional_hierarchy=eval(haylo_additional_hierarchy.read())
    else:
        haylo_db={}
        haylo_additional_hierarchy=None
    if sect in ("story", "sketch"):
        suddenlaunch_db=parse_suddenlaunch(sect)
    else:
        suddenlaunch_db={}
    return locals()

def standardise910link(l):
    #http://community.910cmx.com/?showtopic=7761
    #http://community.910cmx.com/index.php?showtopic=7761
    #http://community.910cmx.com/?/topic/7761-np-february-19-2010/
    #http://community.910cmx.com/index.php?/topic/7761-np-february-19-2010/
    #http://community.910cmx.com/index.php?/topic/7761-np-february-19-2010/?view=getnewpost
    if l.startswith("http://community.910cmx.com/?/topic/"):
        l=l[len("http://community.910cmx.com/?/topic/"):].split("-")[0]
        l="http://community.910cmx.com/?showtopic="+l
    elif l.startswith("http://community.910cmx.com/index.php?/topic/"):
        l=l[len("http://community.910cmx.com/index.php?/topic/"):].split("-")[0]
        l="http://community.910cmx.com/?showtopic="+l
    elif l.startswith("http://community.910cmx.com/index.php?showtopic="):
        l=l[len("http://community.910cmx.com/index.php?showtopic="):].split("&")[0]
        l="http://community.910cmx.com/?showtopic="+l
    return l

def datefix_910(date,sect):
    """Fix dates of 910 threads to match database in cases 
    where precise date is disputable."""
    # Much of this was written during a 910 outage.
    # Much of this is in need of verification.
    if date=="2012-08-12" and sect=="story":
        return "2012-08-13" #Confirmed by Loveall
    if date=="2012-08-16" and sect=="story":
        return "2012-08-15"
    if date=="2012-12-16" and sect=="story":
        return "2012-12-17"
    if date=="2013-02-03" and sect=="story":
        return "2013-02-04"
    #Not safe to double call
    if date=="2013-02-04" and sect=="story":
        return "2013-02-05"
    if date=="2012-03-29" and sect=="story":
        return "2013-03-29" #probably
    if date=="2012-08-04" and sect=="story":
        return "2013-08-05"
    if date=="2015-08-05" and sect=="sketch":
        return "2015-08-04"
    if date=="2015-01-16" and sect=="sketch":
        return "2015-01-15"
    if date=="2015-12-07" and sect=="sketch":
        return "2015-12-08"
    if date=="2013-02-15" and sect=="sketch":
        return "2013-02-20"
    if date=="2014-08-15" and sect=="np":
        return "2014-08-14"
    if date=="2014-08-27" and sect=="np":
        return "2014-08-26"
    if date=="2015-04-29" and sect=="np":
        return "2015-04-28"
    if date=="2015-07-17" and sect=="np":
        return "2015-07-16"
    if date=="2015-01-14" and sect=="np":
        return "2015-01-15"
    if date=="2014-08-20" and sect=="np":
        return "2014-08-19"
    return date

def alphabetical_id(string):
    return tuple(filter(lambda i:i in "qwertyuiopasdfghjklzxcvbnm",string.lower()))

def dates_index(strip,dateswork):
    strip["DateIndexable"]=False
    if strip["Id"] in dateswork:
        dsi=dateswork[strip["Id"]]
        for crit in ('WorksInternal','WorksExternal'):
            if crit in dsi.keys():
                works,date=dsi[crit]
                if works:
                    if date!=strip["Date"]:
                        raise AssertionError
                    strip["DateIndexable"]=True

def load_ookii_record(strip):
    """Load the full Ookii record given the index card."""
    specific_db=open_lib(r"Ookii\ComicRecords\egscomicapi_%d.txt"%strip["OokiiId"],"rU").read()
    if not specific_db:
        print>>sys.stderr,"DEAD DOOR",strip["Date"],strip["OokiiId"]
    else:
        strip.update(scour(eval(specific_db)))

from titlebank import datitles, haylo_errorlinks

def handle_titles_ookii(strip,sect):
    if "untitled" in strip["Title"].lower():
        strip["Titles"]={"Ookii":strip["Title"].split("-",1)[-1].strip()}
    else:
        strip["Titles"]={"Official":strip["Title"]}
    del strip["Title"]
    if sect=="sketch":
        if strip["Id"] in datitles:
            strip["Titles"]["DeviantArt"]=datitles[strip["Id"]]
        strip["SharedDateIndex"]=0

def merge_haylo(strip,haylo_db):
    if strip["Date"] in haylo_db:
        date,title2,fora=haylo_db[strip["Date"]]
        title2=title2.replace("Animi-Style","Anim\xe9-Style".decode("cp1252").encode("utf8"))
        for el in haylo_errorlinks:
            if el in [i[0] for i in fora]:
                #Apparantly an error in the Haylo list.  Made up for by Herald Loveall list.
                del fora[[i[0] for i in fora].index(el)]
        merge_reactions(strip["ReactionLinks"],fora)
        if "Ookii" in strip["Titles"]:
            strip["Titles"]["Haylo"]=title2.split("-")[-1].strip()

def find_eid_ookii(strip,sect,date2id):
    if (sect=="np") and (strip["Date"]=="2005-08-15"):
        strip["Date"]="2005-08-16" #Error somewhere? It's 16
    strip["OokiiId"]=strip["Id"]
    strip["SpecialUrl"]=None
    strip["DateIndexable"]=1
    try:
        strip["Id"]=date2id[strip["Date"]]
    except:
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

egslink2ookii={"story":"Story","sketch":"Sketchbook","np":"EGS:NP"}
ookii2egslink=dict(zip(*zip(*egslink2ookii.items())[::-1]))
ookii2url={"Story":"index.php","EGS:NP":"egsnp.php","Sketchbook":"sketchbook.php"}

def merge_reactions(a,b):
    a1=[i[0] for i in a]
    for i in b:
        if i[0] not in a1:
            a.append(i)

def specific_section(all,sect):
    for section in all:
        if section["Title"]==egslink2ookii[sect]:
            return section
    raise IndexError,"section %r not in db"%sect

def clean(title):
    #'So Much For Vladia\x19s \x18No Violent Threats\x19 Streak&'
    return title.replace("&","&amp;").replace("\x18","&lsquo;").replace("\x19","&rsquo;").replace('"',"&quot;").replace('\x14',"...").replace("<","&lt;").replace(">","&gt;")

def dirty(title):
    return title.replace("&lsquo;","\x18").replace("&rsquo;","\x19").replace("&#39;","\x19").replace("&quot;",'"').replace("&lt;","<").replace("&gt;",">").replace("&nbsp;"," ").replace("&amp;","&")

#In order of preference (best first)
title_sources=("Official","DeviantArt","Tumblr","Haylo","Ookii","Zorua","HarJIT","Reddit")
prefers=("Ookii","Haylo","Zorua")
def get_every_sane_title(comic):
    value=[]
    for ttype in title_sources:
        if ttype in comic["Titles"]:
            if comic["Titles"][ttype]:
                value.append(comic["Titles"][ttype]+" ("+ttype+")")
    return clean((" / ".join(value)) or "")
def get_preferred_title(comic): #Artefact function name
    value=[]
    for ttype in title_sources:
        if ttype in comic["Titles"]:
            if comic["Titles"][ttype]:
                value.append(comic["Titles"][ttype]+" ("+ttype+")")
    if (not value) and comic["Titles"]:
        value.extend([i[1]+" ("+i[0]+")" for i in comic["Titles"].items()])
    return clean((" / ".join(value)) or "Untitled.")
def get_preferred_title_2(comic,pref):
    for ttype in (pref,)+title_sources:
        if ttype in comic["Titles"]:
            return clean(comic["Titles"][ttype])
    if comic["Titles"]:
        return clean(comic["Titles"][comic["Titles"].keys()[0]])
    return "Untitled."

def detag(s):
    o=""
    a=1
    for c in s:
        if c=="<":
            a=0
        elif c==">":
            a=1
        elif a:
            o+=c
    assert a,"partial tag?"
    return o

from calendar import weekday as getwd

_iso2top={}

def top2iso(top):
    wd,md,y=top.split(", ")
    m,d=md.split()
    d="%02d"%int(d)
    m=month2number(m)
    iso=y+"-"+m+"-"+d
    if iso not in _iso2top:
        _iso2top[iso]=top
    return iso

def iso2top(iso):
    if iso not in _iso2top:
        y,m,d=iso.split("-")
        m=int(m,10)
        m2=number2month(m)[:3]
        d=int(d,10)
        y=int(y)
        wd="Comic for "+getwd(y,m,d)
        _iso2top[iso]="%s, %s %d, %04d"%(wd,m2,d,y)
    return _iso2top[iso]

def openrf(fn, *mode):
    import os
    try:
        from MacOS import openrf
    except ImportError:
        mode=list(mode)
        if mode:
            #MacOS.openrf allows and ignores asterisks.
            #One is passed by AppleSingle.py without explanation.
            #Ignore them likewise.
            mode[0]=mode[0].replace("*","")
        try:
            #NTFS under Windows and others
            return open(fn+":rsrc", *mode)
        except (EnvironmentError, SystemError):
            if (os.name=="posix") and not os.path.isdir(fn):
                #Used for HFS+ on some platform(s)
                return open(fn+"/rsrc", *mode)
            raise
    else:
        return openrf(fn, *mode)

