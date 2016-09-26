# egs-indices - Index agglomeration for El Goonish Shive.

## How the heck do I use this thing?

### Dependencies

The entire thing requires Python 2.7.  You might get it working on 2.5, given simplejson.  You might take it upon yourself to port it to 3k.

The "Extracting titles and date information from the EGS website" described below requires GNU wget.

### Updating the sources

Well, firstly, you need to find a way to keep NewFiles.txt and possibly also Date2Id.txt up to date - these are not designed to be updated manually, but the way which I use only works on my system as it reads from a carefully organised and filenamed offline mirror of EGS which is present on my system, and to distribute such a mirror here would be both large and a blatant violation of Dan's copyright.  A dedicated JSON editor, if such a thing exists (I haven't checked), might be helpful.

Reddit Titles simply contains index pages saved (as "HTML only") from /r/elgoonishshive at different times.  Some overlap is fine.

910 Raw DBs was for the old, sadly deceased, pre-crash 910 Forum.  No equivalent system for the present forum exists at the moment.

titlebank.dat["modes"] needs to be updated every time a new storyline starts but is designed to be updated manually in a text editor.

#### Extracting titles and date information from the EGS website

The following takes place in "(Misc Source Material)/Spiders" unless otherwise specified.

You may need to edit the scripts to use the correct path to a GNU wget.  Also, you need a GNU wget (not busybox).

To update the databases on official titles and date anomalies:

* Delete a.txt
* Rename metadataegs3.txt to a.txt (this is used by the script as the starting point).
* Run htmlonlyyo.py
* Press RETURN (Enter) after the script has finished.
* Force copy metadataegs3.txt into the repository root.

To check for any anomalous date lookup successes (this should not be done too frequently):

* Delete b.txt
* Rename dateswork.txt to b.txt (this is used by the script as the starting point).
* Run datecheckyo.py
* Press RETURN (Enter) after the script has finished.
* Force copy dateswork.txt to "(Misc Source Material)" (the parent directory)
* In that directory, run slurp_dateswork.py
* Force copy DatesWorkProcessed.txt into the repository root.

### Rebuilding the database

The simplest and fastest way is to run rebuild.py in the repository root, under Python 2.7.

The chain is composed of a sequence of modular operations which can be run as individual scripts in theory, and were originally, but repeatedly storing and reading the data from the disk is rather inefficient, so rebuild.py runs them in a single process which passes data through memory.

The output will appear in the "out" directory.

## File by file

### Launcher

file(s)|description
---|---
rebuild.bat|loads rebuild.py (sometimes means less typing on Windows, and makes it easy to specify a path to Python by editing it)
rebuild.py|runs the process modules, in order, keeping the database in memory.

### Shared

file(s)|description
---|---
utfsupport.py|lenient UTF-8 support, Ookii character-set support, and code to work around narrow Python builds.
databases.py|access to the various database files.
utility.py|assorted code useful for multiple processes.  sorted into more detailed headings in the module itself.

### Data

file(s)|description
---|---
"910 Raw DBs/" and "Classics 910/"|rest in peace for now.
"(Misc Source Material)/"|source material for some of the other databases, notably the code for updating metadataegs3.txt.
"Reddit Titles/"|various index pages saved (as "HTML only") from /r/elgoonishshive at different times - for titles and reaction links.
alldates*.txt|output of test_get_all_dates.py, used by extract_theads_new910 for anomaly detection
BgNames.txt and BgDescriptions.txt|metadata of legacy backgrounds.  this will not change in the foreseeable future.
Date2Id.txt|mapping of dates to IDs.  not entirely reliable in event of multi-SB days.  still used although there is no need to.  see also NewFiles.txt
DatesWorkProcessed.txt|data about what can and cannot be looked up using a date-scheme URL.
HayloList.html|data from Haylo's fan-site regarding strip titles and reaction links.  no longer accessible at the original site I don't think.
NewFiles.txt|date-ID and filename-title data for, in the current version, actually all comics.
Megathread.dat|data from Reddit about the assigned titles, title assigner and discussion URL from the megathread for the 17-SB day.
metadataegs3.txt|metadata obtained from the website itself - do not attempt to edit this directly, see "Extracting titles and date information from the EGS website" above.
Ookii.dat|the Ookii database (by strip, not by character) saved using the internal AJAX-JSON API.  stored as an uncompressed tarball to save disk footprint (many, many files significantly below 4k is a worst-case scenario for size-footprint ratio).
suddenlaunch.dat|URLs for reaction threads on the briefly-used Suddenlaunch forum.
titlebank.dat|assorted titles, as well as storyline boundary information.  human-readable and designed to be edited in a text editor.
titleharjit.py|titles by HarJIT.
Transcripts.dat|another uncompressed tarfile, extract this the parent folder (it contains a directory called "Transcripts") if you want to do anything with it.
zorua_db.dat|Zorua's EGS-NP titles and appearance data, obtained from the now-dead pre-crash 910 forum.

### Build processes

#### Data preprocessing (extract_*)

file(s)|description
---|---
extract_date2id.py, extract_newfiles.py, extract_bg_title_db.py|these only do anything on my system.
extract_classics_910.py|extract information from the "Classics 910" directory, for what use it is to anyone now.
extract_reddit_info.py|extract information from the "Reddit Titles" directory.
extract_threads_new910.py|extract information from the "910 Raw DBs" directory, for what use it is to anyone anymore.
extract_haylo_list.py, extract_haylo_hierarchy.py|process HayloList.html

#### Database formation (megadb_*)

file(s)|description
---|---
megadb_generate_initial.py|generate the portion of the database covered by the Ookii database, using that as a framework, but adding information from other sources.
megadb_fetch_haylonew.py|further generate database entries for those Story comics covered by HayloList.html but not Ookii.dat
megadb_fetch_newfiles.py|add the remaining database entries using NewFiles.txt and building upon it.
megadb_fetch_tss.py|fetch transcripts and obtain titles for some strips (titlebank.dat and titleharjit.py and others)
megadb_fetch_zorua.py|add Zorua information from zorua_db.dat
megadb_indextransforms.py|reorganise Story database to the arc-line hierarchy used by EGS, and reorganise SB by year.
megadb_pull_bg.py|add entries for legacy backgrounds.

#### Exporting data to files (export_*)

file(s)|description
---|---
export_json.py|store the entire database as a JSON file (AllMegaDb.txt).
export_html.py|generate a HTML index of EGS strips (index.html).
export_titles_template.py|generate a MediaWiki template containing all titles (titles.txt).
export_titles_template_lite.py|generate a MediaWiki template containing official titles (titles_lite2.txt).
export_numberdatemaps.py|generate MediaWiki tables describing sequential numbering, lookup IDs and date information (*map.txt).

### Peripheral and diagnostic tools (test_*)

These are not connected with rebuild.py, and tend not to be part of a typical build sequence.

file(s)|description
---|---
test_get_all_dates.py|generate alldates*.txt allowing up-to-date meaningful warning output from extract_theads_new910.py (this should not be necessary in the shortly foreseeable future).
test_d2a.py|tool for looking for possible errors in date-to-ID mapping.

### Output files (in out/)

file(s)|description
---|---
AllMegaDb.txt|JSON of the entire database.
index.html|HTML index of EGS strips.
titles.txt|MediaWiki template database of titles.
titles_lite2.txt|MediaWiki template database of titles - only official titles to save space.
*map.txt|various MediaWiki tables describing sequential numbering, lookup IDs and date information (*map.txt).







