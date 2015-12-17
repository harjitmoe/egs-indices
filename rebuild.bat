@rem Written in 2015 by HarJIT
@rem
@rem This file is made available under the CC0 Public Domain Dedication.  To the extent possible under law, the author(s) have dedicated all copyright and related and neighboring rights to this file to the public domain worldwide. This file is distributed without any warranty.
@rem
@rem You may have received a copy of the CC0 Public Domain Dedication along with this file. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 
@rem
@rem -----------------------------------------------------------------
@rem
@rem Note: the above notice applies to this file specifically.  Other files may use
@rem different terms.  This note is not part of the above notice.
@rem

@rem The version supported is Python 2.7.  Some (not all) of the 
@rem system supports Python 2.5 (which isn't much use as it all has 
@rem to work or you'll break the output).  Generally no attempt at 
@rem 3k compatibility has been made.

set PYINTER=C:\python27\python
set PYINTER=ipy

@echo off
%PYINTER% rebuild.py
