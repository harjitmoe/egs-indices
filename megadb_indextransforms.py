#!/usr/bin/env python
# -*- python -*-

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

import utility

#so as to pass JSON to eval
null=None
false=False
true=True

import os,sys

main_db=utility.open_alldat()

#SB2Year

by_year={}
by_year_order=[]

def handle_strip_record(strip):
    date=strip["Date"]
    year=date[:4]
    if year in by_year_order:
        by_year[year]["Comics"].append(strip)
    else:
        by_year[year]={"Title":year,"Comics":[strip],"RecordType":"StoryLine"}
        by_year_order.append(year)

def handle_arc(arc):
    map(handle_strip_record,arc["Comics"])

map(handle_arc,utility.specific_section(main_db,"sketch")["StoryArcs"])

output=[]
for year in by_year_order:
    output.append(by_year[year])

utility.specific_section(main_db,"sketch")["StoryArcs"]=output

#ArcLine

arcs=[]
curatitl=""

def handle_line(line):
    global curatitl
    print line["Title"]
    if line["Title"].count(": "):
        atitl,ltitl=line["Title"].split(": ",1)
        if atitl!=curatitl:
            arcs.append({"Title":atitl,"StoryLines":[],"RecordType":"StoryArc"})
            curatitl=atitl
        arcs[-1]["StoryLines"].append({"Title":ltitl,"Comics":line["Comics"],"RecordType":"StoryLine"})
    else:
        curatitl=""
        arcs.append(line)

map(handle_line,utility.specific_section(main_db,"story")["StoryArcs"])

utility.specific_section(main_db,"story")["StoryArcs"]=arcs

#

utility.save_alldat(main_db)
