#!/usr/bin/env python
# -*- python -*-
"""fetch transcripts, fix titles"""

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

import os, utility
import databases, titleharjit

def megadb_fetch_tss(alldat):
    print (">>> megadb_fetch_tss")
    for arc in utility.specific_section(alldat,"story")["StoryArcs"]:
        for strip in arc['Comics']:
            if os.path.exists("..\\Transcripts\\"+strip['Date']+".txt"):
                #print strip["Date"]
                ts_file=open("..\\Transcripts\\"+strip['Date']+".txt","rU")
                transcript=ts_file.read()
                ts_file.close()
                #Thank goodness for Python mutables
                #I can change strip and it also changes in alldat
                # on account of referencing the same object
                strip["Transcript"]=databases.to_utf8(transcript.rstrip("\n")+"\n\n")
            else:
                #print strip['Date']
                strip["Transcript"]=None
            if ("Official" not in strip['Titles']):
                if strip['Id'] in databases.titlebank["megatitles"]:
                    strip['Titles']["Official"]=databases.titlebank["megatitles"][strip['Id']]
                if strip['Id'] in titleharjit.mytitles:
                    strip['Titles']["HarJIT"]=titleharjit.mytitles[strip['Id']]
                if strip['Id'] in databases.titlebank["titles"]:
                    strip['Titles']["Tumblr"]=databases.titlebank["titles"][strip['Id']]
    marker="<strong>Requested by"
    marker2="<strong><a href=\"http://www.patreon.com/egscomics\">Requested</a> by"
    marker3="<strong><a href=\"http://www.patreon.com/egscomics\"> Requested</a> by"
    marker4="<strong> Requested</strong></a><strong> by"
    for arc in utility.specific_section(alldat,"sketch")["StoryArcs"]:
        for strip in arc['Comics']:        
            if ("Official" not in strip['Titles']):
                if strip['Id'] in titleharjit.sbmytitles:
                    strip['Titles']["HarJIT"]=titleharjit.sbmytitles[strip['Id']]
                if strip['Id'] in databases.titlebank["sbmegatitles"]: #NOT elif
                    strip['Titles']["Official"]=databases.titlebank["sbmegatitles"][strip['Id']]
                elif strip['Id'] in databases.metadataegs["sketch"]: #YES elif
                    c=utility.deentity(databases.metadataegs["sketch"][strip['Id']]["Commentary"].replace("&nbsp;"," "),0)
                    if c.count(marker):
                        strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                    elif c.count(marker2):
                        strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker2,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                    elif c.count(marker3):
                        strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker3,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                    elif c.count(marker4):
                        strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker4,1)[1].split("</p>",1)[0].split("<br />",1)[0])
    return alldat

if __name__=="__main__":
    utility.save_alldat(megadb_fetch_tss(utility.open_alldat()))
