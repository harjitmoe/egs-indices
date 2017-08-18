# Written in 2015,2017 by Thomas Hori
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

import sys,os,yaml
import utility

def doit(outfile,b):
    source="Official"
    print("|"+source.lower()+" = {{#switch:{{{3}}}", end=' ', file=outfile)
    #Only, by date
    print("|date = {{#switch:{{{4}}}-{{{5}}}-{{{6}}}", file=outfile)
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if not comic["SharedDateIndex"]:
                    if source in comic["Titles"]:
                        print("|"+comic["Date"]+' = '+utility.entity_escape(comic["Titles"][source]), file=outfile)
    print("|#default = }}", file=outfile)
    #Only, by ID
    print("|id = {{#switch:{{{4}}}", file=outfile)
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if comic["Id"]!=-1:
                    if source in comic["Titles"]:
                        print("|"+repr(comic["Id"])+' = '+utility.entity_escape(comic["Titles"][source]), file=outfile)
    print("|#default = }}", file=outfile)
    print("|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{3}}}'</span>}}", file=outfile)

def export_titles_template_lite2(alldat):
    print (">>> export_titles_template_lite2")
    outfile=open(".build/titles_lite2.txt","w")
    print("<includeonly>{{#switch:{{{1}}}", file=outfile)
    for sect in ("story","sketch","np"):
        b=utility.specific_section(alldat,sect)["StoryArcs"]
        print("|%s={{#switch:{{{2}}}"%sect, file=outfile)
        doit(outfile,b)
        print("|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported authority scheme '{{{2}}}' (only official supported in this version)</span>}}", file=outfile)
    f=open("BgNames.txt","rU")
    b=yaml.safe_load(f)
    f.close()
    print("|bg={{#switch:{{{2}}}", file=outfile)
    for id in sorted(b.keys()):
        print("|"+id+' = '+b[id], file=outfile)
    print("|#default = }}", file=outfile)
    print("|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>", file=outfile)
    print(docs, file=outfile)
    outfile.close() #IronPython grumble grumble

if __name__=="__main__":
    alldat=utility.open_alldat()
    export_titles_template_lite2(alldat)

