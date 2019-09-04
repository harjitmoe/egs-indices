#!/usr/bin/env python3
# -*- python -*-
"""fetch transcripts, fix titles"""

# Copyright (c) HarJIT 2015, 2017, 2018, 2019.
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

import os
import databases, titleharjit, utility

# Following is already in databases.py
#@functools.partial(codecs.register_error, "winlatin_one_fallback")
#def winlatin_one_fallback_handler(error):
#    return (error.object[error.start:error.end].decode("windows-1252"), error.end)


def megadb_fetch_tss(alldat):
    print(">>> megadb_fetch_tss")
    for arc in utility.specific_section(alldat, "story")["StoryArcs"]:
        for strip in arc['Comics']:
            if os.path.exists("../Transcripts/" + strip['Date'] + ".txt"):
                #print strip["Date"]
                ts_file = open("../Transcripts/" + strip['Date'] + ".txt",
                               "rb")
                transcript = ts_file.read().replace(b"\r\n", b"\n").replace(
                    b"\r", b"\n")
                ts_file.close()
                #Thank goodness for Python mutables
                #I can change strip and it also changes in alldat
                # on account of referencing the same object
                tscr = transcript.decode("utf-8",
                                         errors="winlatin_one_fallback")
                strip["Transcript"] = utility.deentity(
                    tscr.rstrip("\n") + "\n\n")
            else:
                #print strip["Date"]
                try:
                    ts_file = databases.open_tss("Transcripts/" +
                                                 strip['Date'] + ".txt")
                    transcript = ts_file.read().replace(b"\r\n",
                                                        b"\n").replace(
                                                            b"\r", b"\n")
                except (EnvironmentError, KeyError):
                    strip["Transcript"] = None
                else:
                    ts_file.close()
                    #Thank goodness for Python mutables
                    #I can change strip and it also changes in alldat
                    # on account of referencing the same object
                    tscr = transcript.decode("utf-8",
                                             errors="winlatin_one_fallback")
                    strip["Transcript"] = utility.deentity(
                        tscr.rstrip("\n") + "\n\n")
            if ("Official" not in strip['Titles']):
                if strip['Id'] in databases.titlebank["megatitles"]:
                    strip['Titles']["Official"] = databases.titlebank[
                        "megatitles"][strip['Id']]
                if strip['Id'] in titleharjit.mytitles:
                    strip['Titles']["HarJIT"] = titleharjit.mytitles[
                        strip['Id']]
                if strip['Id'] in databases.titlebank["titles"]:
                    strip['Titles']["Tumblr"] = databases.titlebank["titles"][
                        strip['Id']]
    marker = "<strong>Requested by"
    marker2 = "<strong><a href=\"http://www.patreon.com/egscomics\">Requested</a> by"
    marker3 = "<strong><a href=\"http://www.patreon.com/egscomics\"> Requested</a> by"
    marker4 = "<strong> Requested</strong></a><strong> by"
    # The metadataegs3 file is produced using repr at the moment but this toolchain is parsing it as YAML (with some preprocessing
    # regarding changing None to null) for security reasons.  Hence strings not containing apostrophes are single quoted (ASCII), which
    # YAML interprets as a raw string (somewhat like Python's r"..."), hence we end up with literal \n in the strings.
    trim = lambda c, m: "Requested by " + utility.detag(
        c.split(m, 1)[1].split("</p>", 1)[0].split("<br />", 1)[0]).replace(
            "\\n", "\n").strip()
    gcom = lambda st: utility.deentity(
        utility.recdeentity(
            databases.metadataegs["sketch"][utility.identifier(strip)][
                "Commentary"].replace("&nbsp;", " "), 0))
    for arc in utility.specific_section(alldat, "story")["StoryArcs"]:
        for strip in arc['Comics']:
            if strip['Id'] and strip['Id'] in databases.stids:
                strip["UrlSlug"] = databases.stids[strip['Id']]
    for arc in utility.specific_section(alldat, "np")["StoryArcs"]:
        for strip in arc['Comics']:
            if strip['Id'] and strip['Id'] in databases.npids:
                strip["UrlSlug"] = databases.npids[strip['Id']]
    for arc in utility.specific_section(alldat, "sketch")["StoryArcs"]:
        for strip in arc['Comics']:
            if strip['Id'] and strip['Id'] in databases.sbids:
                strip["UrlSlug"] = databases.sbids[strip['Id']]
            if ("Official" not in strip['Titles']):
                if utility.identifier(strip) in titleharjit.sbmytitles:
                    strip['Titles']["HarJIT"] = titleharjit.sbmytitles[
                        utility.identifier(strip)]
                if utility.identifier(strip) in databases.titlebank[
                        "sbmegatitles"]:  #NOT elif
                    strip['Titles']["Official"] = databases.titlebank[
                        "sbmegatitles"][utility.identifier(strip)]
                elif utility.identifier(
                        strip) in databases.metadataegs["sketch"]:  #YES elif
                    c = gcom(strip)
                    if c.count(marker):
                        strip['Titles']["Official"] = trim(c, marker)
                    elif c.count(marker2):
                        strip['Titles']["Official"] = trim(c, marker2)
                    elif c.count(marker3):
                        strip['Titles']["Official"] = trim(c, marker3)
                    elif c.count(marker4):
                        strip['Titles']["Official"] = trim(c, marker4)
    return alldat
