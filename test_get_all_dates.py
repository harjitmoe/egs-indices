try:
    import json
except ImportError:
    import simplejson as json
import utility
alldat=json.loads(open(".build/AllMegaDb.txt","rU").read())
dates=None
def proc(node):
    if node[u"RecordType"]==u"Comic":
        if node[u"Date"]!=u"?":
            dates.append(node[u"Date"].encode("utf-8"))
        return
    #
    if node[u"RecordType"]==u"Section":
        nxtgen=u"StoryArcs"
    elif node[u"RecordType"]==u"StoryArc":
        nxtgen=u"StoryLines"
    elif node[u"RecordType"]==u"StoryLine":
        nxtgen=u"Comics"
    else:
        raise ValueError(node[u"RecordType"].encode("utf-8"))
    for child in node[nxtgen]:
        proc(child)
for section in alldat:
    if section[u"Title"]==u"Backgrounds":
        continue
    dates=[]
    proc(section)
    open("alldates-%s.txt"%utility.ookii2egslink[section[u"Title"]],"wb").write(json.dumps(dates))
