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

import re

unichr4all = chr # Not needed anymore in current Python 3k. versions

def unichr_mslatin(n):
    """Given a integer code-point mixing Unicode and Microsoft-Latin-1, return a Unicode string."""
    if n<0x100:
        return bytes([n]).decode("cp1252")
    else:
        return chr(n)

# Equivalent to bs4.UnicodeDammit.detwingle(...), should I use that?
def hybrid_to_unicode(s):
    """Given a bytes mixing Microsoft-Latin-1 with UTF-8, return it in UTF-8."""
    def count_ones(n):
        for i in range(8):
            if not (n&0x80):
                return i
            n=n<<1
        return 8
    ot=""
    while s:
        curchar=s[0]
        s=s[1:]
        ones=count_ones(curchar)
        if ones in (0,1):
            ot+=unichr_mslatin(curchar)
        else:
            seq=s[:ones-1]
            if len(seq)<(ones-1):
                ot+=unichr_mslatin(curchar)
                continue
            s=s[ones-1:]
            nos=[]
            for tra in seq:
                if count_ones(tra)!=1:
                    ot+=unichr_mslatin(curchar)
                    s=seq+s
                    break
                nos.append(tra%(2**7))
            else:
                #print seq,nos
                nos=[curchar%(2**(8-ones))]+nos
                outchar=0
                for i in nos:
                    outchar=outchar<<6
                    outchar+=i
                ot+=unichr_mslatin(outchar)
    return ot

_ampersand_quasi_ellipsis = re.compile(rb"(?<!\S)&(?=\S)|(?<=\S)&(?!\S)|(?<=\")&(?=\S)|(?<=\S)&(?=\")")
def ookii_to_mslatin1(obj):
    """Convert Ookii's C0-replacement characters to Microsoft's C1-replacement characters.
    Also replaces ampersands which should be ellipses with actual ellipses."""
    return b"\x85".join(_ampersand_quasi_ellipsis.split(obj.replace(b"\x14",b"\x85").replace(b"\x18",b"\x91").replace(b"\x19",b"\x92")))

def object_to_utf8(obj, ookii=False):
    raise RuntimeError("function removed")
