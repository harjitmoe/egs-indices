#!/usr/bin/env python2
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
# Copyright (c) Thomas Hori 2015, 2016.
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
#     original work, and neither the name of Thomas Hori nor the names of authors or
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
names={"index":"story","egsnp":"np","sketchbook":"sketch"}

#At least this is entirely deterministic...
maxyear=time.gmtime(time.time())[0]
maxmonth=12
maxday=31

if os.path.exists("c.txt"):
    f=open("c.txt")
    database=eval(f.read())
    f.close()

try:
    for interface in ("index","egsnp","sketchbook"):
        year=2013 #Before 2013 usually goes without saying, don't waste time.
        month=1
        day=1
        print("I",interface)
        prefix = names[interface]
        if prefix not in list(database.keys()):
            database[prefix]={}
        #Get the section homepage (hence fallback) strip.
        url = "http://www.egscomics.com/"+interface+".php"
        os.system(wget+" -O \""+interface+".php\" \""+url+"\" >> wgetlog.txt 2>&1")
        if not os.path.exists(interface+".php"):
            print("A")
        rd = open(interface+".php","rU")
        data = rd.read()
        rd.close()
        comic_file_re = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
        fallback = comic_file_re.group()
        tm=time.time()
        while 1:
            try:
                if (year,month,day) not in list(database[prefix].keys()):
                    print("T",year,month,day)
                    url = "http://www.egscomics.com/"+interface+(".php?date=%04d-%02d-%02d"%(year,month,day))
                    #Cap rate at once a second
                    if 1.0-(time.time()-tm)>1:
                        time.sleep(1.0-(time.time()-tm))
                    os.system(wget+" -O \""+interface+(".php@date=%04d-%02d-%02d"%(year,month,day))+"\" \""+url+"\" >> wgetlog.txt 2>&1")
                    if not os.path.exists(interface+(".php@date=%04d-%02d-%02d"%(year,month,day))):
                        print("A")
                        continue
                    rd = open(interface+(".php@date=%04d-%02d-%02d"%(year,month,day)),"rU")
                    data = rd.read()
                    rd.close()
                    os.unlink(interface+(".php@date=%04d-%02d-%02d"%(year,month,day)))
                    comic_file_re = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
                    if not comic_file_re:
                        database[prefix][year,month,day]="Error"
                    else:
                        comic_file = comic_file_re.group()
                        if comic_file==fallback:
                            database[prefix][year,month,day]="No"
                        else:
                            database[prefix][year,month,day]="Yes"
            except Exception as e:
                print("Pfail",year,month,day,str(e))
            day += 1
            if day>maxday:
                day = 1
                month += 1
                if month>maxmonth:
                    month = 1
                    year += 1
                    if year>maxyear:
                        break
            tm=time.time()
finally:
    f=open("alldates.break.txt","w")
    f.write(repr(database))
    f.close()

f=open("alldates.txt","w")
f.write(repr(database))
f.close()

input()
