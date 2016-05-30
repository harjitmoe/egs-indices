# egs-indices - Index agglomoration for El Goonish Shive.

## How the heck do I use this thing?

### Dependencies

The entire thing requires Python 2.7.  You might get it working on 2.5, given simplejson.  You might take it upon yourself to port it to 3k.

The "Pulling data from the EGS website" described below requires GNU wget.

### Updating the sources

Well, firstly, you need to find a way to keep NewFiles.txt and Date2Id.txt up to date - these are not designed to be updated manually, but the way which I use only works on my system as it reads from a carefully organised and filenamed offline mirror of EGS which is present on my system, and to distribute such a mirror here would be both *very* large and a blatant violation of Dan's copyright.  A dedicated JSON editor, if such a thing exists (I haven't checked), might be helpful.

Reddit Titles simply contains index pages saved (as "HTML only") from /r/elgoonishshive at different times.  Some overlap is fine.

910 Raw DBs was for the old, sadly deceased, pre-crash 910 Forum.  No equivalent system for the present forum exists at the moment.

titlebank.dat["modes"] needs to be updated every time a new storyline starts but is designed to be updated manually in a text editor.

#### Pulling data from the EGS website: (Misc Source Material)/Spiders

You may need to edit the scripts to use the correct path to a GNU wget.  Also, you need a GNU wget (not busybox).

To update the databases on official titles and date anomolies:

* Delete a.txt
* Rename metadataegs3.txt to a.txt (this is used by the script as the starting point).
* Run htmlonlyyo.py
* Force copy metadataegs3.txt into the repository root.

To check for any anomolous date lookup successes (this should not be done too frequently):

* Delete b.txt
* Rename dateswork.txt to b.txt (this is used by the script as the starting point).
* Run datecheckyo.py
* Force copy dateswork.txt to "(Misc Source Material)" (the parent directory)
* In that directory, run slurp_dateswork.py
* Force copy DatesWorkProcessed.txt into the repository root.

### Rebuilding the database

The simplest and fastest way is to run rebuild.py in the repository root, under Python 2.7.

The chain is composed of a sequence of modular operations which can be run as individual scripts in theory, and were originally, but repeatedly storing and reading the data from the disk is a tad inefficient, so rebuild.py runs them in a single process which passes data through memory.

The output will appear in the "out" directory.

