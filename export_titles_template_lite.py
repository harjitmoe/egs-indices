# Written in 2015,2017 by HarJIT
#
# This file is made available under the CC0 Public Domain Dedication.  To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this file to the public domain worldwide. This file is distributed without any warranty.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
#
# -----------------------------------------------------------------
#
# Note: the above notice applies to this file specifically.  Other files may use
# different terms.  This note is not part of the above notice.
#

docs="""

== About ==

{{templatenotice}}

Gene""" """rated template for obtaining strip titles from dates or IDs.  

Official titles are mostly identified in and weeded out from the Ookii or Haylo databases.  Some of these represent titles on the strips themselves, others represent official titles which may remain on egscomics.com in the commentary section, '''or which may have been originally from the official site but lost, apparently in the move to 910CMX'''.  Some newer official titles have been identified and added; amongst the newer titles, some were isolated from the HTML browser (tab) titles.  Previous Summer Moments are recovered from the strips themselves.    

The bg titles were scoured by HarJIT from various revisions in the Wayback Machine (each given page covered a different span in different revisions due to the wallpapers being listed latest-first, so in some cases multiple revisions of the same page were needed for to cumulatively cover the entire span).

== Usage ==

First parameter is the type (story, sketch, np or bg).

For bg, the only other parameter is the 4-digit integer ID, counting from 0000.

For the others, the second parameter is the "authority scheme", which must be "official" (without the quotes).  Earlier versions supported more authority schemes which were never used, which bloated the template enormously, and which are not included by the branch of the code used to generate this version.

The third is either "date" or "id" depending on what is being passed in.  The subsequent parameters are:

* For date, year (4-digit), month (2-digit) and day (2-digit) in that order.
* For id, the comic ID with no leading zeroes (in contrast to the bg scheme).

[[Category:General wiki templates]]
</noinclude>
"""

docs_date="""

== About ==

{{templatenotice}}

Gene""" """rated template for obtaining strip titles from dates.  

Official titles are mostly identified in and weeded out from the Ookii or Haylo databases.  Some of these represent titles on the strips themselves, others represent official titles which may remain on egscomics.com in the commentary section, '''or which may have been originally from the official site but lost, apparently in the move to 910CMX'''.  Some newer official titles have been identified and added; amongst the newer titles, some were isolated from the HTML browser (tab) titles.  Previous Summer Moments are recovered from the strips themselves.

== Usage ==

First parameter is the type (story, sketch, np).

The subsequent parameters are year (4-digit), month (2-digit) and day (2-digit) in that order.

[[Category:General wiki templates]]
</noinclude>
"""

docs_id="""

== About ==

{{templatenotice}}

Gene""" """rated template for obtaining strip titles from EGSComics IDs.  

Official titles are mostly identified in and weeded out from the Ookii or Haylo databases.  Some of these represent titles on the strips themselves, others represent official titles which may remain on egscomics.com in the commentary section, '''or which may have been originally from the official site but lost, apparently in the move to 910CMX'''.  Some newer official titles have been identified and added; amongst the newer titles, some were isolated from the HTML browser (tab) titles.  Previous Summer Moments are recovered from the strips themselves.    

== Usage ==

First parameter is the type (story, sketch, np or bg).  Second parameter is the comic ID with no leading zeroes.

[[Category:General wiki templates]]
</noinclude>
"""

docs_bg="""

== About ==

{{templatenotice}}

Gene""" """rated template for obtaining legacy background titles from four-digit IDs.  

The bg titles were scoured by HarJIT from various revisions in the Wayback Machine (each given page covered a different span in different revisions due to the wallpapers being listed latest-first, so in some cases multiple revisions of the same page were needed for to cumulatively cover the entire span).

== Usage ==

The only parameter is the 4-digit integer ID, counting from 0000 inclusive.

[[Category:General wiki templates]]
</noinclude>
"""

import sys,os,json
import utility

def doit_date(outfile,b,shuffle=0):
    source="Official"
    #Only, by date
    print("{{#switch:{{{%d}}}-{{{%d}}}-{{{%d}}}"%(4+shuffle,5+shuffle,6+shuffle), file=outfile)
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if not comic["SharedDateIndex"]:
                    if source in comic["Titles"]:
                        print("|"+comic["Date"]+' = '+utility.entity_escape(comic["Titles"][source]), file=outfile)
    print("|#default = }}", file=outfile)

def doit_id(outfile,b,shuffle=0):
    source="Official"
    #Only, by ID
    print("{{#switch:{{{%d}}}"%(4+shuffle,), file=outfile)
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if comic["Id"]!=-1:
                    if source in comic["Titles"]:
                        print("|"+repr(comic["Id"])+' = '+utility.entity_escape(comic["Titles"][source]), file=outfile)
    print("|#default = }}", file=outfile)

def doit(outfile,b,shuffle=0):
    print("{{#switch:{{{%d}}}"%(3+shuffle,), end=' ', file=outfile)
    #Only, by date
    print("|date =", end=' ', file=outfile)
    doit_date(outfile, b, shuffle)
    #Only, by ID
    print("|id =", end=' ', file=outfile)
    doit_id(outfile, b, shuffle)
    print("|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{%d}}}'</span>}}"%(3+shuffle,), file=outfile)

def export_titles_template_lite(alldat):
    print (">>> export_titles_template_lite")
    outfile=open(".build/titles_lite2.txt","w")
    outfile_date=open(".build/titles_lite_date.txt","w")
    outfile_id=open(".build/titles_lite_id.txt","w")
    outfile_bg=open(".build/titles_lite_bg.txt","w")
    print("<includeonly>{{#switch:{{{1}}}", file=outfile)
    print("<includeonly>{{#switch:{{{1}}}", file=outfile_date)
    print("<includeonly>{{#switch:{{{1}}}", file=outfile_id)
    for sect in ("story","sketch","np"):
        b=utility.specific_section(alldat,sect)["StoryArcs"]
        print("|%s={{#switch:{{{2}}}"%sect, file=outfile)
        print("|official =", end=' ', file=outfile)
        doit(outfile,b)
        print("|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported authority scheme '{{{2}}}' (only official supported in this version)</span>}}", file=outfile)
        print(("|%s="%sect), end=' ', file=outfile_date)
        doit_date(outfile_date,b,-2)
        print(("|%s="%sect), end=' ', file=outfile_id)
        doit_id(outfile_id,b,-2)
    f=open("BgNames.txt","rU")
    b=json.load(f)
    f.close()
    print("|bg={{#switch:{{{2}}}", file=outfile)
    print("<includeonly>{{#switch:{{{1}}}", file=outfile_bg)
    for id in sorted(b.keys()):
        print("|"+id+' = '+b[id], file=outfile)
        print("|"+id+' = '+b[id], file=outfile_bg)
    print("|#default = }}</includeonly><noinclude>", file=outfile_bg)
    print("|#default = }}", file=outfile)
    print("|#default = <span class=\"error\">[[Template:EGS-title-dateid|EGS-title-dateid]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>", file=outfile_id)
    print("|#default = <span class=\"error\">[[Template:EGS-title-date|EGS-title-date]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>", file=outfile_date)
    print("|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>", file=outfile)
    print(docs, file=outfile)
    print(docs_date, file=outfile_date)
    print(docs_id, file=outfile_id)
    print(docs_bg, file=outfile_bg)
    tuple(i.close() for i in (outfile,outfile_date,outfile_id,outfile_bg)) #IronPython grumble grumble

if __name__=="__main__":
    alldat=utility.open_alldat()
    export_titles_template_lite2(alldat)

