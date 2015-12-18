# Written in 2014, 2015 by HarJIT
#
# This file is made available under the CC0 Public Domain Dedication.  To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this file to the public domain worldwide. This file is distributed without any warranty.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
#
# -----------------------------------------------------------------
#
# Note: the above notice applies to this file specifically.  Other files may use
# different terms.  This note is not part of the above notice.
#

# The version supported is Python 2.7.  Some (not all) of the 
# system supports Python 2.5 (which isn't much use as it all has 
# to work or you'll break the output).  Generally no attempt at 
# 3k compatibility has been made.

import sys, os, shutil, json, utility

# Remove build dir so existing files do not mess up regen process
shutil.rmtree(".build")

os.mkdir(".build")
try:
    os.mkdir("out")
except:
    pass

def execfile2(fp):
    print>>sys.stderr, "\n"+os.getcwd()+">\""+sys.executable+"\" \""+fp+"\""
    module=type(shutil)("__main__") #if __name__=="__main__" checks
    execfile(fp, module.__dict__)

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
import extract_classics_910
import extract_reddit_info
import extract_threads_new910
import extract_haylo_list
import extract_haylo_hierarchy
extract_classics_910.extract_classics_910()
extract_reddit_info.extract_reddit_info()
extract_threads_new910.extract_threads_new910()
extract_haylo_list.extract_haylo_list()
extract_haylo_hierarchy.extract_haylo_hierarchy()

# Generate MegaDB
import megadb_generate_initial
alldat=megadb_generate_initial.megadb_generate_initial()

# Add new strips
import megadb_fetch_haylonew
import megadb_fetch_newfiles
alldat=megadb_fetch_haylonew.megadb_fetch_haylonew(alldat)
alldat=megadb_fetch_newfiles.megadb_fetch_newfiles(alldat)

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
utility.save_alldat(alldat) #for modules still using the slightly older system.

# Regenerate Shiveapedia templates and docs
execfile2("export_titles_template.py")
execfile2("export_titles_template_lite.py")
execfile2("export_titles_template_lite2.py")
execfile2("export_numberdatemaps.py")

# Generate the HTML index, make JSON
import export_html
import export_json
export_html.export_html(alldat)
export_json.export_json(alldat)

# Enter build dir
os.chdir(".build")

# Generate a combined MOBI-KF8 and then immediately split
# into MOBI (kept alone) and KF8 (converted to EPUB)
# Requires Kindlegen and KindleUnpack.
# ..\..\Tools\kindlegen_win32_v2_9\kindlegen index.html -c1 -o index.azw3
# python ..\..\Tools\KindleUnpack_v073\lib\kindleunpack.py -s index.azw3 .
# ren mobi7-index.mobi index.mobi

# Copy files into output dir
def export(fp):
    fn=os.path.basename(fp)
    if os.path.exists(os.path.join("../out",fn)):
        os.unlink(os.path.join("../out",fn))
    if os.path.exists(fp):
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
