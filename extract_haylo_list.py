# Copyright (c) Thomas Hori 2015.
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

def extract_haylo_list():
    print (">>> extract_haylo_list")
    import utility
    f=open("HayloList.html")
    b=f.read().replace("www.egscomics.com","egscomics.com").replace("/index.php?","/?")
    b=utility.deentity(b,3)
    f.close()
    #XXX this ignores headings
    b=[i.split("</p>")[0] for i in b.split('<p style="margin-left:10.2em; \n')[1:]]
    lst={}
    order=[]
    for record in b:
        date=record.split('<a href="http://egscomics.com/?date=')[1].split('"')[0]
        title=utility.deentity(record.split('<a href="http://egscomics.com/?date='+date+'" >')[2].split('</a')[0],2)
        related=[(utility.standardise910link(utility.deentity(i.split('"')[0],2)),i.split('/res/')[1].startswith("classic")) for i in record.split('<a href="http://egscomics.com/?date='+date+'" >')[2].split('<a href="')[1:]]
        lst[date]=(date,title,related)
        order.append(date)
    return lst,order

if __name__=="__main__":
    haylo_db,haylo_order=extract_haylo_list()
    open(".build/HayloListMini.txt","w").write(repr(haylo_db))
    open(".build/HayloOrderMini.txt","w").write(repr(haylo_order))
