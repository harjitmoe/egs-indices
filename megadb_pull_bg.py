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

def formurl(idst):
    #Not eval(idst) because starting a number with 0 means octal in Py2 (a nice gotcha for newbies) and is invalid in Py3
    ext = "_1280x960.gif" if int(idst,10) in gifs else "_1280x960.jpg"
    return "http://egscomics.com/bg/egs_bg_"+idst+ext

gifs=[0,1,2,3,4,5,6,7,826,27,28,29,30,31,32,33,34,35,36,38,45,48,54,55]

def megadb_pull_bg(alldat):
    print ">>> megadb_pull_bg"
    f=open("BgNames.txt","rU")
    b=eval(f.read()) #Blatantly no security, assume trust
    f.close()
    f=open("BgDescriptions.txt","rU")
    c=eval(f.read()) #Blatantly no security, assume trust
    f.close()
    comics=[]
    for i in sorted(c.keys()):
        title=b[i]
        comment=c[i]
        comics.append({"ReactionLinks": [], "SharedDateIndex": 0, "OokiiId": -1, "DateIndexable": False, "Section": "Backgrounds", "RecordType": "Comic", "Titles": {"Official": title}, "Characters": None, "Date": "?", "Commentary": comment, "Transcript": None, "Id": int(i,10), "SpecialUrl": formurl(i)})
    alldat.append({"Title":"Backgrounds","StoryArcs":comics,"RecordType":"Section"})
    return alldat

if __name__=="__main__":
    utility.save_alldat(megadb_pull_bg(utility.open_alldat()))
