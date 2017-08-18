# Copyright (c) Thomas Hori 2015, 2016, 2017.
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

import json, yaml, tarfile
import utfsupport

_ookii=tarfile.open("Ookii.dat","r:")
def open_lib(path):
    return _ookii.extractfile(path.replace("\\","/"))

_transcipts=tarfile.open("Transcripts.tar","r:")
def open_tss(path):
    return _transcipts.extractfile(path.replace("\\","/"))

def load_ookii_record(strip):
    """Load the full Ookii record given the index card."""
    specific_db = open_lib(r"Ookii\ComicRecords\egscomicapi_%d.txt"%strip["OokiiId"]).read()
    specific_db = utfsupport.hybrid_to_unicode(utfsupport.ookii_to_mslatin1(specific_db))
    if not specific_db:
        print("DEAD DOOR",strip["Date"],strip["OokiiId"], file=sys.stderr)
    else:
        try:
            psdb = json.loads(specific_db)
        except ValueError:
            psdb = yaml.safe_load(specific_db)
        strip.update(psdb)

date2id = open("Date2Id.txt","rU")
date2id = json.loads(date2id.read())
lsdir = open("NewFiles.txt","rU")
lsdir = json.loads(lsdir.read())

# true and True are both YAML, as are null, Null, NULL but not None
_p = lambda s: s.replace(": None", ": null")

metadataegs = open("metadataegs3.txt","rU")
metadataegs = yaml.safe_load(_p(metadataegs.read()))
dateswork = open("DatesWorkProcessed.txt","rU")
dateswork = yaml.safe_load(_p(dateswork.read().replace("(", "[").replace(")", "]")))

main_db={}
for sect in ("story","sketch","np"):
    main_db[sect] = open_lib(r"Ookii\ComicIndices\egscomicapi_%d.txt"%([None,"story","np","sketch"].index(sect)))
    _deco = utfsupport.hybrid_to_unicode(utfsupport.ookii_to_mslatin1(main_db[sect].read()))
    try:
        _pdeco = json.loads(_deco)
    except ValueError:
        _pdeco = yaml.safe_load(_deco)
    main_db[sect] = _pdeco
del sect

def _parse_suddenlaunch(sect):
    sdb={}
    f=open("suddenlaunch.dat","rU")
    b=f.read().split("\n")
    f.close()
    for record in b:
        url,section,date=record.split(" ")
        if section in {"sketch":("Filler",),"story":("Story","Comic")}[sect]:
            month,day,year=date.split("/") #MM/DD/YYYY (middle endian)
            date="-".join((year,month,day)) #YYYY-MM-DD (big endian)
            sdb[date]=url
    return sdb
suddenlaunch_db={}
suddenlaunch_db["story"]=_parse_suddenlaunch("story")
suddenlaunch_db["sketch"]=_parse_suddenlaunch("sketch")
suddenlaunch_db["np"]={}

titlebank=open("titlebank.dat","rU")
titlebank=yaml.safe_load(titlebank.read())

