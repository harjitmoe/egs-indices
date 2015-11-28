f=open("BgNames.txt","rU")
b=eval(f.read()) #Blatantly no security, assume trust
f.close()

f=open("BgDescriptions.txt","rU")
c=eval(f.read()) #Blatantly no security, assume trust
f.close()

comics=[]

gifs=[0,1,2,3,4,5,6,7,826,27,28,29,30,31,32,33,34,35,36,38,45,48,54,55]

def formurl(idst):
    #Not eval(idst) because starting a number with 0 means octal in Py2 (a nice gotcha for newbies) and is invalid in Py3
    ext = "_1280x960.gif" if int(idst,10) in gifs else "_1280x960.jpg"
    return "http://egscomics.com/bg/egs_bg_"+idst+ext

for i in sorted(c.keys()):
    title=b[i]
    comment=c[i]
    comics.append({"ReactionLinks": [], "SharedDateIndex": 0, "OokiiId": -1, "DateIndexable": False, "Section": "Backgrounds", "RecordType": "Comic", "Titles": {"Official": title}, "Characters": None, "Date": "?", "Commentary": comment, "Transcript": None, "Id": int(i,10), "SpecialUrl": formurl(i)})

alldat=eval(open(".build/AllMegaDb.txt","rU").read())
alldat.append({"Title":"Backgrounds","StoryArcs":comics,"RecordType":"Section"})
open(".build/AllMegaDb.txt","w").write(repr(alldat))