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

import re, os, time

i = 1
dab={}
if os.path.exists("b.txt"):
    f=open("b.txt","rU")
    dab=eval(f.read())
    f.close()
#wget="..\\wget.exe"
wget="wget-gnu"
names={"index":"story","egsnp":"np","sketchbook":"sketch"}

f=open("metadataegs3.txt")
dob=eval(f.read())
f.close()

for interface in ("index","egsnp","sketchbook"):
    for styla in ("DateInBrowserTitle","DateStatedAboveComic"):
        fs=0
        sub=dob[names[interface]]
        print "I",interface
        while 1:
            if i not in sub.keys():
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
            try:
                if (names[interface]+"-"+styla+"-"+str(i) not in dab.keys()) or (dab[names[interface]+"-"+styla+"-"+str(i)]==None):
                    url = "http://www.egscomics.com/"+interface+".php?date="+(sub[i][styla])
                    #time.sleep(0.5)
                    os.system(wget+" -O \""+interface+".php@id="+str(i)+"\" \""+url+"\" >> wgetlog.txt 2>&1")
                    if not os.path.exists(interface+".php@id="+str(i)):
                        print "A"
                        continue
                    rd = open(interface+".php@id="+str(i),"rU")
                    data = rd.read()
                    rd.close()
                    os.unlink(interface+".php@id="+str(i))
                    res2 = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
                    works=sub[i][styla]
                    if not res2:
                        works=None
                    dab[names[interface]+"-"+styla+"-"+str(i)]=(works,res2.group() if res2 else None)
                else:
                    fs=0
            except Exception,e:
                print "Pfail",i,str(e)
            i += 1

f=open("dateswork.txt","w")
f.write(`dab`)
f.close()

raw_input()
