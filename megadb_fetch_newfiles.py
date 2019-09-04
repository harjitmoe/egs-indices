#!/usr/bin/env python3
# -*- python -*-

# Copyright (c) HarJIT 2015, 2017, 2019.
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

import utility, databases
import os, sys


def shared_date(strip, djv, source_strip):
    if source_strip[0] in djv:
        djv[source_strip[0]]["SharedDateIndex"] = 1
        djv[source_strip[0]]["SharedDateTotal"][0] += 1
        strip["SharedDateIndex"] = djv[source_strip[0]]["SharedDateTotal"][0]
        strip["SharedDateTotal"] = djv[source_strip[0]]["SharedDateTotal"]
    else:
        strip["SharedDateIndex"] = 0
        strip["SharedDateTotal"] = [1]  #1-list approximating a pointer.
        djv[source_strip[0]] = strip


def megadb_fetch_newfiles(alldat, reddit_titles, reddit_links, links_910new):
    print(">>> megadb_fetch_newfiles")
    for sect in ("story", "np", "sketch"):
        mode = databases.titlebank["modes"][sect]
        arcs = []
        allot = {}
        for number, name in mode:
            if name in allot:
                arcs.append(allot[name])
                continue
            newark = {"Title": name, "Comics": [], "RecordType": "StoryLine"}
            utility.specific_section(alldat, sect)["StoryArcs"].append(newark)
            arcs.append(newark)
            allot[name] = newark
        djv = {}
        for source_strip in sorted(databases.lsdir[sect].keys()):
            if len(databases.lsdir[sect][source_strip]) == 2:
                source_strip = (source_strip, ) + tuple(
                    databases.lsdir[sect][source_strip])
            else:
                source_strip = databases.lsdir[sect][source_strip]
            if source_strip[1] and ((mode[0][0]) and
                                    (source_strip[1] < mode[0][0])):
                continue
            strip = {}
            shared_date(strip, djv, source_strip)
            strip["Date"] = source_strip[0]
            strip["Id"] = source_strip[1]
            if len(source_strip) >= 4:
                strip["UrlSlug"] = source_strip[3]
            assert (strip["Id"] is not None) or ("UrlSlug" in strip), strip
            if utility.identifier(strip) in databases.metadataegs[sect]:
                siid = utility.identifier(strip)
                if siid == 2502:
                    # Due to the unknown-URL-to-current-page behaviour of EGS, the Reddit data
                    # uses a 2502 ID for 2018-05-23, but the metadataegs actually uses it for
                    # 2018-05-25 since that was the current page at the time…
                    siid = "SLUG-" + strip["UrlSlug"]
                strip.update(
                    utility.recdeentity(databases.metadataegs[sect][siid]))
            strip["OokiiId"] = -1
            strip["FileNameTitle"] = source_strip[2]
            strip["Section"] = utility.egslink2ookii[sect]
            strip["Characters"] = {}
            strip["ReactionLinks"] = []
            if utility.identifier(strip) in reddit_links[sect]:
                strip["ReactionLinks"].append(
                    reddit_links[sect][utility.identifier(strip)])
            if strip["Date"] in links_910new[sect]:
                utility.merge_reactions(strip["ReactionLinks"],
                                        links_910new[sect][strip["Date"]])
            utility.dates_index(strip, databases.dateswork[sect])
            if utility.identifier(strip) not in reddit_titles[sect]:
                strip["Titles"] = {
                    "Filename": strip["FileNameTitle"]
                }  #For now
            else:
                uuu = utility.alphabetical_id(strip["FileNameTitle"])
                if uuu and uuu == utility.alphabetical_id(reddit_titles[sect][
                        utility.identifier(strip)][::-1].split("( ",
                                                               1)[1][::-1]):
                    strip["Titles"] = {
                        "Reddit": reddit_titles[sect][utility.identifier(strip)][:-1] +
                                  ", based on filename)"
                    }
                else:
                    strip["Titles"] = {
                        "Reddit": reddit_titles[sect][utility.identifier(strip)]
                    }
            if ("HtmlComicTitle" in strip) and strip["HtmlComicTitle"] and (
                    "UrlSlug" not in strip):
                strip["Titles"]["Official"] = strip["HtmlComicTitle"]
            strip["RecordType"] = "Comic"
            if strip["Id"] is not None:
                assert isinstance(strip["Id"], int), strip
                for number, (aid, name) in enumerate(mode):
                    if isinstance(aid, int) and (strip["Id"] < aid):
                        arcs[number - 1]["Comics"].append(strip)
                        break
                else:
                    #else clause of for-loop, i.e. finished without break
                    arcs[-1]["Comics"].append(strip)
            else:
                for number, (aid, name) in enumerate(mode):
                    if isinstance(aid, str) and (strip["Date"] < aid):
                        arcs[number - 1]["Comics"].append(strip)
                        break
                else:
                    #else clause of for-loop, i.e. finished without break
                    arcs[-1]["Comics"].append(strip)
    return alldat
