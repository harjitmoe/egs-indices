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


def kasplit(s):
    o = ""
    h = 0
    for n in s:
        if n == "<" and not h:
            h = 1
        if not h:
            if n in " \t\r\n\v\f":
                if o[-1] != " ":
                    o += " "
            else:
                o += n
        if n == ">" and h:
            h = 0
    return o


def extract_haylo_hierarchy():
    print(">>> extract_haylo_hierarchy")
    f = open("HayloList.html")
    b = f.read().replace("www.egscomics.com",
                         "egscomics.com").replace("/index.php?", "/?")
    b = utility.deentity(b, 3)
    f.close()
    #XXX this ignores headings
    b = b.split('<em > \n        <strong>')[1:]
    hier = []
    addhier = []
    counting = 0
    for bb in b:
        title = utility.deentity(kasplit(bb.split("</em >")[0]).strip(), 2)
        if title == "The Dawn - Family Tree":
            counting = 1
        ba = [
            i.split("</p>")[0]
            for i in bb.split('<p style="margin-left:10.2em; \n')[1:]
        ]
        hier2 = []
        for record in ba:
            date = record.split(
                '<a href="http://egscomics.com/?date=')[1].split('"')[0]
            hier2.append(date)
        hier.append((title, hier2))
        if counting:
            addhier.append((title, hier2))
    return hier, addhier


if __name__ == "__main__":
    haylo_mini_hierarchy, haylo_additional_hierarchy = extract_haylo_hierarchy(
    )
    open(".build/HayloHierarchyMini.txt",
         "w").write(repr(haylo_mini_hierarchy))
    open(".build/HayloHierarchyAdditional.txt",
         "w").write(repr(haylo_additional_hierarchy))
