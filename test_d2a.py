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

f=open("metadataegs3.txt","r")
id2date3=eval(f.read())
f.close()
date2id=eval(open("Date2Id.txt","rU").read())

for category in ("story","sketch","np"):
    d2i=date2id[category]
    for date in sorted(d2i.keys()):
        index=d2i[date]
        if index in id2date3[category]:
            roundtrip1=id2date3[category][index]["DateInBrowserTitle"]
            roundtrip2=id2date3[category][index]["DateStatedAboveComic"]
            roundtrip=(roundtrip2 if roundtrip2 else roundtrip1)
            if roundtrip1!=roundtrip:
                print "Eh?",`category`,`date`,`d2i[date]`,`roundtrip1`,`roundtrip2`
            if date not in (roundtrip,):
                print "Discrepancy",`category`,`date`,`d2i[date]`,`roundtrip1`,`roundtrip2`
        else:
            print "Not grabbed",category,date,d2i[date]
