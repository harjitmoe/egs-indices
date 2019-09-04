# Copyright (c) HarJIT 2015, 2019.
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

import sys, utility

reallyspaced = "<hr /><hr style='page-break-before:always;' />"


def get_section(record):
    mapp = {"Story": 1, "EGS:NP": 2, "Sketchbook": 3, "Backgrounds": 4}
    if record["RecordType"] == "Comic":
        return mapp[record["Section"]]
    elif record["RecordType"] == "StoryLine":
        return mapp[record["Comics"][0]["Section"]]
    elif record["RecordType"] == "StoryArc":
        return mapp[record["StoryLines"][0]["Comics"][0]["Section"]]
    elif record["RecordType"] == "Section":
        return mapp[record["Title"]]


def get_comid(record):
    if record["Id"] is None and "UrlSlug" in record:
        return record["UrlSlug"]
    elif (record["Id"] is not None) and (record["Id"] >= 0):
        # i.e. not an error code (ID may be 0 in BG section)
        return repr(record["Id"])
    else:
        return record["Date"]


def get_id(record):
    if record["RecordType"] == "Comic":
        return "section%d" % (get_section(record)) + "strip" + get_comid(record)
    elif record["RecordType"] == "StoryLine":
        assert record["Comics"], record
        return "linestarting" + record["Comics"][0]["Section"] + get_id(record["Comics"][0])
    elif record["RecordType"] == "StoryArc":
        return ("arcstarting" + record["StoryLines"][0]["Comics"][0]["Section"] +
                get_id(record["StoryLines"][0]["Comics"][0]))
    elif record["RecordType"] == "Section":
        no = {
            "Story": 1,
            "EGS:NP": 2,
            "Sketchbook": 3,
            "Backgrounds": 4,
        }[record["Title"]]
        return "section%d" % no
    elif record["RecordType"] == "Database":
        return "topmenu"


def get_couplet(record):
    if record["RecordType"] == "Comic":
        return get_id(record), utility.get_title_aggregate(record)
    elif record["RecordType"] == "StoryLine":
        return get_id(record), utility.entity_escape(record["Title"])
    elif record["RecordType"] == "StoryArc":
        return get_id(record), utility.entity_escape(record["Title"])
    elif record["RecordType"] == "Section":
        return get_id(record), utility.entity_escape(record["Title"])
    elif record["RecordType"] == "Database":
        return get_id(record), "Table of Contents:"


HDR = ("<p style='margin: 0 0 1ex 0'><a id='{1}'>(anchor)</a></p>" + 
       "<h{0:d} style='margin: 0 0 1ex 0'>{2}</h{0:d}>")
UOL = ("<p style='margin: 0 0 1ex 0'><a href='#{}'>(up one level)</a></p>")
def output_html(outfile, record, parent=None):
    if record["RecordType"] == "Database":
        print(HDR.format(1, *get_couplet(record)) + "<ol>", file=outfile)
        for section in record["Sections"]:
            print("<li><a href='#%s'>%s</a></li>" % get_couplet(section), file=outfile)
        print("<li><a href='#end'>End of document</a></li></ol>", file=outfile)
        for section in record["Sections"]:
            output_html(outfile, section, record)
    elif record["RecordType"] == "Section":
        print(reallyspaced, file=outfile)
        print(HDR.format(1, *get_couplet(record)), file=outfile)
        print(UOL.format(get_id(parent)), file=outfile)
        if "Id" not in record["StoryArcs"][0]:
            #Usual
            print("<ol>", file=outfile)
            for arc in record["StoryArcs"]:
                print("<li><a href='#%s'>%s</a></li>" % get_couplet(arc), file=outfile)
            print("</ol>", file=outfile)
        else:
            #Legacy Backgrounds
            print("<ul>", file=outfile)
            for arc in record["StoryArcs"]:
                print(("<li><a href='#%s'>" +
                       ("%04d" % arc["Id"]) + ": %s</a></li>") %
                      get_couplet(arc),
                      file=outfile)
            print("</ul>", file=outfile)
        for arc in record["StoryArcs"]:
            output_html(outfile, arc, record)
    elif record["RecordType"] == "StoryArc":
        print(reallyspaced, file=outfile)
        print(HDR.format(2, *get_couplet(record)), file=outfile)
        print(UOL.format(get_id(parent)) + "<ol>", file=outfile)
        for line in record["StoryLines"]:
            print("<li><a href='#%s'>%s</a></li>" % get_couplet(line),
                  file=outfile)
        print("</ol>", file=outfile)
        for line in record["StoryLines"]:
            output_html(outfile, line, record)
    elif record["RecordType"] == "StoryLine":
        print(reallyspaced, file=outfile)
        print(HDR.format(3, *get_couplet(record)), file=outfile)
        print(UOL.format(get_id(parent)) + "<ul>", file=outfile)
        reul_counter = 0
        for comic in record["Comics"]:
            print("<li><a href='#" + get_id(comic) + "'>" + comic["Date"] +
                  ": " + get_comid(comic) + ": " +
                  utility.get_title_aggregate(comic) + "</a></li>",
                  file=outfile)
            #Back-buttoning onto middle of list causes all to appear unbulleted on one line
            #Contain damage by splitting ul into chunks (also why I'm using ul, not ol)
            # Note added 2019: I was referring above to behaviour of converted Kindle book form.
            if reul_counter >= 100:
                print("</ul><ul>", file=outfile)
                reul_counter = 0
            else:
                reul_counter += 1
        print("</ul>", file=outfile)
        for comic in record["Comics"]:
            output_html(outfile, comic, record)
    elif record["RecordType"] == "Comic":
        print(reallyspaced, file=outfile)
        comic = record
        print(HDR.format(4, *get_couplet(record)), file=outfile)
        print(UOL.format(get_id(parent)), file=outfile)
        #
        if "UrlSlug" in comic:
            print(
                "<p style='margin: 0 0 1ex 0'>URL Slug: <a href='http://egscomics.com/"
                + utility.ookii2url2018[comic["Section"]] + "/" +
                comic["UrlSlug"] + "'>" +
                utility.ookii2url2018[comic["Section"]] + "/" +
                comic["UrlSlug"] + "</a></p>",
                file=outfile)
        #
        if comic["DateIndexable"]:
            print(
                "<p style='margin: 0 0 1ex 0'>Date: <a href='http://egscomics.com/"
                + utility.ookii2url[comic["Section"]] + "?date=" +
                comic["Date"] + "'>" + comic["Date"] + "</a></p>",
                file=outfile)
        else:
            print("<p style='margin: 0 0 1ex 0'>Date: " + comic["Date"],
                  file=outfile)
            if comic['SharedDateIndex']:
                print("(%d of %d)" % (comic['SharedDateIndex'],
                                      (comic['SharedDateTotal'][0]
                                       if 'SharedDateTotal' in comic else -1)),
                      file=outfile)
            print("</p>", file=outfile)
        #
        if "DateInBrowserTitle" in comic:
            if comic["DateInBrowserTitle"]:
                print(
                    "<p style='margin: 0 0 1ex 0'>Date given in browser title: "
                    + comic["DateInBrowserTitle"] + "</p>",
                    file=outfile)
            else:
                print(
                    "<p style='margin: 0 0 1ex 0'>No date given in browser title.</p>",
                    file=outfile)
            if comic["DateStatedAboveComic"]:
                print(
                    "<p style='margin: 0 0 1ex 0'>Date stated above the comic, converted to ISO format: "
                    + comic["DateStatedAboveComic"] + "</p>",
                    file=outfile)
            else:
                print(
                    "<p style='margin: 0 0 1ex 0'>No date stated above the comic.</p>",
                    file=outfile)
        #
        if ("SpecialUrl" in comic) and comic["SpecialUrl"]:
            special_website = comic["SpecialUrl"]
            if special_website.startswith("http://"):
                special_website = special_website.split("://", 1)[1]
            special_website = special_website.split("/")[0]
            if (comic["Id"] is not None) and (comic["Id"] >= 0):
                # i.e. not an error code (will be zero for BG 0000)
                print("<p style='margin: 0 0 1ex 0'>Archival ID: " +
                      comic["Section"] + " " + repr(comic["Id"]) + "</p>",
                      file=outfile)
            print(
                "<p style='margin: 0 0 1ex 0'>Unfortunately absent from current archives, or at least the interface thereof, possibly for technical reasons.  Accessible over "
                + special_website + " <a href='" + comic["SpecialUrl"] +
                "'>here</a>.</p>",
                file=outfile)
        elif ("Id" in comic) and (comic["Id"] is not None) and (comic["Id"] >= 0):
            print(
                "<p style='margin: 0 0 1ex 0'>Archival ID: <a href='http://egscomics.com/"
                + utility.ookii2url[comic["Section"]] + "?id=" +
                repr(comic["Id"]) + "'>" + comic["Section"] + " " +
                repr(comic["Id"]) + "</a></p>",
                file=outfile)
        elif "UrlSlug" not in comic:
            print(
                "<p style='margin: 0 0 1ex 0'>Unable to determine archival ID or slug.  Lookup by date may or may not work.</p>",
                file=outfile)
        else:
            print(
                "<p style='margin: 0 0 1ex 0'>Unable to determine legacy archival ID, if it ever had one.</p>",
                file=outfile)
        #
        if comic["OokiiId"] > 0:
            print("<p style='margin: 0 0 1ex 0'>Ookii database ID: " +
                  repr(comic["OokiiId"]) + "</p>",
                  file=outfile)
        else:
            print(
                "<p style='margin: 0 0 1ex 0'>Not in Ookii database as of time of grab.</p>",
                file=outfile)
        #
        if ("FileNameTitle" in comic) and comic["FileNameTitle"]:
            print(
                "<p style='margin: 0 0 1ex 0'>Meaningful part of original filename: "
                + comic["FileNameTitle"] + "</p>",
                file=outfile)
        #
        if comic['Characters']:
            for authority in sorted(comic['Characters'].keys()):
                chars = comic['Characters'][authority]
                print("<h5 style='margin: 0 0 1ex 0'>Characters per " +
                      authority + ":</h5>",
                      file=outfile)
                for ch in chars:
                    if 'CharacterForms' in ch:
                        print(
                            "<p style='margin: 0 0 1ex 0'>Appearance %d of %s in %s, appearing in form(s):"
                            % (ch['AppearanceNumber'], ch['CharacterName'],
                               comic["Section"]),
                            file=outfile)
                        print(", ".join(ch['CharacterForms']), file=outfile)
                        print("</p>", file=outfile)
                    else:
                        print(
                            "<p style='margin: 0 0 1ex 0'>Appearance %d of %s in %s</p>"
                            % (ch['AppearanceNumber'], ch['CharacterName'],
                               comic["Section"]),
                            file=outfile)
        else:
            print(
                "<p style='margin: 0 0 1ex 0'>(Ookii character information unavailable)</p>",
                file=outfile)
        #
        if ('Transcript' in comic) and comic['Transcript']:
            print("<h5 style='margin: 0 0 1ex 0'>Transcript: </h5>",
                  file=outfile)
            ts = utility.entity_escape(
                comic['Transcript']).strip("\n").replace(
                    "\n\n", "</p><p style='margin: 0 0 1ex 0'>").replace(
                        "\n", "<br />")
            print("<blockquote><p style='margin: 0 0 1ex 0'>" + ts +
                  "</p></blockquote>",
                  file=outfile)
        else:
            print("<p style='margin: 0 0 1ex 0'>(Transcript unavailable)</p>",
                  file=outfile)
        #
        if ('ReactionLinks' in comic) and comic['ReactionLinks']:
            print("<h5 style='margin: 0 0 1ex 0'>Reaction links: </h5>",
                  file=outfile)
            for rl, classic in sorted(comic['ReactionLinks']):
                rl = utility.entity_escape(rl)  #XML parsing
                print("<p style='margin: 0 0 1ex 0'><a href=%r>%s</a>%s</p>" %
                      (rl, rl, " (Classics Thread)"
                       if classic else " (Original Thread)"),
                      file=outfile)
        else:
            if comic["Date"].startswith(
                    "2012-09-") or comic["Date"].startswith(
                        "2012-08-2") or comic["Date"].startswith("2012-08-3"):
                pass  #"(Note: Threads lost in server crash)" -- Herald Loveall
            elif comic["Section"] == "Backgrounds":
                pass
            else:
                print(comic["Section"], comic["Date"], file=sys.stderr)


def export_html(sections):
    print(">>> export_html")
    outfile = open(".build/index.html", "w")
    #HTML 5:
    #print>>outfile, "<!doctype html>"
    #print>>outfile, '<html><head><title>Index of EGS Strips</title><meta charset="UTF-8" /></head>'
    #
    #XHTML 5:
    #print>>outfile, '<!DOCTYPE html SYSTEM "about:legacy-compat">'
    #print>>outfile, '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Index of EGS Strips</title><meta charset="UTF-8" /></head>'
    #
    #XHTML 1.1:
    print(
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
        file=outfile)
    print(
        '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Index of EGS Strips</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>',
        file=outfile)
    #
    print("<body><h1 style='margin: 0 0 1ex 0'>Index of EGS Strips</h1>",
          file=outfile)
    output_html(outfile, {"Sections": sections, "RecordType": "Database"})
    print(reallyspaced, file=outfile)
    print(
        "<a id='end'></a><h2 style='margin: 0 0 1ex 0'>End of document</h2>",
        file=outfile
    )  #No, the sketchbook section is NOT footnotes!  This doesn't fix this, use of classic MOBI does IIRC.
    #Actually, it's anchors ending with numbers that triggers it.
    print("<a href='#topmenu'>(back to top)</a><hr /></body></html>",
          file=outfile)
    outfile.close()  #IronPython grumble grumble


if __name__ == "__main__":
    sections = utility.open_alldat()
    export_html(sections)
