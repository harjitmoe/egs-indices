# Written in 2014, 2015, 2016 by HarJIT.
# Portions copyright (c) HarJIT 2016.
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

# The version supported is Python 2.7.  Generally no attempt at 
# 3k compatibility has been made.  Python 2.5 requires the
# simplejson extension but is likely to work.

import __builtin__,os

modules=set()
_real_import=__import__
_raels=os.listdir(".")
class ModuleWarper(object):
    def __init__(self,nom,mod):
        object.__setattr__(self,"nom",nom)
        object.__setattr__(self,"mod",mod)
    def __getattribute__(self,attr):
        if attr.startswith("__") and attr.endswith("__") \
                and (attr not in ("__all__","__dict__")):
            return object.__getattribute__(self,attr)
        nom=object.__getattribute__(self,"nom")
        mod=object.__getattribute__(self,"mod")
        if (nom not in modules) and (nom+".py" not in _raels):
            modules.add(nom)
        return getattr(mod,attr)
    def __setattr__(self,attr,val):
        nom=object.__getattribute__(self,"nom")
        mod=object.__getattribute__(self,"mod")
        if (nom not in modules) and (nom+".py" not in _raels):
            modules.add(nom)
        return setattr(mod,attr,val)
    def __delattr__(self,attr):
        nom=object.__getattribute__(self,"nom")
        mod=object.__getattribute__(self,"mod")
        if (nom not in modules) and (nom+".py" not in _raels):
            modules.add(nom)
        delattr(mod,attr)
def __import__(nom,*args,**kw):
    return ModuleWarper(nom,_real_import(nom,*args,**kw))
__builtin__.__import__=__import__

import sys, os, shutil, utility, __builtin__

try:
    import json
except ImportError:
    import simplejson as json
    sys.modules["json"]=json

#Arkadiusz Wahlig's PCRE binding for Python 2.6+.
#Preferred to SRE if present.
try:
    #Unique module name in Arkadiusz Wahlig's binding
    #(unlike pcre, which is used in the pre-SRE re module to bind
    # to a very old PCRE which lacks sufficient syntax support)
    import _pcre
except ImportError:
    pass
else:
    import pcre
    sys.modules["re"]=pcre

# Remove build dir so existing files do not mess up regen process
shutil.rmtree(".build")

os.mkdir(".build")
try:
    os.mkdir("out")
except:
    pass

# Certain details are stored in local mirror of EGS, extract them.
# This will almost certainly only work on my system, hence
# files are not stored in build dir.
import extract_date2id
import extract_newfiles
import extract_bg_title_db
extract_date2id.extract_date2id()
extract_newfiles.extract_newfiles()
extract_bg_title_db.extract_bg_title_db()

# The HTML sets where processing is actually done
# in the build process rather than already.
from extract_classics_910 import extract_classics_910 
from extract_reddit_info import extract_reddit_info 
from extract_threads_new910 import extract_threads_new910 
from extract_haylo_list import extract_haylo_list 
from extract_haylo_hierarchy import extract_haylo_hierarchy 
classics_db = extract_classics_910()
reddit_titles,reddit_links = extract_reddit_info()
links_910new = extract_threads_new910()
haylo_db,haylo_order = extract_haylo_list()
haylo_mini_hierarchy,haylo_additional_hierarchy = extract_haylo_hierarchy()

# Generate MegaDB
from megadb_generate_initial import megadb_generate_initial
alldat = megadb_generate_initial(classics_db,haylo_db,reddit_links,links_910new)

# Add new strips
from megadb_fetch_haylonew import megadb_fetch_haylonew
from megadb_fetch_newfiles import megadb_fetch_newfiles
alldat = megadb_fetch_haylonew(alldat,haylo_additional_hierarchy,haylo_db,links_910new)
alldat = megadb_fetch_newfiles(alldat,reddit_titles,reddit_links,links_910new)

# Fetch transcripts whilst adding new titles and appearance data
import megadb_fetch_tss
import megadb_fetch_zorua
alldat=megadb_fetch_tss.megadb_fetch_tss(alldat)
alldat=megadb_fetch_zorua.megadb_fetch_zorua(alldat)

# Divide Sketchbook by ID, introduce true-arc records, pull BG
import megadb_indextransforms
import megadb_pull_bg
alldat=megadb_indextransforms.megadb_indextransforms(alldat)
alldat=megadb_pull_bg.megadb_pull_bg(alldat)

# Generate the HTML index, make JSON
import export_json
import export_html
export_json.export_json(alldat)
export_html.export_html(alldat)

# Regenerate Shiveapedia templates and docs
import export_titles_template
import export_titles_template_lite
import export_titles_template_lite2
import export_numberdatemaps
export_titles_template.export_titles_template(alldat)
export_titles_template_lite.export_titles_template_lite(alldat)
export_titles_template_lite2.export_titles_template_lite2(alldat)
export_numberdatemaps.export_numberdatemaps(alldat)

# Enter build dir
os.chdir(".build")

# Generate a combined MOBI-KF8 and then immediately split
# into MOBI (kept alone) and KF8 (converted to EPUB)
# Requires Kindlegen and KindleUnpack.
def ebooks():
    import subprocess
    print ">>> kindlegen"
    subprocess.call(["../../Tools/kindlegen_win32_v2_9\kindlegen.exe", "index.html", "-c1", "-o", "index.azw3"])
    print ">>> kindleunpack"
    subprocess.call([sys.executable, "../../Tools/KindleUnpack_v073/lib/kindleunpack.py", "-s", "index.azw3", "."])
    os.rename("mobi7-index.mobi", "index.mobi")
#ebooks()

# Copy files into output dir
def export(fp):
    fn=os.path.basename(fp)
    if os.path.exists(os.path.join("../out",fn)):
        print ">>> removing existing",fn,"from out dir"
        os.unlink(os.path.join("../out",fn))
    if os.path.exists(fp):
        print ">>> exporting",fn
        shutil.copy(fp,"../out")

export("index.mobi")
export("mobi8/index.epub")
export("index.html")
export("AllMegaDb.txt")
export("titles.txt")
export("titles_lite.txt")
export("titles_lite2.txt")
export("numbereidmap.txt")
export("numberoidmap.txt")
export("numberdibmap.txt")
export("datefakemap.txt")

# Leave build dir
os.chdir("..")

print "Used external modules:",sorted(list(modules))
