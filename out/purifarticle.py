d2i = {}
for sect in ("ST","SB","NP"):
    f = open("dateidtemplate-"+sect+".txt","rU")
    b = f.read()
    f.close()
    b=dict([i.split("=") for i in b.replace("{{{","(").replace("}}}","))").split("{{")[1].split("}}")[0].strip().split("\n|")[1:]])
    d2i[sect]=b

del sect

kremlin=open("input.txt","rU").read()

out = ""

import re

kremlin = re.compile(r"\{\{\s*EGS-link\s*\|",re.I).split(kremlin)

out += kremlin.pop(0)

for putin in kremlin:
    wool,squeals = putin.split("}}",1)
    wool = wool.split("|")
    sect = "story"
    datemode = 1
    if wool[0].strip() == "sketchlost":
        sect = "sketch"
        wool.pop(0)
        wool.append("usemirror="+wool.pop(0).strip())
        squeals = " (lost, externally mirrored)"+squeals
    elif wool[0].strip() == "bg":
        wool.pop(0)
        trailing="|".join([""]+wool) #Leading | iff not empty
        out += "{{EGS-BG-link"+trailing+"}}"+squeals
        continue
    elif wool[0].strip()[0] in "ns":
        sect = wool[0].strip().rstrip("2")
        if wool[0].strip()[-1]=="2":
            datemode = 0
        wool.pop(0)
    #
    if not datemode:
        id=wool.pop(0).strip()
        year=wool.pop(0).strip()
        month=wool.pop(0).strip()
        day=wool.pop(0).strip()
    else:
        year=wool.pop(0).strip()
        month=wool.pop(0).strip()
        day=wool.pop(0).strip()
        try:
            id=d2i[{"story":"ST","sketch":"SB","np":"NP"}[sect]][year+"-"+month+"-"+day]
        except KeyError:
            id=None
        if id[0]=="-":
            id=None
    #Note if "polysketch" in a title (unlikely) then we in trouble.
    trailing=("|".join([""]+wool)).replace("polysketch","polyday") #Leading | iff not empty
    if not id: #i.e. none found
        out += "{{EGS-link-date|"+sect+"|"+year+"|"+month+"|"+day+trailing+"}}"
    else:
        out += "{{EGS-link-dateid|"+sect+"|"+id+"|"+year+"|"+month+"|"+day+trailing+"}}"
    out += squeals

open("output.txt","w").write(out)
f=5
