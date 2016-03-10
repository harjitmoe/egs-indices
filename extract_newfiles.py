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

import os, json

def getdate_st(fn):
    pl=len("ST-2010-04-23-")
    return fn[3:][:10],(int(fn[pl:][:5]),fn[pl+6:][:-4])

def getdate_sb(fn):
    pl=len("NP-2010-04-23-")
    return fn[3:][:10]+"/"+fn[pl:][:5],(fn[3:][:10],int(fn[pl:][:5]),fn[pl+6:][:-4])

def getdate_np(fn):
    pl=len("NP-2010-04-23-")
    return fn[3:][:10],(int(fn[pl:][:5]),fn[pl+6:][:-4])

def extract_newfiles():
    print (">>> extract_newfiles")
    if not os.path.exists("../../egs/0003 - (Sketchbook and Extras)/0001 - Filler Sketchbook"):
        print ("Not running on HarJIT's machine, not regenerating NewFiles.txt")
        return
    #
    stmap=[]
    sbmap=[]
    npmap=[]
    for r,ds,fs in os.walk("../../egs"):
        if ".git" not in r:
            for i in fs:
                if i.startswith("ST-"):
                    stmap.append(i)
                elif i.startswith("SB-"):
                    sbmap.append(i)
                elif i.startswith("NP-"):
                    npmap.append(i)
    stmap=dict(map(getdate_st,filter(lambda i:not i.lower().count("-original") and not i.lower().count("-remastered-sb"),stmap)))
    sbmap=dict(map(getdate_sb,filter(lambda i:i.lower().count("-00"),sbmap)))
    npmap=dict(map(getdate_np,filter(lambda i:not i.lower().count("-original") and not i.lower().count("-remastered-sb") and not i.lower().count("-colour-official"),npmap)))
    open("NewFiles.txt","w").write(json.dumps({"story":stmap,"sketch":sbmap,"np":npmap}))

if __name__=="__main__":
    extract_newfiles()
