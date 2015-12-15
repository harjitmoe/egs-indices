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

import binascii,sys,urllib
import utility
reallyspaced="<hr /><hr style='page-break-before:always;' />"

#so as to pass JSON to eval
null=None
false=False
true=True

def get_section(record):
    map={"Story":1,"EGS:NP":2,"Sketchbook":3,"Backgrounds":4}
    if record["RecordType"]=="Comic":
        return map[record["Section"]]
    elif record["RecordType"]=="StoryLine":
        return map[record["Comics"][0]["Section"]]
    elif record["RecordType"]=="StoryArc":
        return map[record["StoryLines"][0]["Comics"][0]["Section"]]
    elif record["RecordType"]=="Section":
        return map[record["Title"]]

def get_comid(record):
    if record["Id"]>0:#i.e. not an error code
        return `record["Id"]`
    else:
        return record["Date"]

def get_id(record):
    if record["RecordType"]=="Comic":
        return "section%d"%(get_section(record))+"strip"+get_comid(record)
    elif record["RecordType"]=="StoryLine":
        return "linestarting"+record["Comics"][0]["Section"]+get_id(record["Comics"][0])
    elif record["RecordType"]=="StoryArc":
        return "arcstarting"+record["StoryLines"][0]["Comics"][0]["Section"]+get_id(record["StoryLines"][0]["Comics"][0])
    elif record["RecordType"]=="Section":
        no={"Story":1,"EGS:NP":2,"Sketchbook":3,"Backgrounds":4}[record["Title"]]
        return "section%d"%no
    elif record["RecordType"]=="Database":
        return "topmenu"

def get_couplet(record):
    if record["RecordType"]=="Comic":
        return get_id(record),utility.get_preferred_title(record)
    elif record["RecordType"]=="StoryLine":
        return get_id(record),utility.clean(record["Title"])
    elif record["RecordType"]=="StoryArc":
        return get_id(record),utility.clean(record["Title"])
    elif record["RecordType"]=="Section":
        return get_id(record),utility.clean(record["Title"])
    elif record["RecordType"]=="Database":
        return get_id(record),"Table of Contents:"

def output_html(record,parent=None):
    if record["RecordType"]=="Database":
        print "<p style='margin: 0 0 1ex 0'><a id='%s'>(anchor)</a></p><h1 style='margin: 0 0 1ex 0'>%s</h1><ol>"%get_couplet(record)
        for section in record["Sections"]:
            print "<li><a href='#%s'>%s</a></li>"%get_couplet(section)
        print "<li><a href='#end'>End of document</a></li></ol>"
        for section in record["Sections"]:
            output_html(section,record)
    elif record["RecordType"]=="Section":
        print reallyspaced
        print "<p style='margin: 0 0 1ex 0'><a id='%s'>(anchor)</a></p><h1 style='margin: 0 0 1ex 0'>%s</h1>"%get_couplet(record)
        print "<p style='margin: 0 0 1ex 0'><a href='#%s'>(up one level)</a></p>"%get_id(parent)
        if "Id" not in record["StoryArcs"][0]:
            #Usual
            print "<ol>"
            for arc in record["StoryArcs"]:
                print "<li><a href='#%s'>%s</a></li>"%get_couplet(arc)
            print "</ol>"
        else:
            #Legacy Backgrounds
            print "<ul>"
            for arc in record["StoryArcs"]:
                print ("<li><a href='#%s'>" + ("%04d"%arc["Id"]) + ": %s</a></li>")%get_couplet(arc)
            print "</ul>"
        for arc in record["StoryArcs"]:
            output_html(arc,record)
    elif record["RecordType"]=="StoryArc":
        print reallyspaced
        print "<p style='margin: 0 0 1ex 0'><a id='%s'>(anchor)</a></p><h2 style='margin: 0 0 1ex 0'>%s</h2>"%get_couplet(record)
        print "<p style='margin: 0 0 1ex 0'><a href='#%s'>(up one level)</a></p><ol>"%get_id(parent)
        for line in record["StoryLines"]:
            print "<li><a href='#%s'>%s</a></li>"%get_couplet(line)
        print "</ol>"
        for line in record["StoryLines"]:
            output_html(line,record)
    elif record["RecordType"]=="StoryLine":
        print reallyspaced
        print "<p style='margin: 0 0 1ex 0'><a id='%s'>(anchor)</a></p><h3 style='margin: 0 0 1ex 0'>%s</h3>"%get_couplet(record)
        print "<p style='margin: 0 0 1ex 0'><a href='#%s'>(up one level)</a></p><ul>"%get_id(parent)
        reul_counter=0
        for comic in record["Comics"]:
            print "<li><a href='#"+get_id(comic)+"'>"+comic["Date"]+": "+get_comid(comic)+": "+utility.get_preferred_title(comic)+"</a></li>"
            #Back-buttoning onto middle of list causes all to appear unbulleted on one line
            #Contain damage by splitting ul into chunks (also why I'm using ul, not ol)
            if reul_counter>=100:
                print "</ul><ul>"
                reul_counter=0
            else:
                reul_counter+=1
        print "</ul>"
        for comic in record["Comics"]:
            output_html(comic,record)
    elif record["RecordType"]=="Comic":
        print reallyspaced
        comic=record
        print "<p style='margin: 0 0 1ex 0'><a id='"+get_id(comic)+"'>(anchor)</a></p><h4 style='margin: 0 0 1ex 0'>"+utility.get_preferred_title(comic)+"</h4>"
        print "<p style='margin: 0 0 1ex 0'><a href='#"+get_id(parent)+"'>(up one level)</a></p>"
        if comic["DateIndexable"]:
            print "<p style='margin: 0 0 1ex 0'>Date: <a href='http://egscomics.com/"+utility.ookii2url[comic["Section"]]+"?date="+comic["Date"]+"'>"+comic["Date"]+"</a></p>"
        else:
            print "<p style='margin: 0 0 1ex 0'>Date: "+comic["Date"]
            if comic['SharedDateIndex']:
                print "(%d of %d)"%(comic['SharedDateIndex'],(comic['SharedDateTotal'][0] if 'SharedDateTotal' in comic else -1))
            print "</p>"
        if "DateInBrowserTitle" in comic:
            if comic["DateInBrowserTitle"]:
                print "<p style='margin: 0 0 1ex 0'>Date given in browser title: "+comic["DateInBrowserTitle"]+"</p>"
            else:
                print "<p style='margin: 0 0 1ex 0'>No date given in browser title.</p>"
            if comic["DateStatedAboveComic"]:
                print "<p style='margin: 0 0 1ex 0'>Date stated above the comic, converted to ISO format: "+comic["DateStatedAboveComic"]+"</p>"
            else:
                print "<p style='margin: 0 0 1ex 0'>No date stated above the comic.</p>"
        if ("SpecialUrl" in comic.keys()) and comic["SpecialUrl"]:
            special_website=comic["SpecialUrl"]
            if special_website.startswith("http://"):
                special_website=special_website.split("://",1)[1]
            special_website=special_website.split("/")[0]
            if comic["Id"]>0:#i.e. not an error code
                print "<p style='margin: 0 0 1ex 0'>Archival ID: "+comic["Section"]+" "+`comic["Id"]`+"</p>"
            print "<p style='margin: 0 0 1ex 0'>Unfortunately absent from current archives, or at least the interface thereof, possibly for technical reasons.  Accessible over "+special_website+" <a href='"+comic["SpecialUrl"]+"'>here</a>.</p>"
        elif comic["Id"]>0:#i.e. not an error code
            print "<p style='margin: 0 0 1ex 0'>Archival ID: <a href='http://egscomics.com/"+{"Story":"index.php","EGS:NP":"egsnp.php","Sketchbook":"sketchbook.php"}[comic["Section"]]+"?id="+`comic["Id"]`+"'>"+comic["Section"]+" "+`comic["Id"]`+"</a></p>"
        else:
            print "<p style='margin: 0 0 1ex 0'>Unable to determine archival ID.  Lookup by date may or may not work.</p>"
        if comic["OokiiId"]>0:
            print "<p style='margin: 0 0 1ex 0'>Ookii database ID: "+`comic["OokiiId"]`+"</p>"
        else:
            print "<p style='margin: 0 0 1ex 0'>Not in Ookii database as of time of grab.</p>"
        if ("FileNameTitle" in comic.keys()) and comic["FileNameTitle"]:
            print "<p style='margin: 0 0 1ex 0'>Meaningful part of original filename: "+comic["FileNameTitle"]+"</p>"
        if comic['Characters']:
            for authority,chars in comic['Characters'].items():
                print "<h5 style='margin: 0 0 1ex 0'>Characters per "+authority+":</h5>"
                for ch in chars:
                    if 'CharacterForms' in ch:
                        print "<p style='margin: 0 0 1ex 0'>Appearance %d of %s in %s, appearing in form(s):"%(ch['AppearanceNumber'],ch['CharacterName'],comic["Section"])
                        print ", ".join(ch['CharacterForms'])
                        print "</p>"
                    else:
                        print "<p style='margin: 0 0 1ex 0'>Appearance %d of %s in %s</p>"%(ch['AppearanceNumber'],ch['CharacterName'],comic["Section"])
        else:
            print "<p style='margin: 0 0 1ex 0'>(Ookii character information unavailable)</p>"
        if ('Transcript' in comic.keys()) and comic['Transcript']:
            print "<h5 style='margin: 0 0 1ex 0'>Transcript: </h5>"
            ts=utility.clean(comic['Transcript']).strip("\n").replace("\n\n","</p><p style='margin: 0 0 1ex 0'>").replace("\n","<br />")
            print "<blockquote><p style='margin: 0 0 1ex 0'>"+ts+"</p></blockquote>"
        else:
            print "<p style='margin: 0 0 1ex 0'>(Transcript unavailable)</p>"
        if ('ReactionLinks' in comic.keys()) and comic['ReactionLinks']:
            print "<h5 style='margin: 0 0 1ex 0'>Reaction links: </h5>"
            for rl,classic in comic['ReactionLinks']:
                rl=rl.replace("&","&amp;") #XML parsing error?!
                print "<p style='margin: 0 0 1ex 0'><a href=%r>%s</a>%s</p>"%(rl,rl," (Classics Thread)" if classic else " (Original Thread)")
        else:
            if comic["Date"].startswith("2012-09-") or comic["Date"].startswith("2012-08-2") or comic["Date"].startswith("2012-08-3"):
                pass #"(Note: Threads lost in server crash)" -- Herald Loveall
            elif comic["Section"]=="Backgrounds":
                pass
            else:
                print>>sys.stderr,comic["Section"],comic["Date"]

sections=utility.open_alldat()
#HTML 5:
#print "<!doctype html>"
#print '<html><head><title>Index of EGS Strips</title><meta charset="UTF-8" /></head>'
#
#XHTML 1.1:
print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
print '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Index of EGS Strips</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>'
#
print "<body><h1 style='margin: 0 0 1ex 0'>Index of EGS Strips</h1>"
output_html({"Sections":sections,"RecordType":"Database"})
print reallyspaced
print "<a id='end'></a><h2 style='margin: 0 0 1ex 0'>End of document</h2>" #No, the sketchbook section is NOT footnotes!  This doesn't fix this, use of classic MOBI does IIRC.
print "<a href='#topmenu'>(back to top)</a><hr /></body></html>"
