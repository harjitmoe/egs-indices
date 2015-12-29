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

import utility

#SB2Year

def handle_strip_record(strip, by_year, by_year_order):
    date=strip["Date"]
    year=date[:4]
    if year in by_year_order:
        by_year[year]["Comics"].append(strip)
    else:
        by_year[year]={"Title":year,"Comics":[strip],"RecordType":"StoryLine"}
        by_year_order.append(year)

def handle_arc(arc, by_year, by_year_order):
    for i in arc["Comics"]:
        handle_strip_record(i,by_year,by_year_order)

def megadb_sb2year(main_db):
    print ">>> megadb_sb2year (megadb_indextransforms)"
    by_year={}
    by_year_order=[]
    for arc in utility.specific_section(main_db,"sketch")["StoryArcs"]:
        handle_arc(arc, by_year, by_year_order)
    output=[]
    for year in by_year_order:
        output.append(by_year[year])
    utility.specific_section(main_db,"sketch")["StoryArcs"]=output
    return main_db

#ArcLine

def handle_line(line, arcs, curatitl_p):
    print line["Title"]
    if line["Title"].count(": "):
        atitl,ltitl=line["Title"].split(": ",1)
        if atitl!=curatitl_p[0]:
            arcs.append({"Title":atitl,"StoryLines":[],"RecordType":"StoryArc"})
            curatitl_p[0]=atitl
        arcs[-1]["StoryLines"].append({"Title":ltitl,"Comics":line["Comics"],"RecordType":"StoryLine"})
    else:
        curatitl_p[0]=""
        arcs.append(line)

def megadb_arcline(main_db):
    print ">>> megadb_arcline (megadb_indextransforms)"
    arcs=[]
    curatitl_p=[""] #single-item array functioning as a pointer.
    arcs_in=utility.specific_section(main_db,"story")["StoryArcs"]
    for arc in arcs_in:
        handle_line(arc,arcs,curatitl_p)
    utility.specific_section(main_db,"story")["StoryArcs"]=arcs
    return main_db

#

def megadb_indextransforms(alldat):
    return megadb_arcline(megadb_sb2year(alldat))

if __name__=="__main__":
    utility.save_alldat(megadb_indextransforms(utility.open_alldat()))
