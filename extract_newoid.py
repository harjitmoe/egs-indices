# Copyright (c) HarJIT 2016, 2017.
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

import json, tarfile, zipfile, utfsupport, ast

_ookii2 = zipfile.ZipFile("Ookii2.dat", "r")


def open_lib2(path):
    return _ookii2.open(path.replace("\\", "/"))


date2id = json.loads(open("Date2Id.txt", "rU").read())


def extract_newoid():
    print(">>> extract_newoid")
    out = {}
    n = 0
    for sect in ("story", "np", "sketch"):
        d2i = date2id[sect]
        n += 1
        null = None
        true = True
        false = False
        our_dat = ast.literal_eval(open_lib2(str(n)).read())  #JSON borks
        aut = out[sect] = {}
        for i in our_dat:
            for j in i["Comics"]:
                if ("ComicLinkId" in j) and j["ComicLinkId"]:
                    aut[j["ComicLinkId"]] = j["Id"], utfsupport.object_to_utf8(
                        j["Title"], True)
                elif j["Date"] in d2i:
                    aut[d2i[j["Date"]]] = j["Id"], utfsupport.object_to_utf8(
                        j["Title"], True)
    open(".build/newoid.txt", "w").write(repr(out))
    return out


if __name__ == "__main__":
    extract_newoid()
