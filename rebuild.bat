@rem The version supported is Python 2.7.  Some (not all) of the 
@rem system supports Python 2.5 (which isn't much use as it all has 
@rem to work or you'll break the output).  Generally no attempt at 
@rem 3k compatibility has been made.

set PYINTER=C:\Python27\python

@echo off
%PYINTER% rebuild.py
