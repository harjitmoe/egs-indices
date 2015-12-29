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

try:
    import json
except ImportError:
    import simplejson as json
import utility
alldat=json.loads(open(".build/AllMegaDb.txt","rU").read())
dates=None
def proc(node):
    if node[u"RecordType"]==u"Comic":
        if node[u"Date"]!=u"?":
            dates.append(node[u"Date"].encode("utf-8"))
        return
    #
    if node[u"RecordType"]==u"Section":
        nxtgen=u"StoryArcs"
    elif node[u"RecordType"]==u"StoryArc":
        nxtgen=u"StoryLines"
    elif node[u"RecordType"]==u"StoryLine":
        nxtgen=u"Comics"
    else:
        raise ValueError(node[u"RecordType"].encode("utf-8"))
    for child in node[nxtgen]:
        proc(child)
for section in alldat:
    if section[u"Title"]==u"Backgrounds":
        continue
    dates=[]
    proc(section)
    open("alldates-%s.txt"%utility.ookii2egslink[section[u"Title"]],"wb").write(json.dumps(dates))
