d2i = {}
for sect in ("ST","SB","NP"):
    f = open("dateidtemplate-"+sect+".txt","rU")
    b = f.read()
    f.close()
    b=dict([i.split("=") for i in b.replace("{{{","(").replace("}}}","))").split("{{")[1].split("}}")[0].strip().split("\n|")[1:]])
    d2i[sect]=b

del sect

myinp = open("input.txt","rU").read()

out = ""

import re

myinp = re.compile(r"\{\{\s*EGS-link\s*\|",re.I).split(myinp)

out += myinp.pop(0)

for part in myinp:
    tcall, text = part.split("}}",1)
    tcall = tcall.split("|")
    sect = "story"
    datemode = 1
    if tcall[0].strip() == "sketchlost":
        sect = "sketch"
        tcall.pop(0)
        tcall.append("usemirror="+tcall.pop(0).strip())
        text = " (lost, externally mirrored)"+text
    elif tcall[0].strip() == "bg":
        tcall.pop(0)
        trailing="|".join([""]+tcall) #Leading | iff not empty
        out += "{{EGS-BG-link"+trailing+"}}"+text
        continue
    elif tcall[0].strip()[0] in "ns":
        sect = tcall[0].strip().rstrip("2")
        if tcall[0].strip()[-1] == "2":
            datemode = 0
        tcall.pop(0)
    #
    if not datemode:
        sid = tcall.pop(0).strip()
        year = tcall.pop(0).strip()
        month = tcall.pop(0).strip()
        day = tcall.pop(0).strip()
    else:
        year = tcall.pop(0).strip()
        month = tcall.pop(0).strip()
        day = tcall.pop(0).strip()
        try:
            sid = d2i[{"story":"ST","sketch":"SB","np":"NP"}[sect]][year+"-"+month+"-"+day]
        except KeyError:
            sid = None
        if sid[0] == "-":
            sid = None
    #Note if "polysketch" in a title (unlikely) then we in trouble.
    trailing = ("|".join([""] + tcall)).replace("polysketch", "polyday") #Leading | iff not empty
    if not sid: #i.e. none found
        out += "{{EGS-link-date|"+sect+"|"+year+"|"+month+"|"+day+trailing+"}}"
    else:
        out += "{{EGS-link-dateid|"+sect+"|"+sid+"|"+year+"|"+month+"|"+day+trailing+"}}"
    out += text

open("output.txt","w").write(out)
f=5
