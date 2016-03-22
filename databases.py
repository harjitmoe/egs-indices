# Copyright (c) HarJIT 2015, 2016.
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

import json, tarfile, re

_ookii=tarfile.open("Ookii.dat","r:")
def open_lib(path):
    return _ookii.extractfile(path.replace("\\","/"))

def _unichr4all(n):
    """Support full-range unichr, even on narrow builds."""
    try:
        return unichr(n)
    except (ValueError, OverflowError):
        # One might expect CESU sequences in eventual UTF-8;
        # they are actually a fairly common phenomenon, possibly
        # for this reason.  Python handles this properly, though.
        #
        # Will output triple or quadruple-surrogates if needed,
        # concordant with the up-to-eight-bytes parsed by
        # _make_me_utf8 - I might be going a bit crazy with
        # the "handle every input" thing here.
        main=n-0x010000
        s=unichr(0xDC00+(main%1024))
        while 1:
            main = main//1024
            s=unichr(0xD800+(main%1024))+s
            if not (main//1024):
                return s

def _mslatinised_to_utf8(n):
    """Given a integer code-point mixing Unicode and Microsoft-Latin-1, return a UTF-8 string."""
    if n<0x100:
        return chr(n).decode("cp1252").encode("utf-8")
    else:
        return unichr(n).encode("utf-8")

def _make_me_utf8(s):
    """Given a string mixing Microsoft-Latin-1 with UTF-8, return it in UTF-8."""
    def count_ones(n):
        for i in range(8):
            if not (n&0x80):
                return i
            n=n<<1
        return 8
    ot=""
    while s:
        curchar=ord(s[0])
        s=s[1:]
        ones=count_ones(curchar)
        if ones in (0,1):
            ot+=_mslatinised_to_utf8(curchar)
        else:
            seq=s[:ones-1]
            if len(seq)<(ones-1):
                ot+=_mslatinised_to_utf8(curchar)
                continue
            s=s[ones-1:]
            nos=[]
            for tra in seq:
                if count_ones(ord(tra))!=1:
                    ot+=_mslatinised_to_utf8(curchar)
                    s=seq+s
                    break
                nos.append(ord(tra)%(2**7))
            else:
                #print seq,nos
                nos=[curchar%(2**(8-ones))]+nos
                outchar=0
                for i in nos:
                    outchar=outchar<<6
                    outchar+=i
                ot+=_mslatinised_to_utf8(outchar)
    return ot

_ampersand_quasi_ellipsis = re.compile(r"(?<!\S)&(?=\S)|(?<=\S)&(?!\S)")
def _ookii_to_mslatin1(obj):
    """Convert Ookii's C0-replacement characters to Microsoft's C1-replacement characters.
    Also replaces ampersands which should be ellipses with actual ellipses."""
    return "\x85".join(_ampersand_quasi_ellipsis.split(obj.replace("\x14","\x85").replace("\x18","\x91").replace("\x19","\x92")))

def to_utf8(obj, ookii=True):
    """Given a dict, list, tuple or string mixing Ookii- and/or Microsoft-Latin-1 with UTF-8, return it in UTF-8.
    Ookii processing (second arg) may be disabled, and must be if HTML entities in input."""
    if isinstance(obj, type({})):
        d={}
        for k,v in obj.items():
            d[to_utf8(k)]=to_utf8(v)
        return d
    elif isinstance(obj, type([])):
        return map(to_utf8,obj)
    elif isinstance(obj,type(())):
        return map(to_utf8,obj)
    elif type(obj)==type(""):
        if ookii:
            return _make_me_utf8(_ookii_to_mslatin1(obj))
        else:
            return _make_me_utf8(obj)
    else:
        return obj

def _fakejsonloads(dat):
    null=None
    true=True
    false=False
    return eval(dat,locals())

def load_ookii_record(strip):
    """Load the full Ookii record given the index card."""
    specific_db=open_lib(r"Ookii\ComicRecords\egscomicapi_%d.txt"%strip["OokiiId"]).read()
    if not specific_db:
        print>>sys.stderr,"DEAD DOOR",strip["Date"],strip["OokiiId"]
    else:
        strip.update(to_utf8(_fakejsonloads(specific_db)))

date2id=open("Date2Id.txt","rU")
date2id=json.loads(date2id.read())
lsdir=open("NewFiles.txt","rU")
lsdir=json.loads(lsdir.read())

metadataegs=open("metadataegs3.txt","rU")
metadataegs=eval(metadataegs.read())
dateswork=open("DatesWorkProcessed.txt","rU")
dateswork=eval(dateswork.read())

main_db={}
for sect in ("story","sketch","np"):
    main_db[sect]=open_lib(r"Ookii\ComicIndices\egscomicapi_%d.txt"%([None,"story","np","sketch"].index(sect)))
    main_db[sect]=to_utf8(_fakejsonloads(main_db[sect].read()))
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
titlebank=eval(titlebank.read()) #JSON apparently does not support numerical keys.

