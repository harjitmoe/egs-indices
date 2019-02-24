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

f=open("dateswork.txt")
idat=eval(f.read())
f.close()

map={"DateStatedAboveComic":"WorksExternal","DateInBrowserTitle":"WorksInternal"}

spatulae={}

odat={"story":{},"sketch":{},"np":{}}

for i in list(idat.keys()):
    if idat[i]==None:
        continue
    section,dtyp,id=i.split("-")
    id=int(id)
    odat[section][id]={}
    date,path=idat[i]
    if path not in spatulae:
        spatulae[path]=0
    else:
        #if spatulae[path]:print path
        spatulae[path]+=1

for i in list(idat.keys()):
    if idat[i]==None:
        continue
    section,dtyp,id=i.split("-")
    id=int(id)
    date,path=idat[i]
    works=spatulae[path]<2 #not a recurring image (i.e. current comic)
    odat[section][id][map[dtyp]]=(works,date)

for s,sodat in list(odat.items()):
    lastid=0
    for id in sorted(sodat.keys()):
        if (id-lastid)!=1:
            print(s,id,lastid)
        lastid=id

f=open("DatesWorkProcessed.txt","w")
f.write(repr(odat))
f.close()
