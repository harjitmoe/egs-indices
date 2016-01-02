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

import re, os, time

i = 1
dab={}
wget="..\\..\\..\\Tools\\wget.exe"
#wget="wget-gnu"
names={"index":"story","egsnp":"np","sketchbook":"sketch"}

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
    dab=eval(f.read())
    f.close()

for interface in ("index","egsnp","sketchbook"):
    fs=0
    print "I",interface
    prefix = names[interface]
    if prefix not in dab.keys():
        dab[prefix]={}
    while 1:
        try:
            if i not in dab[prefix].keys():
                url = "http://www.egscomics.com/"+interface+".php?id="+str(i)
                #time.sleep(0.5)
                os.system(wget+" -O \""+interface+".php@id="+str(i)+"\" \""+url+"\" >> wgetlog.txt 2>&1")
                if not os.path.exists(interface+".php@id="+str(i)):
                    print "A"
                    continue
                rd = open(interface+".php@id="+str(i),"rU")
                data = rd.read()
                rd.close()
                os.unlink(interface+".php@id="+str(i))
                res = re.search("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]</title>", data)
                res2 = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
                if not res2:
                    print "F",i
                    fs+=1
                    if fs>=5:
                        i=1
                        break
                    else:
                        i+=1
                        continue
                else:
                    fs=0
                dat4=data.split('<div id="newsarea">',1)[1].split('<div id="boxad">',1)[0]
                dat0=""
                if res:
                    dat0=res.group()[:-8]
                dat1=""
                dat3=""
                if 'title="' in data:
                    dat1,dat3=(data.split('title="',1)[1].split('"',1)[0]+"-").split("-",1)
                    dat1=dat1.strip()
                    dat3=dat3.strip().rstrip("-")
                dat2=""
                if '">Comic for ' in data:
                    dat2=data.split('">Comic for ',1)[1].split("</div>",1)[0].split(", ",1)[1]
                    dat2=dat2.replace(", "," ")
                    month,day,year=dat2.split(" ",3)
                    month="%02d"%([None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(month[:3]))
                    day="%02d"%int(day)
                    dat2=year+"-"+month+"-"+day
                date1=dat0
                date2,title=(dat1+"-"+dat3+" ").split(" ",1)
                title=title.strip(" -")
                date2=date2.strip(" -")
                date3=dat2
                if date2[0] not in "0123456789":
                    title=date2+" "+title
                    date2=""
                if title and title[0] in "0123456789":
                    date2=date2+" "+title
                    title=""
                if not date1:
                    date1=date2
                if date1!=date2:
                    raise AssertionError
                if " - " in date1:
                    date1,title=date1.split(" - ",1)
                commentary=strip_style(strip_comments(dat4)).replace(' target="_blank"','').replace('<div id="newsheader"></div>',"").replace("<div>","<br />").replace("</div>","").strip()
                dab[prefix][i]={"Commentary":commentary,"Id":i,"DateStatedAboveComic":(date3 or None),"DateInBrowserTitle":(date1 or None),"HtmlComicTitle":(title or None)}
            else:
                fs=0
        except Exception,e:
            print "Pfail",i,str(e)
        i += 1

f=open("metadataegs3.txt","w")
f.write(`dab`)
f.close()

raw_input()
