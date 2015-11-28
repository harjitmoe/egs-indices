# Written in 2015 by HarJIT
#
# This file is made available under the CC0 Public Domain Dedication.  To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this file to the public domain worldwide. This file is distributed without any warranty.
#
# You may have received a copy of the CC0 Public Domain Dedication along with this file. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

import json
f=open(".build/AllMegaDb.txt","rb+")
dat=eval(f.read())
f.seek(0)
f.write(json.dumps(dat))
f.truncate()
f.close()

