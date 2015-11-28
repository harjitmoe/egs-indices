# Written in 2015 by HarJIT
#
# This file is made available under the CC0 Public Domain Dedication.  To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this file to the public domain worldwide. This file is distributed without any warranty.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

import json

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
