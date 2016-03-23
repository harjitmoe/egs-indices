# Written in 2015 by Thomas Hori
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

import json,os

def extract_bg_title_db():
    print (">>> extract_bg_title_db")
    if not os.path.exists(r"../../egs/0003 - (Sketchbook and Extras)/0001 - Filler Sketchbook"):
        print ("Not running on Thomas Hori's machine, not regenerating Bg*.txt")
        return
    db={}
    dbt={}
    ls=["backgrounds_0.html","backgrounds_1.html","backgrounds_2.html","backgrounds_3.html","backgrounds_4.html","backgrounds_5.html","backgrounds_6.html"]
    keyphrase="alt='EGS Background #"
    for cell in ls:
        f=open("../../egsbg/"+cell,"rU")
        b=f.read().split(keyphrase)[1:]
        f.close()
        for celluolus in b:
            id=celluolus[:4]
            title=celluolus.split("<b>",1)[1].split("</b>",1)[0].strip()
            text=celluolus.split("<br>",3)[3].split("</td>",1)[0].strip()
            db[id]=title
            dbt[id]=text

    if db and dbt:
        open("BgNames.txt","w").write(json.dumps(db))
        open("BgDescriptions.txt","w").write(json.dumps(dbt))

if __name__=="__main__":
    extract_bg_title_db()
