# Written in 2015 by Thomas Hori
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

import sys,os
import utility

def doit_date(outfile,b,shuffle=0):
    source="Official"
    #Only, by date
    print>>outfile, "{{#switch:{{{%d}}}-{{{%d}}}-{{{%d}}}"%(4+shuffle,5+shuffle,6+shuffle)
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if not comic["SharedDateIndex"]:
                    if source in comic["Titles"]:
                        print>>outfile, "|"+comic["Date"]+' = '+utility.entity_escape(comic["Titles"][source])
    print>>outfile, "|#default = }}"

def doit_id(outfile,b,shuffle=0):
    source="Official"
    #Only, by ID
    print>>outfile, "{{#switch:{{{%d}}}"%(4+shuffle,)
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if comic["Id"]!=-1:
                    if source in comic["Titles"]:
                        print>>outfile, "|"+`comic["Id"]`+' = '+utility.entity_escape(comic["Titles"][source])
    print>>outfile, "|#default = }}"

def doit(outfile,b,shuffle=0):
    print>>outfile, "{{#switch:{{{%d}}}"%(3+shuffle,),
    #Only, by date
    print>>outfile, "|date =",
    doit_date(outfile, b, shuffle)
    #Only, by ID
    print>>outfile, "|id =",
    doit_id(outfile, b, shuffle)
    print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{%d}}}'</span>}}"%(3+shuffle,)

def export_titles_template_lite(alldat):
    print (">>> export_titles_template_lite")
    outfile=open(".build/titles_lite2.txt","w")
    outfile_date=open(".build/titles_lite_date.txt","w")
    outfile_id=open(".build/titles_lite_id.txt","w")
    outfile_bg=open(".build/titles_lite_bg.txt","w")
    print>>outfile, "<includeonly>{{#switch:{{{1}}}"
    print>>outfile_date, "<includeonly>{{#switch:{{{1}}}"
    print>>outfile_id, "<includeonly>{{#switch:{{{1}}}"
    for sect in ("story","sketch","np"):
        b=utility.specific_section(alldat,sect)["StoryArcs"]
        print>>outfile, "|%s={{#switch:{{{2}}}"%sect
        print>>outfile, "|official =",
        doit(outfile,b)
        print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported authority scheme '{{{2}}}' (only official supported in this version)</span>}}"
        print>>outfile_date, ("|%s="%sect),
        doit_date(outfile_date,b,-2)
        print>>outfile_id, ("|%s="%sect),
        doit_id(outfile_id,b,-2)
    f=open("BgNames.txt","rU")
    b=eval(f.read()) #Blatantly no security, assume trust
    f.close()
    print>>outfile, "|bg={{#switch:{{{2}}}"
    print>>outfile_bg, "<includeonly>{{#switch:{{{1}}}"
    for id in sorted(b.keys()):
        print>>outfile, "|"+id+' = '+b[id]
        print>>outfile_bg, "|"+id+' = '+b[id]
    print>>outfile_bg, "|#default = }}</includeonly><noinclude>"
    print>>outfile, "|#default = }}"
    print>>outfile_id, "|#default = <span class=\"error\">[[Template:EGS-title-dateid|EGS-title-dateid]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>"
    print>>outfile_date, "|#default = <span class=\"error\">[[Template:EGS-title-date|EGS-title-date]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>"
    print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>"
    print>>outfile, docs
    print>>outfile_date, docs_date
    print>>outfile_id, docs_id
    print>>outfile_bg, docs_bg
    tuple(i.close() for i in (outfile,outfile_date,outfile_id,outfile_bg)) #IronPython grumble grumble

if __name__=="__main__":
    alldat=utility.open_alldat()
    export_titles_template_lite2(alldat)

