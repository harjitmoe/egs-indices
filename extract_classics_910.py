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

def extract_classics_910():
    print (">>> extract_classics_910")
    classics_db={}
    for stype in ("story","sketch","np"):
        f=open("Classics 910/classics-"+stype+".html","rU")
        b=f.read()+"\n"
        f.close()
        b=b.split("<div class='bbc_spoiler_content' style=\"display:none;\">")[1:]
        b=[i.split("</div>")[0].replace("\n"," ").replace("<br />","\n").strip().split("\n") for i in b]
        b2=[]
        for i in b:
            for j in i:
                if "href" in j: #i.e. not a dud placeholder - actually a link
                    b3,b4=j[::-1].split("<",1)[1][::-1].split("href='")[1].split("'",1)
                    b3="http://"+b3.split("http://")[1]
                    b4=b4.replace("<span class='bbc_underline'>","").replace("</span>","")
                    b4=b4.split(">")[1].strip()
                    if b4: #not a blank line with hyperlink
                        b5,b6,b7=b4.replace(","," ").split()
                        b7=b7.split("<",1)[0]
                        b5=utility.month2number(b5)
                        b6="%02d"%int(b6)
                        b4="-".join((b7,b5,b6))
                        b4=utility.datefix_910(b4,stype)
                        classic=(int(b7)<2009) or ((int(b7)==2009) and (int(b5)<2))
                        b2.append((b4,(utility.standardise910link(b3),classic)))
        classics_db[stype]=dict(b2)
    return classics_db

if __name__=="__main__":
    open(".build/classics_910.txt","w").write(repr(extract_classics_910()))
