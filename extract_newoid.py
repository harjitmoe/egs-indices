import json, tarfile, zipfile, utfsupport

_ookii2=zipfile.ZipFile("Ookii2.dat","r")
def open_lib2(path):
    return _ookii2.open(path.replace("\\","/"))

date2id=json.loads(open("Date2Id.txt","rU").read())

def extract_newoid():
    print(">>> extract_newoid")
    out={}
    n=0
    for sect in ("story","np","sketch"):
        d2i=date2id[sect]
        n+=1
        null=None;true=True;false=False
        our_dat=eval(open_lib2(str(n)).read()) #JSON borks
        aut=out[sect]={}
        for i in our_dat:
            for j in i["Comics"]:
                if ("ComicLinkId" in j) and j["ComicLinkId"]:
                    aut[j["ComicLinkId"]]=j["Id"],utfsupport.object_to_utf8(j["Title"],True)
                elif j["Date"] in d2i:
                    aut[d2i[j["Date"]]]=j["Id"],utfsupport.object_to_utf8(j["Title"],True)
    open(".build/newoid.txt","w").write(repr(out))
    return out

if __name__=="__main__":
    extract_newoid()
