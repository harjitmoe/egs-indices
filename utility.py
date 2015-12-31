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

import sys

####################################################################
##### Support for the current incarnation of the Script System #####

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

####################################
##### Date/calendar processing #####

import calendar
_iso2top={}
def month2number(month):
    #Just a TAD NEUROTIC?
    if month[:3]=="Qui": month="Jul" #Quinctilis=July
    if month[:3]=="Sex": month="Aug" #Sextilis=August
    return "%02d"%[None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(month[:3])
def number2month(month):
    return [None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(month)]
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
        wd="Comic for "+calendar.weekday(y,m,d)
        _iso2top[iso]="%s, %s %d, %04d"%(wd,m2,d,y)
    return _iso2top[iso]
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

##################################################
##### Conversion between HTML and plain text #####

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
def deentity(data,mode=0):
    # The level of overhead which results from inefficiencies in this function is phenomenal.
    from htmlentitydefs import name2codepoint,codepoint2name
    #
    # 0: Fast, 1: Comprehensive, 2: Syntax-critical only, 3: Whole-file mode (skip syntax-critical)
    data=data.decode("utf-8")
    if mode==0:
        foci=(u'lt', u'gt', u'quot', u'nbsp', u'lsquo', u'rsquo', u'ldquo', u'rdquo', u'ndash', u'hellip')
    elif mode in (1,3):
        foci=name2codepoint.keys()
    elif mode==2:
        foci=(u'lt',u'gt')
    for name in foci:
        if name!=u"amp":
            if (mode!=3) or (name not in (u'lt',u'gt')):
                data=data.replace(u"&"+name+u";",unichr(name2codepoint[name]))
    if mode in (0,2):
        data=data.replace(u"&#39;",unichr(39))
    elif mode in (1,3):
        for number in range(0x100):
            name=u"#"+str(number).decode("latin1")
            data=data.replace(u"&"+name+u";",unichr(number))
    if mode!=3:
        data=data.replace(u"&amp;",u"&")
    return data.encode("utf-8")
def entity_escape(data):
    # The level of overhead which results from inefficiencies in this function is phenomenal.
    from htmlentitydefs import name2codepoint,codepoint2name
    data=data.decode("utf-8").replace(u"&",u"&amp;")
    for name in (u'lt', u'gt', u'quot', u'nbsp', u'lsquo', u'rsquo', u'ldquo', u'rdquo', u'ndash', u'hellip'):
        data=data.replace(unichr(name2codepoint[name]),u"&"+name+u";")
    return data.encode("utf-8")

##############################################
##### Reaction link duplicity regulation #####

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
def merge_reactions(a,b):
    a1=[i[0] for i in a]
    for i in b:
        if i[0] not in a1:
            a.append(i)

############################
##### Title processing #####

#In order of preference (best first)
title_sources=("Official","DeviantArt","Tumblr","Haylo","Ookii","Zorua","HarJIT","Reddit")
prefers=("Ookii","Haylo","Zorua")
def get_every_sane_title(comic):
    value=[]
    for ttype in title_sources:
        if ttype in comic["Titles"]:
            if comic["Titles"][ttype]:
                value.append(comic["Titles"][ttype]+" ("+ttype+")")
    return entity_escape((" / ".join(value)) or "")
def get_title_aggregate(comic):
    value=[]
    for ttype in title_sources:
        if ttype in comic["Titles"]:
            if comic["Titles"][ttype]:
                value.append(comic["Titles"][ttype]+" ("+ttype+")")
    if (not value) and comic["Titles"]:
        value.extend([i[1]+" ("+i[0]+")" for i in comic["Titles"].items()])
    return entity_escape((" / ".join(value)) or "Untitled.")
def get_title_preferring(comic,pref):
    for ttype in (pref,)+title_sources:
        if ttype in comic["Titles"]:
            return entity_escape(comic["Titles"][ttype])
    if comic["Titles"]:
        return entity_escape(comic["Titles"][comic["Titles"].keys()[0]])
    return "Untitled."
def alphabetical_id(string):
    return tuple(filter(lambda i:i in "qwertyuiopasdfghjklzxcvbnm",string.lower()))

#### Unsorted:

#"Backgrounds" is an extension used by megadb_pull_bg
egslink2ookii={"story":"Story","sketch":"Sketchbook","np":"EGS:NP","bg":"Backgrounds"}
ookii2egslink=dict(zip(*zip(*egslink2ookii.items())[::-1]))
ookii2url={"Story":"index.php","EGS:NP":"egsnp.php","Sketchbook":"sketchbook.php"}

def specific_section(whole,sect):
    for section in whole:
        if section["Title"]==egslink2ookii[sect]:
            return section
    raise IndexError,"section %r not in db"%sect

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

