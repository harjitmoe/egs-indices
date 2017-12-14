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

import re, codecs, functools

def unichr4all(i):
    raise RuntimeError("function removed, not needed in recent Python 3, use chr")

def object_to_utf8(obj, ookii=False):
    raise RuntimeError("function removed")

def unichr_mslatin(n):
    raise RuntimeError("function removed")

@functools.partial(codecs.register_error, "winlatin_one_fallback")
def winlatin_one_fallback_handler(error):
    return (error.object[error.start:error.end].decode("windows-1252"), error.end)

def hybrid_to_unicode(s):
    """Given a bytes mixing Microsoft-Latin-1 with UTF-8, return it in Unicode."""
    return s.decode("utf-8", errors = "winlatin_one_fallback")

_ampersand_quasi_ellipsis = re.compile(rb"(?<!\S)&(?=\S)|(?<=\S)&(?!\S)|(?<=\")&(?=\S)|(?<=\S)&(?=\")")
def ookii_to_mslatin1(obj):
    """Convert Ookii's C0-replacement characters to Microsoft's C1-replacement characters.
    Also replaces ampersands which should be ellipses with actual ellipses."""
    return b"\x85".join(_ampersand_quasi_ellipsis.split(obj.replace(b"\x14",b"\x85").replace(b"\x18",b"\x91").replace(b"\x19",b"\x92")))
