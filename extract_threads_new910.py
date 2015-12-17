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
class Gazza(dict):
    """Subclass dict to allow b[i].append without having to check if
    b[i] exists yet thus allowing cleaner code in general."""
    def __getitem__(self,k):
        try:
            return dict.__getitem__(self,k)
        except KeyError:
            self[k]=[]
            return self[k]
date2str=Gazza()
def parse_date(s):
    os=s
    #Correcting missing years (yeah) and months (whut?)
    #and wrong dates in general
    if s=="Story: Friday 14, 2012":
        s="Story: Friday December 14, 2012"
    elif s=="Story Friday January 3rd":
        s="Story Friday January 3rd, 2014"
    elif s=="Story Tuesday April 16th":
        s="Story Tuesday April 16th, 2013"
    elif s=="Story Tuesday December 31st":
        s="Story Tuesday December 31st, 2013"
    elif s=="Story: Mon 18 2013":
        s="Story: Mon March 18 2013"
    elif s=="Story Friday December 6th":
        s="Story Friday December 6th 2013"
    elif s=="Sketchbook Wednesday December 31th":
        s="Sketchbook Wednesday December 31th 2014"
    elif s=="Sketchbook: Thursday, September 4":
        s="Sketchbook: Thursday, September 4 2014"
    elif s=='Story: Monday, 4th February 2013':
        s='Story: Monday, 3rd February 2013'
    elif s=='NP, December 17th':
        s='NP, December 17th 2009'
    elif s=='NP Wednesday August 27th':
        s='NP Wednesday August 27th 2014'
    elif s=='NP, Jan 22':
        s='NP, Jan 22 2010'
    elif s=='Power glove, power glove, power glove!':
        #Apparently a secondary thread for this?
        s='Story, Jan 21 2013'
    elif s=='Zoinks!':
        s='NP, Jan 5th 2010'
    elif s=='Gods of Curling':
        s='NP, Feb 19th 2010'
    #Remove annotations which confuse the gestalt matcher
    if s.startswith("Story Friday October 17, 2014"):
        s="Story Friday October 17, 2014"
    #Real work
    year=None
    month=None
    day=None
    dow=None
    from difflib import get_close_matches as gcm
    s=s.replace(","," ")
    while "  " in s:
        s=s.replace("  "," ")
    s=s.lower().strip("[]").split()
    months=["january","february","march","april","may","june","july","quinctilis","august","sextilis","september","october","november","december"]
    months.extend([i[:3] for i in months])
    for j in s[:]:
        i=gcm(j,months,1,0.6)
        if i:
            month=int(utility.month2number(i[0].title()),10)
            s.remove(j)
        elif j in ("2015","2014","2013","2012","2011","2010","2009"):
            year=int(j,10)
            s.remove(j)
        elif (len(j.rstrip("."))<=2) and (j[0] in "0123456789") and (not j.endswith(")")):
            if day==None:
                day=int(j.rstrip("."),10)
                s.remove(j)
            else:
                print year,month,day,dow,s
                return None
        elif (j.endswith("th") or j.endswith("nd") or j.endswith("st") or j.endswith("rd")) and (j[0] in "0123456789"):
            if day==None:
                day=int(j[:-2],10)
                s.remove(j)
            else:
                print year,month,day,dow,s
                return None
    if not year or not month or not day:
        print year,month,day,dow,s
        return None
    date2str["%04d-%02d-%02d"%(year,month,day)].append(os)
    return "%04d-%02d-%02d"%(year,month,day)
def grok(code):
    b3={}
    import os
    checkdb=None
    checkdbp="alldates-%s.txt"%code.lower()
    if os.path.exists(checkdbp):
        #Insecure
        checkdb=eval(open(checkdbp,"rU").read())
    for f in os.listdir("910 Raw DBs/"+code)[:]:
        if f.endswith(".htm"):
            f=open(os.path.join("910 Raw DBs/"+code,f),"rU")
            b=f.read()
            f.close()
            b=b.split('<div class="rowContent">')[1:]
            b=[i.split('<a href="',1)[1] for i in b]
            b=[i.split('</a>',1)[0] for i in b]
            b=[i.split('" class="topic_title title">',1)[::-1] for i in b]
            b=dict(b)
            b3.update(b)
    b2=Gazza()
    for i in b3.keys():
        j=parse_date(i)
        if j:
            j=utility.datefix_910(j,code.lower())
            if checkdb and (j not in checkdb):
                print "anomoly",code,j
            #XXX do what with 2014-12-08?
            b2[j].append((utility.standardise910link(b3[i]),False))
        else:
            print i
    return b2

def extract_threads_new910():
    print (">>> extract_threads_new910")
    b4={"story":grok("Story"),"sketch":grok("Sketch"),"np":grok("NP")}
    open(".build/910-new.dat","w").write(repr(b4))

if __name__=="__main__":
    extract_threads_new910()
