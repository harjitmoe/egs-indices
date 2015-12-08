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

import pprint
pprint.pprint(eval(open("SbMegaDb.txt","rU").read()),open("SbMegaDb pprint.txt","w"))
pprint.pprint(eval(open("SbMegaDb old.txt","rU").read()),open("SbMegaDb old pprint.txt","w"))