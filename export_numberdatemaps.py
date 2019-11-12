# Copyright (c) HarJIT 2015.
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

import utility, os


def munj(id):
    if id == -1:
        return "NONE"
    return id


def print_infos_nem(nem, cd):
    print("|-\n|%s||%s||%s" %
          (cd["Date"], cd["-numberidmap-numero"], munj(cd["Id"])),
          file=nem)


def print_infos_nom(nom, cd):
    print("|-\n|%s||%s||%s" %
          (cd["Date"], cd["-numberidmap-numero"], munj(cd["OokiiId"])),
          file=nom)


def print_infos_dim(dim, cd):
    print("|-\n|%s||%s||%s||%s" %
          (cd["Date"], cd["-numberidmap-numero"], munj(cd["Id"]),
           ("YES" if cd["DateIndexable"] else "NO")),
          file=dim)


def print_infos_dfm(dfm, cd):
    print("|-\n|%s||%s||%s" %
          (munj(cd["Id"]), cd["Date"], cd["DateInBrowserTitle"]),
          file=dfm)


def export_numberdatemaps(alldat):
    print(">>> export_numberdatemaps")
    stdb = utility.specific_section(alldat, "story")["StoryArcs"]
    sbdb = utility.specific_section(alldat, "sketch")["StoryArcs"]
    npdb = utility.specific_section(alldat, "np")["StoryArcs"]
    nem = open(".build/numbereidmap.txt", "w")
    print("== Numbers to IDs ==", file=nem)
    nom = open(".build/numberoidmap.txt", "w")
    print("== Numbers to Ookii IDs ==", file=nom)
    dim = open(".build/numberdibmap.txt", "w")
    print("== Which comics date lookup works for ==", file=dim)
    dfm = open(".build/datefakemap.txt", "w")
    print("== Incorrect, elaborated or non-ISO dates in browser title ==",
          file=dfm)
    for title, db in (("Main Story", stdb), ("Sketchbook", sbdb), ("EGS:NP",
                                                                   npdb)):
        print(
            "===%s===\n\n{|border=\"1\" cellpadding=\"3\"\n!Date!!Number!!ID (EGSComics)"
            % title,
            file=nem)
        print(
            "===%s===\n\n{|border=\"1\" cellpadding=\"3\"\n!Date!!Number!!OokiiDB ID"
            % title,
            file=nom)
        print(
            "===%s===\n\n{|border=\"1\" cellpadding=\"3\"\n!Date!!Number!!ID (EGSComics)!!Date-indexable"
            % title,
            file=dim)
        print(
            "===%s===\n\nThis only catalogues those found using ID-lookup. Those found using date lookup are invariably wrong and seem not to depend on the actual date. Only discrepancies, and elaborated dates on multi-posting days (or not), are listed. \n\n{|border=\"1\" cellpadding=\"3\"\n!ID!!ISO Date%s!!Date in browser title"
            % (title, (" (probable)" if title == "EGS:NP" else
                       " (converted from above comic)")),
            file=dfm)
        lastid = -40
        lastod = -40
        lastdib = None
        numero = 0
        ellipsed_nem = 2
        ellipsed_nom = 2
        ellipsed_dim = 2
        last = None
        lastprinted_nem = None
        lastprinted_nom = None
        lastprinted_dim = None
        for arc in db:
            for line in (arc["StoryLines"]
                         if arc["RecordType"] == "StoryArc" else (arc, )):
                for comic in line["Comics"]:
                    numero += 1
                    comic["-numberidmap-numero"] = numero
                    if "DateInBrowserTitle" not in comic:
                        comic["DateInBrowserTitle"] = "(Error)"
                    if comic["Id"] is None:
                        continue
                    if (comic["Id"] != lastid + 1):
                        if (last != None) and (last != lastprinted_nem):
                            print_infos_nem(nem, last)
                        print_infos_nem(nem, comic)
                        lastprinted_nem = comic
                        ellipsed_nem = 0
                    else:
                        if ellipsed_nem == 1:
                            print("|-\n|...||...||...", file=nem)
                        ellipsed_nem += 1
                    if (comic["OokiiId"] != lastod + 1):
                        if (last != None) and (last != lastprinted_nom):
                            print_infos_nom(nom, last)
                        print_infos_nom(nom, comic)
                        lastprinted_nom = comic
                        ellipsed_nom = 0
                    else:
                        if ellipsed_nom == 1:
                            print("|-\n|...||...||...", file=nom)
                        ellipsed_nom += 1
                    if (comic["DateIndexable"] != lastdib):
                        if (last != None) and (last != lastprinted_dim):
                            print_infos_dim(dim, last)
                        print_infos_dim(dim, comic)
                        lastprinted_dim = comic
                        ellipsed_dim = 0
                    else:
                        if ellipsed_dim == 1:
                            print("|-\n|...||...||...||...", file=dim)
                        ellipsed_dim += 1
                    if (comic["Date"] != comic["DateInBrowserTitle"]):
                        print_infos_dfm(dfm, comic)
                    lastod = (comic["OokiiId"] if
                              (comic["OokiiId"] != -1) else -2)
                    lastid = comic["Id"]
                    lastdib = comic["DateIndexable"]
                    last = comic
        print("|}\n\n", file=nem)
        print("|}\n\n", file=nom)
        print("|}\n\n", file=dim)
        print("|}\n\n", file=dfm)
        print("COMIC COUNT FOR {}: {} strips".format(title, numero)) # i.e. to stdout.
    for i in (nem, nom, dim, dfm):
        i.close()  #IronPython grumble grumble


if __name__ == "__main__":
    alldat = utility.open_alldat()
    export_numberdatemaps(alldat)
