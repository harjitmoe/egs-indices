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

docs="""

== About ==

{{templatenotice}}

Gene""" """rated template for obtaining strip titles from dates or IDs.  

Official titles are mostly identified in and weeded out from the Ookii or Haylo databases.  Some of these represent titles on the strips themselves, others represent official titles which may remain on egscomics.com in the commentary section, '''or which may have been originally from the official site but lost, apparently in the move to 910CMX'''.  Some newer official titles have been identified and added; amongst the newer titles, some were isolated from the HTML browser (tab) titles.  Previous Summer Moments are recovered from the strips themselves.    

The bg titles were scoured by HarJIT from various revisions in the Wayback Machine (each given page covered a different span in different revisions due to the wallpapers being listed latest-first, so in some cases multiple revisions of the same page were needed for to cumulatively cover the entire span).

When not invoked in the official mode, some titles may be ones written by Haylo, Unforgiven (Ookii), Zorua, HarJIT or (attributed) Reddit users.  A few are even select captions quoted from Dan's Tumblr.  Or titles given to postings of them on Dan's DeviantArt (I'm being cautious and not labelling them as official nonetheless).

== Usage ==

First parameter is the type (story, sketch, np or bg).

For bg, the only other parameter is the 4-digit integer ID, counting from 0000.

For the others, the second parameter is the "authority scheme", of which the following are the most likely to be used:

* official
* composite
* prefer_haylo
* prefer_ookii
* prefer_zorua

The "official" scheme will only return official titles.  The "composite" scheme will return whatever it has.  Where both are available, the "prefer_haylo" (only makes sense on main story) and "prefer_zorua" (only makes sense on EGS:NP) scheme will prefer Haylo's or Zorua's titles respectively, and the "prefer_ookii" scheme will prefer Unforgiven's.  The "prefer_" prefix may be omitted, but there is rarely any logical reason to do so, especially as that would exclude official titles.

Less likely to be used, and therefore without "prefer_" versions due to template size concerns:

* deviantart
* harjit
* reddit
* tumblr

The third is either "date" or "id" depending on what is being passed in.  The subsequent parameters are:

* For date, year (4-digit), month (2-digit) and day (2-digit) in that order.
* For id, the comic ID with no leading zeroes (in contrast to the bg scheme).

[[Category:General wiki templates]]
</noinclude>
"""

import sys,os
import utility

def doit(outfile,b):
    print>>outfile, "|composite = {{#switch:{{{3}}}",
    #Composite, by date
    print>>outfile, "|date = {{#switch:{{{4}}}-{{{5}}}-{{{6}}}"
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if not comic["SharedDateIndex"]:
                    print>>outfile, "|"+comic["Date"]+' = ("'+utility.get_every_sane_title(comic)+'")'
    print>>outfile, "|#default = }}"
    #Composite, by ID
    print>>outfile, "|id = {{#switch:{{{4}}}"
    for arc in b:
        for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
            for comic in line["Comics"]:
                if comic["Id"]!=-1:
                    print>>outfile, "|"+`comic["Id"]`+' = ("'+utility.get_every_sane_title(comic)+'")'
    print>>outfile, "|#default = }}"
    print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{3}}}'</span>}}"
    for source in utility.title_sources:
        #Only
        print>>outfile, "|"+source.lower()+" = {{#switch:{{{3}}}",
        #Only, by date
        print>>outfile, "|date = {{#switch:{{{4}}}-{{{5}}}-{{{6}}}"
        for arc in b:
            for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
                for comic in line["Comics"]:
                    if not comic["SharedDateIndex"]:
                        if source in comic["Titles"]:
                            print>>outfile, "|"+comic["Date"]+' = ("'+utility.entity_escape(comic["Titles"][source])+'")'
        print>>outfile, "|#default = }}"
        #Only, by ID
        print>>outfile, "|id = {{#switch:{{{4}}}"
        for arc in b:
            for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
                for comic in line["Comics"]:
                    if comic["Id"]!=-1:
                        if source in comic["Titles"]:
                            print>>outfile, "|"+`comic["Id"]`+' = ("'+utility.entity_escape(comic["Titles"][source])+'")'
        print>>outfile, "|#default = }}"
        print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{3}}}'</span>}}"
        if source in utility.prefers: #Limit size of template
            #Preferred
            print>>outfile, "|prefer_"+source.lower()+" = {{#switch:{{{3}}}",
            #Preferred, by date
            print>>outfile, "|date = {{#switch:{{{4}}}-{{{5}}}-{{{6}}}"
            for arc in b:
                for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
                    for comic in line["Comics"]:
                        if not comic["SharedDateIndex"]:
                            print>>outfile, "|"+comic["Date"]+' = ("'+utility.get_title_preferring(comic,source)+'")'
            print>>outfile, "|#default = }}"
            #Preferred, by ID
            print>>outfile, "|id = {{#switch:{{{4}}}"
            for arc in b:
                for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
                    for comic in line["Comics"]:
                        if comic["Id"]!=-1:
                            print>>outfile, "|"+`comic["Id"]`+' = ("'+utility.get_title_preferring(comic,source)+'")'
            print>>outfile, "|#default = }}"
            print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported lookup scheme '{{{3}}}'</span>}}"

def export_titles_template(alldat):
    print (">>> export_titles_template")
    outfile=open(".build/titles.txt","w")
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
    for id in sorted(b.keys()):
        print>>outfile, "|"+id+' = ("'+b[id]+'")'
    print>>outfile, "|#default = }}"
    print>>outfile, "|#default = <span class=\"error\">[[Template:EGS-title|EGS-title]]: Unsupported comic type '{{{1}}}'</span>}}</includeonly><noinclude>"
    print>>outfile, docs
    outfile.close() #IronPython grumble grumble

if __name__=="__main__":
    alldat=utility.open_alldat()
    export_titles_template(alldat)

