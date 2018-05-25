# Written in 2014, 2015 by Thomas Hori
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

import os, json

def extract_date2id():
    print (">>> extract_date2id")
    if not os.path.exists("../../egs/0003 - (Sketchbook and Extras)/0001 - Filler Sketchbook"):
        print ("Not running on Thomas Hori's machine, not regenerating Date2Id.txt")
        return
    lsdir=[]
    for r,ds,fs in os.walk("../../egs"):
        if ".git" not in r:
            lsdir.extend(fs)
    pl=len("ST-2010-04-23-")
    def getdate(fn):
        return fn[3:][:10], (int(fn[pl:][:5]) if fn[pl:][:5].strip("xn") else None)
    stmap=dict(list(map(getdate,[i for i in lsdir if i.startswith("ST-") and not i.lower().count("-original") and not i.lower().count("-pagecut") and not i.lower().count("-pageextend") and not i.lower().count("-remastered-sb")])))
    npmap=dict(list(map(getdate,[i for i in lsdir if i.startswith("NP-") and not i.lower().count("-original") and not i.lower().count("-colour-official")])))
    sbmap=dict(list(map(getdate,[i for i in lsdir if i.startswith("SB-") and not i.lower().count("-original") and not i.lower().count("-xxxxx")])))
    if stmap and npmap and sbmap:
        open("Date2Id.txt","w").write(json.dumps({"story":stmap,"sketch":sbmap,"np":npmap}))

if __name__=="__main__":
    extract_date2id()
