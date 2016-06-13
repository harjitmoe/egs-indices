# Written in 2016 by Thomas Hori
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

docs="""<noinclude>{{templatenotice}}

This database template is the date-to-ID mapping for the [[%s]] section.

This is more reliable than using the site's own date-lookup functionality.  It can also be updated with more recent mappings, but is not updated automatically.

Dates with multiple postings in the same section take an additional hyphen and number (no leading zeroes) indicating which nth posting it is.  Otherwise, pass an ISO date (including hyphens).

The three templates are {{t|Date2Id-story}}, {{t|Date2Id-sketch}} and {{t|Date2Id-np}}.

</noinclude>"""

import utility, os

def export_dateidtemplate(alldat):
    print (">>> export_dateidtemplate")
    stdb=utility.specific_section(alldat,"story")["StoryArcs"]
    sbdb=utility.specific_section(alldat,"sketch")["StoryArcs"]
    npdb=utility.specific_section(alldat,"np")["StoryArcs"]
    ditst=open(".build/dateidtemplate-ST.txt","w")
    ditsb=open(".build/dateidtemplate-SB.txt","w")
    ditnp=open(".build/dateidtemplate-NP.txt","w")
    for outf,db,title in ((ditst,stdb,"Structural Nomenclature|Main Story"),(ditsb,sbdb,"Sketchbook"),(ditnp,npdb,"EGS:NP")):
        print>>outf,"<includeonly>{{#switch:{{{1}}}"
        for arc in db:
            for line in (arc["StoryLines"] if arc["RecordType"]=="StoryArc" else (arc,)):
                for comic in line["Comics"]:
                    date = comic["Date"]
                    if comic['SharedDateIndex']:
                        date+="-"+str(comic['SharedDateIndex'])
                    print>>outf, "|%s=%d"%(date, comic["Id"])
                    if comic['SharedDateIndex']:
                        print>>outf, "|%s of %s=%d"%(date, (comic['SharedDateTotal'][0] if 'SharedDateTotal' in comic else -1), comic["Id"])
        print>>outf, "}}</includeonly>"+(docs%title)
        outf.close()

if __name__=="__main__":
    alldat=utility.open_alldat()
    export_dateidtemplate(alldat)

