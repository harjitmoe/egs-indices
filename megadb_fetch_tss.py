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

from titleharjit import *

import os,utility
from titlebank import * #Must be imported after utility

alldat=eval(open(".build/AllMegaDb.txt","rU").read())
for arc in utility.specific_section(alldat,"story")["StoryArcs"]:
    for strip in arc['Comics']:
        if os.path.exists("..\\Transcripts\\"+strip['Date']+".txt"):
            #print strip["Date"]
            transcript=open("..\\Transcripts\\"+strip['Date']+".txt","rU").read()
            #Thank goodness for Python mutables
            #I can change strip and it also changes in alldat
            # on account of referencing the same object
            strip["Transcript"]=utility.scour(transcript.rstrip("\n")+"\n\n")
        else:
            #print strip['Date']
            strip["Transcript"]=None
        if ("Official" not in strip['Titles']):
            if strip['Id'] in megatitles:
                strip['Titles']["Official"]=megatitles[strip['Id']]
            if strip['Id'] in mytitles:
                strip['Titles']["HarJIT"]=mytitles[strip['Id']]
            if strip['Id'] in titles:
                strip['Titles']["Tumblr"]=titles[strip['Id']]

locals().update(utility.open_dbs("sketch"))
marker="<strong>Requested by"
marker2="<strong><a href=\"http://www.patreon.com/egscomics\">Requested</a> by"
marker3="<strong><a href=\"http://www.patreon.com/egscomics\"> Requested</a> by"
marker4="<strong> Requested</strong></a><strong> by"
for arc in utility.specific_section(alldat,"sketch")["StoryArcs"]:
    for strip in arc['Comics']:        
        if ("Official" not in strip['Titles']):
            if strip['Id'] in sbmytitles:
                strip['Titles']["HarJIT"]=sbmytitles[strip['Id']]
            if strip['Id'] in sbmegatitles: #NOT elif
                strip['Titles']["Official"]=sbmegatitles[strip['Id']]
            elif strip['Id'] in metadataegs: #YES elif
                c=utility.dirty(metadataegs[strip['Id']]["Commentary"])
                if c.count(marker):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                elif c.count(marker2):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker2,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                elif c.count(marker3):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker3,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                elif c.count(marker4):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker4,1)[1].split("</p>",1)[0].split("<br />",1)[0])

open(".build/AllMegaDb.txt","w").write(repr(alldat))
