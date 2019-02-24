# Written in 2015 by HarJIT
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

import json, utility

def export_json(dat):
    print (">>> export_json")
    f=open(".build/AllMegaDb.txt","w")
    json.dump(dat,f)
    f.close()

if __name__=="__main__":
    sections=utility.open_alldat()
    export_json(sections)
