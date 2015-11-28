# Written in 2014, 2015 by HarJIT
#
# This file is made available under the CC0 Public Domain Dedication.  To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this file to the public domain worldwide. This file is distributed without any warranty.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

import os, json
lsdir=[]
for r,ds,fs in os.walk(r"..\..\egs"):
    if ".git" not in r:
        lsdir.extend(fs)
pl=len("ST-2010-04-23-")
def getdate(fn):
    return fn[3:][:10],int(fn[pl:][:5])

stmap=dict(map(getdate,filter(lambda i:i.startswith("ST-") and not i.lower().count("-original") and not i.lower().count("-remastered-sb"),lsdir)))
npmap=dict(map(getdate,filter(lambda i:i.startswith("NP-") and not i.lower().count("-original") and not i.lower().count("-colour-official"),lsdir)))
sbmap=dict(map(getdate,filter(lambda i:i.startswith("SB-") and not i.lower().count("-original") and not i.lower().count("-xxxxx"),lsdir)))

if stmap and npmap and sbmap:
    open("Date2Id.txt","w").write(json.dumps({"story":stmap,"sketch":sbmap,"np":npmap}))
