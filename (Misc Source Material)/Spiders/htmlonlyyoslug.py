#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (c) 2009 xipe totec
#
# http://code.activestate.com/recipes/576881-fetch-all-new-xkcd-strips/
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
#  THE SOFTWARE.
#
# Copyright (c) HarJIT 2015, 2016, 2019.
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

import re, os, time

database={}
#wget="..\\..\\..\\Tools\\wget.exe"
#wget="wget-gnu"
wget="wget"
names={"comic":"story","egsnp":"np","sketchbook":"sketch"}

def strip_comments(data):
    try:
        data="".join([i.split("-->",1)[1] for i in ("-->"+data+"-->").split("<!--")])
        if data.endswith("-->"):
            data=data[:-3]
        return data
    except:
        global foo
        foo=data
        raise

def strip_style(data):
    try:
        data="".join([i.split('"',1)[1] for i in ('"'+data).split(' style="')])
        return data
    except:
        global foo
        foo=data
        raise

if os.path.exists("a.txt"):
    f=open("a.txt")
    database=eval(f.read())
    f.close()
else:
    f=open("metadataegs3.txt")
    database=eval(f.read())
    f.close()

firstnewslugs = {"story": "2018-05-23", "sketch": "2018-02-12-nase-fv5-sarah-and-elliot",
                "np": "2018-05-21"}

lastt = "xktdxkxxxkxdxupdxh,bhxxgcxxgcxgcxgxgcxgci" # THANK YOU, NEW SCHEME
for interface in ("comic","egsnp","sketchbook"):
    print("I",interface)
    prefix = names[interface]
    if prefix not in list(database.keys()):
        database[prefix] = {}
    i = database[prefix].get("<LAST>", firstnewslugs[prefix])
    while 1:
        try:
            print(prefix, i)
            url = "http://www.egscomics.com/" + interface + "/" + i
            #time.sleep(0.5)
            os.system(wget+" -O temp.tmp \""+url+"\" >> wgetlog.txt 2>&1")
            if not os.path.exists("temp.tmp"):
                print("A")
                continue
            rd = open("temp.tmp", "rU", errors="surrogateescape")
            data = rd.read()
            rd.close()
            os.unlink("temp.tmp")
            if i not in list(database[prefix].keys()):
                title_date_re = re.search("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].*?</title>", data)
                valid_id_re = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
                if not valid_id_re or valid_id_re.group(0) == lastt:
                    break #Hopefully not needed.
                #Obtain date from above comic if present
                printed_date=""
                if '">Comic for ' in data:
                    printed_date=data.split('">Comic for ',1)[1].split("</div>",1)[0].split(", ",1)[1]
                    printed_date=printed_date.replace(", "," ")
                    month,day,year=printed_date.split(" ",3)
                    month="%02d"%([None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(month[:3]))
                    day="%02d"%int(day)
                    printed_date=year+"-"+month+"-"+day
                #Obtain HTML title and check against mouse-over text
                title_date=""
                if title_date_re:
                    title_date=title_date_re.group()[:-8]
                mouseover=data.split('title="',1)[1].split('"',1)[0]
                if not title_date:
                    title_date=mouseover
                if title_date!=mouseover:
                    raise AssertionError
                #Separate date and title from HTML title / mouse-over
                title_date,title=(title_date+" ").split(" ",1)
                title=title.strip(" -")
                title_date=title_date.strip(" -")
                if title_date[0] not in "0123456789":
                    title=title_date+" "+title
                    title_date=""
                if title and title[0] in "0123456789":
                    title_date=title_date+" "+title
                    title=""
                #Extract commentary (which may contain some title info)
                #Was <div id="newsarea">
                commentary=data.split('<div id="news">',1)[1].split('<div id="boxad">',1)[0]
                commentary=strip_style(strip_comments(commentary)).replace(' target="_blank"','').replace('<div id="newsheader"></div>',"").replace("<div>","<br />").replace("</div>","").strip()
                #Store in database
                database[prefix]["SLUG-"+i]={"Commentary":commentary,"UrlSlug":i,"DateStatedAboveComic":(printed_date or None),"DateInBrowserTitle":(title_date or None),"HtmlComicTitle":(title or None)}
            if 'class="cc-next" rel="next" href="' in data:
                i = data.split('class="cc-next" rel="next" href="', 1)[1].split('"', 1)[0].rsplit("/", 1)[1]
            else:
                break
        except Exception as e:
            print("Pfail",i,str(e))
            raise
    database[prefix]["<LAST>"] = i

f=open("metadataegs4.txt","w")
f.write(repr(database))
f.close()

input()
