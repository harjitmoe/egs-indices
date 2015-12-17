# Written in 2015 by HarJIT
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

import sys,os
import utility

def doit(outfile,b):
    source="Official"
    print>>outfile, "|"+source.lower()+" = {{#switch:{{{3}}}",
    #Only, by date
    print>>outfile, "|date = {{#switch:{{{4}}}-{{{5}}}-{{{6}}}"
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if not comic["SharedDateIndex"]:
                    if source in comic["Titles"]:
                        print>>outfile, "|"+comic["Date"]+' = ("'+utility.clean(comic["Titles"][source])+'")'
    print>>outfile, "|#default = }}"
    #Only, by ID
    print>>outfile, "|id = {{#switch:{{{4}}}"
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if comic["Id"]!=-1:
                    if source in comic["Titles"]:
                        print>>outfile, "|"+`comic["Id"]`+' = ("'+utility.clean(comic["Titles"][source])+'")'
    print>>outfile, "|#default = }}"
    print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{3}}}' (only official supported in this version)</span>}}"

alldat=utility.open_alldat()
outfile=open(".build/titles_lite.txt","w")

print>>outfile, "<includeonly>{{#switch:{{{1}}}"

for sect in ("story","sketch","np"):
    b=utility.specific_section(alldat,sect)["StoryArcs"]
    print>>outfile, "|%s={{#switch:{{{2}}}"%sect
    doit(outfile,b)
    print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported authority scheme '{{{2}}}'</span>}}"

f=open("BgNames.txt","rU")
b=eval(f.read()) #Blatantly no security, assume trust
f.close()
print>>outfile, "|bg={{#switch:{{{2}}}"
for id in b:
    print>>outfile, "|"+id+' = ("'+b[id]+'")'
print>>outfile, "|#default = }}"

print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>"
print>>outfile, """

== About ==

Generated template for obtaining strip titles from dates or IDs.  

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

