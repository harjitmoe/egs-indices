@rem The version supported is Python 2.7.  Some (not all) of the 
@rem system supports Python 2.5 (which isn't much use as it all has 
@rem to work or you'll break the output).  Generally no attempt at 
@rem 3k compatibility has been made.

@rem Remove build dir so existing files do not mess up regen process
rmdir /Q /S .build

mkdir .build
mkdir out

@rem Certain details are stored in local mirror of EGS, extract them.
@rem This will almost certainly only work on my system, hence
@rem files are not stored in build dir.
@rem Edit: try to contain damage on fail cases.  I still recommend
@rem other users to @rem-out or delete these though.
C:\Python27\python extract_date2id.py
C:\Python27\python extract_newfiles.py
C:\Python27\python extract_bg_title_db.py

@rem The HTML sets where processing is actually done
@rem in the build process rather than already.
C:\Python27\python extract_classics_910.py
C:\Python27\python extract_reddit_info.py
C:\Python27\python extract_threads_new910.py
C:\Python27\python extract_haylo_list.py
C:\Python27\python extract_haylo_hierarchy.py

@rem Generate MegaDB
C:\Python27\python megadb_generate_initial.py

@rem Add new strips
C:\Python27\python megadb_fetch_haylonew.py
C:\Python27\python megadb_fetch_newfiles.py

@rem Fetch transcripts whilst adding new titles and appearance data
C:\Python27\python megadb_fetch_tss.py
C:\Python27\python megadb_fetch_zorua.py

@rem Divide Sketchbook by ID, introduce true-arc records, pull BG
C:\Python27\python megadb_indextransforms.py
C:\Python27\python megadb_pull_bg.py

@rem Regenerate Shiveapedia templates and docs
C:\Python27\python export_titles_template.py > .build\titles.txt
C:\Python27\python export_titles_template_lite.py > .build\titles_lite.txt
C:\Python27\python export_titles_template_lite2.py > .build\titles_lite2.txt
C:\Python27\python export_numberdatemaps.py

@rem Generate the HTML index, make JSON
C:\Python27\python export_html.py > .build\index.html
C:\Python27\python megadb_jsonise.py

@rem Enter build dir
cd .build

@rem Generate a combined MOBI-KF8 and then immediately split
@rem into MOBI (kept alone) and KF8 (converted to EPUB)
@rem Requires Kindlegen and KindleUnpack.
@rem ..\..\Tools\kindlegen_win32_v2_9\kindlegen index.html -c1 -o index.azw3
@rem C:\Python27\python ..\..\Tools\KindleUnpack_v073\lib\kindleunpack.py -s index.azw3 .
@rem ren mobi7-index.mobi index.mobi

@rem Copy files into output dir
del ..\out\index.mobi
copy index.mobi ..\out
del ..\out\index.epub
copy mobi8\index.epub ..\out
del ..\out\index.html
copy index.html ..\out
del ..\out\index.html
copy index.html ..\out
del ..\out\AllMegaDb.txt
copy AllMegaDb.txt ..\out
del ..\out\titles.txt
copy titles.txt ..\out
del ..\out\titles_lite.txt
copy titles_lite.txt ..\out
del ..\out\titles_lite2.txt
copy titles_lite2.txt ..\out
del ..\out\numbereidmap.txt
copy numbereidmap.txt ..\out
del ..\out\numberoidmap.txt
copy numberoidmap.txt ..\out
del ..\out\numberdibmap.txt
copy numberdibmap.txt ..\out
del ..\out\datefakemap.txt
copy datefakemap.txt ..\out

@rem Leave build dir
cd ..
