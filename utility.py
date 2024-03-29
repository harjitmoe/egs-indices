# Copyright (c) HarJIT 2015, 2016, 2017, 2019.
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

####################################
##### Date/calendar processing #####

import calendar
_iso2top = {}


def month2number(month):
    """Convert a month name to a number."""
    #Slightly excessive?
    if month[:3] == "Qui": month = "Jul"  #Quinctilis=July
    if month[:3] == "Sex": month = "Aug"  #Sextilis=August
    return "%02d" % [
        None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
    ].index(month[:3])


def number2month(month):
    """Convert a month number to a three-character name."""
    return [
        None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
    ][int(month)]


def top2iso(top):
    """Convert the date format used above comics on the EGS website to ISO format."""
    wd, md, y = top.split(", ")
    m, d = md.split()
    d = "%02d" % int(d)
    m = month2number(m)
    iso = y + "-" + m + "-" + d
    if iso not in _iso2top:
        _iso2top[iso] = top
    return iso


def iso2top(iso):
    if iso not in _iso2top:
        y, m, d = iso.split("-")
        m = int(m, 10)
        m2 = number2month(m)[:3]
        d = int(d, 10)
        y = int(y)
        wd = "Comic for " + calendar.weekday(y, m, d)
        _iso2top[iso] = "%s, %s %d, %04d" % (wd, m2, d, y)
    return _iso2top[iso]


def datefix_910(date, sect):
    """Fix dates of 910 threads to match database in cases 
    where precise date is disputable."""
    # Much of this was written during a 910 outage.
    # ~~Much of this is in need of verification.~~ Moot now.
    if date == "2012-03-29" and sect == "story":
        return "2013-03-29"  #Confirmed
    if date == "2013-08-04" and sect == "story":  #Amended (was correcting from 2012)
        return "2013-08-05"  #Confirmed
    if date == "2012-08-12" and sect == "story":
        return "2012-08-13"  #Confirmed by Loveall
    if date == "2012-08-16" and sect == "story":
        return "2012-08-15"  #Confirmed
    if date == "2012-12-16" and sect == "story":
        return "2012-12-17"  #Confirmed
    if date == "2013-01-20" and sect == "story":
        return "2014-01-20"  #Fixed
    if date == "2015-08-05" and sect == "story":
        return "2015-08-04"  #Added
    if date == "2012-10-05" and sect == "sketch":
        return "2012-11-05"  #Added
    if date == "2012-10-06" and sect == "sketch":
        return "2012-11-06"  #Added
    if date == "2013-01-26" and sect == "sketch":
        return "2014-01-26"  #Added
    if date == "2013-02-15" and sect == "sketch":
        return "2014-02-15"  #Amended (was correcting to 2013-02-20)
    if date == "2015-01-16" and sect == "sketch":
        return "2015-01-15"  #Confirmed
    if date == "2014-12-07" and sect == "sketch":
        return "2014-12-08"
    if date == "2014-08-15" and sect == "np":
        return "2014-08-14"
    if date == "2014-08-20" and sect == "np":
        return "2014-08-19"
    if date == "2014-08-27" and sect == "np":
        return "2014-08-26"
    if date == "2015-01-14" and sect == "np":
        return "2015-01-15"
    if date == "2015-04-29" and sect == "np":
        return "2015-04-28"
    if date == "2015-07-17" and sect == "np":
        return "2015-07-16"
    return date


##################################################
##### Conversion between HTML and plain text #####


def detag(s):
    """Remove HTML tags from a string."""
    o = ""
    a = 1
    for c in s:
        if c == "<":
            a = 0
        elif c == ">":
            a = 1
        elif a:
            o += c
    assert a, "partial tag?"
    return o


def deentity(data, mode=0):
    """Remove HTML entities from a string.
    
    Modes:
    
    0: Fast / common entities only (default)
    1: Comprehensive (slow)
    2: Syntax-critical escapes only
    3: Whole-file mode (skip syntax-critical escapes)
    """
    # The level of overhead which results from inefficiencies in this function is phenomenal.
    # TODO: convert this entire function to do it properly or at least using a compiled regex.
    from html.entities import name2codepoint, codepoint2name
    #
    # 0: Fast, 1: Comprehensive, 2: Syntax-critical only, 3: Whole-file mode (skip syntax-critical)
    if mode == 0:
        foci = ('lt', 'gt', 'quot', 'nbsp', 'lsquo', 'rsquo', 'ldquo', 'rdquo',
                'ndash', 'hellip', 'eacute')
    elif mode in (1, 3):
        foci = list(name2codepoint.keys())
    elif mode == 2:
        foci = ('lt', 'gt')
    for name in foci:
        if name != "amp":
            if (mode != 3) or (name not in ('lt', 'gt')):
                data = data.replace("&" + name + ";",
                                    chr(name2codepoint[name]))
    if mode in (0, 2):
        data = data.replace("&#39;", chr(39))
    elif mode in (1, ):  #3):
        for number in range(0x100):
            name = "#" + str(number)
            data = data.replace("&" + name + ";", chr(number))
    if mode != 3:
        data = data.replace("&amp;", "&")
    return data


def entity_escape(data):
    """Encode the HTML entities used by deentity in Mode 0."""
    # The level of overhead which results from inefficiencies in this function is phenomenal.
    from html.entities import name2codepoint, codepoint2name
    data = data.replace("&", "&amp;")
    for name in ('lt', 'gt', 'quot', 'nbsp', 'lsquo', 'rsquo', 'ldquo',
                 'rdquo', 'ndash', 'hellip', 'eacute'):
        data = data.replace(chr(name2codepoint[name]), "&" + name + ";")
    return data


def recdeentity(obj, mode=0):
    """Remove HTML entities from a JSON-compatible object (modes same as deentity)."""
    if isinstance(obj, type({})):
        d = {}
        for k, v in list(obj.items()):
            d[recdeentity(k, mode=mode)] = recdeentity(v, mode=mode)
        return d
    elif isinstance(obj, type([])):
        return list(map(lambda ob, mode=mode: recdeentity(ob, mode=mode), obj))
    elif isinstance(obj, type(())):
        return tuple(map(lambda ob, mode=mode: recdeentity(ob, mode=mode),
                         obj))
    elif type(obj) == type(""):
        return deentity(obj, mode)
    else:
        return obj


##############################################
##### Reaction link duplicity regulation #####


def standardise910link(l):
    #http://community.910cmx.com/?showtopic=7761
    #http://community.910cmx.com/index.php?showtopic=7761
    #http://community.910cmx.com/?/topic/7761-np-february-19-2010/
    #http://community.910cmx.com/index.php?/topic/7761-np-february-19-2010/
    #http://community.910cmx.com/index.php?/topic/7761-np-february-19-2010/?view=getnewpost
    if l.startswith("http://community.910cmx.com/?/topic/"):
        l = l[len("http://community.910cmx.com/?/topic/"):].split("-")[0]
        l = "http://community.910cmx.com/?showtopic=" + l
    elif l.startswith("http://community.910cmx.com/index.php?/topic/"):
        l = l[len("http://community.910cmx.com/index.php?/topic/"):].split(
            "-")[0]
        l = "http://community.910cmx.com/?showtopic=" + l
    elif l.startswith("http://community.910cmx.com/index.php?showtopic="):
        l = l[len("http://community.910cmx.com/index.php?showtopic="):].split(
            "&")[0]
        l = "http://community.910cmx.com/?showtopic=" + l
    return l


def merge_reactions(a, b):
    a1 = [i[0] for i in a]
    for i in b:
        if i[0] not in a1:
            a.append(i)


############################
##### Title processing #####

#In order of preference (best first)
title_sources = ("Official", "DeviantArt", "Tumblr", "Reddit", "Haylo", "Ookii", "Zorua",
                 "HarJIT")
prefers = ("Ookii", "Haylo", "Zorua")


def get_every_sane_title(comic):
    value = []
    for ttype in title_sources:
        if ttype in comic["Titles"]:
            if comic["Titles"][ttype]:
                value.append(comic["Titles"][ttype] + " (" + ttype + ")")
    return entity_escape((" / ".join(value)) or "")


def get_title_aggregate(comic):
    value = []
    for ttype in title_sources:
        if ttype in comic["Titles"]:
            if comic["Titles"][ttype]:
                value.append(comic["Titles"][ttype] + " (" + ttype + ")")
    if (not value) and comic["Titles"]:
        value.extend(
            [i[1] + " (" + i[0] + ")" for i in list(comic["Titles"].items())])
    return entity_escape((" / ".join(value)) or "Untitled.")


def get_title_preferring(comic, pref):
    for ttype in (pref, ) + title_sources:
        if ttype in comic["Titles"]:
            return entity_escape(comic["Titles"][ttype])
    if comic["Titles"]:
        return entity_escape(comic["Titles"][list(comic["Titles"].keys())[0]])
    return "Untitled."


def alphabetical_id(string):
    return tuple(
        [i for i in string.lower() if i in "qwertyuiopasdfghjklzxcvbnm"])


#### Unsorted:

#"Backgrounds" is an extension used by megadb_pull_bg
egslink2ookii = {
    "story": "Story",
    "sketch": "Sketchbook",
    "np": "EGS:NP",
    "bg": "Backgrounds"
}
ookii2egslink = dict(list(zip(*list(zip(*list(egslink2ookii.items())))[::-1])))
ookii2url = {
    "Story": "index.php",
    "EGS:NP": "egsnp.php",
    "Sketchbook": "sketchbook.php"
}
ookii2url2018 = {
    "Story": "comics",
    "EGS:NP": "egsnp",
    "Sketchbook": "sketchbook"
}


def specific_section(whole, sect):
    """Index the database for a section by Shiveapedia code."""
    for section in whole:
        if section["Title"] == egslink2ookii[sect]:
            return section
    raise IndexError("section %r not in db" % sect)


def dates_index(strip, dateswork):
    strip["DateIndexable"] = False
    if strip["Id"] in dateswork:
        dsi = dateswork[strip["Id"]]
        for crit in ('WorksInternal', 'WorksExternal'):
            if crit in dsi:
                works, date = dsi[crit]
                if works and date:
                    if date != strip["Date"]:
                        print("%s %s" % (strip["Date"], date))
                        raise AssertionError
                    strip["DateIndexable"] = True


def identifier(strip):
    if strip["Id"] is not None:
        return strip["Id"]
    return "SLUG-" + strip["UrlSlug"]


def open_alldat():
    # Used when running / debugging exporters individually
    import json
    return json.load(open(".build/AllMegaDb.txt", "rU"))


def openrf(fn, *mode):
    import os
    try:
        from MacOS import openrf
    except ImportError:
        mode = list(mode)
        if mode:
            #MacOS.openrf allows and ignores asterisks.
            #One is passed by AppleSingle.py without explanation.
            #Ignore them likewise.
            mode[0] = mode[0].replace("*", "")
        try:
            #NTFS under Windows and others
            return open(fn + ":rsrc", *mode)
        except (EnvironmentError, SystemError):
            if (os.name == "posix") and not os.path.isdir(fn):
                #Used for HFS+ on some platform(s)
                return open(fn + "/rsrc", *mode)
            raise
    else:
        return openrf(fn, *mode)
