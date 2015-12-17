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

import os

def extract_newfiles():
    print (">>> extract_newfiles")
    if not os.path.exists(r"..\..\egs\0003 - (Sketchbook and Extras)\0001 - Filler Sketchbook"):
        print ("Not running on HarJIT's machine, not regenerating NewFiles.txt")
        return
    stmap=[]
    for r,ds,fs in os.walk(r"..\..\egs\0001 - Main Story"):
        if ".git" not in r:
            stmap.extend(fs)
    pl=len("ST-2010-04-23-")
    def getdate(fn):
        return fn[3:][:10],(int(fn[pl:][:5]),fn[pl+6:][:-4])
    stmap=dict(map(getdate,filter(lambda i:i.startswith("ST-") and not i.lower().count("-original") and not i.lower().count("-remastered-sb"),stmap)))

    sbmap=[]
    for r,ds,fs in os.walk(r"..\..\egs\0003 - (Sketchbook and Extras)\0001 - Filler Sketchbook"):
        if ".git" not in r:
            sbmap.extend(fs)
    pl=len("NP-2010-04-23-")
    def getdate(fn):
        return fn[3:][:10]+"/"+fn[pl:][:5],(fn[3:][:10],int(fn[pl:][:5]),fn[pl+6:][:-4])
    sbmap=dict(map(getdate,filter(lambda i:i.startswith("SB-") and i.lower().count("-00"),sbmap)))

    lsdir=[]
    for r,ds,fs in os.walk(r"..\..\egs\0002 - EGS-NP"):
        if ".git" not in r:
            lsdir.extend(fs)
    pl=len("NP-2010-04-23-")
    def getdate(fn):
        return fn[3:][:10],(int(fn[pl:][:5]),fn[pl+6:][:-4])
    lsdir=dict(map(getdate,filter(lambda i:i.startswith("NP-") and not i.lower().count("-original") and not i.lower().count("-remastered-sb") and not i.lower().count("-colour-official"),lsdir)))

    if stmap and lsdir and sbmap:
        open("NewFiles.txt","w").write(repr({"story":stmap,"sketch":sbmap,"np":lsdir}))

if __name__=="__main__":
    extract_newfiles()
