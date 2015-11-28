from htmlentitydefs import name2codepoint,codepoint2name

def deentity(data):
    for name in name2codepoint.keys():
        if name!="amp":
            data=data.replace("&"+name+";",unichr(name2codepoint[name]).encode("utf8"))
    for number in range(0x100):
        name="#"+str(number)
        data=data.replace("&"+name+";",unichr(number).encode("utf8"))
    data=data.replace("&amp;","&")
    return data

def strip_comments(data):
    try:
        data="".join([i.split("-->",1)[1] for i in ("-->"+data+"-->").split("<!--")])
        if data.endswith("-->"):
            data=data[:-3]
        return data
    except:
        global foo
        foo=data
        raise

def strip_style(data):
    try:
        data="".join([i.split('"',1)[1] for i in ('"'+data).split(' style="')])
        return data
    except:
        global foo
        foo=data
        raise
    
f=open("metadataegs2.txt","r")
d=eval(f.read())
f.close()
d2={}

for index in sorted(d.keys()):
    prefix,id=index.split("-")
    if prefix not in d2.keys():
        d2[prefix]={}
    id=int(id)
    date1=d[index][0]
    date2,title=(d[index][1]+"-"+d[index][3]+" ").split(" ",1)
    title=title.strip(" -")
    date2=date2.strip(" -")
    date3=d[index][2]
    if date2[0] not in "0123456789":
        title=date2+" "+title
        date2=""
    if title and title[0] in "0123456789":
        date2=date2+" "+title
        title=""
    if not date1:
        date1=date2
    if date1!=date2:
        raise AssertionError
    commentary=strip_style(strip_comments(d[index][4])).replace(' target="_blank"','').replace('<div id="newsheader"></div>',"").replace("<div>","<br />").replace("</div>","").strip()
    d2[prefix][id]={"Commentary":commentary,"Id":id,"DateStatedAboveComic":(date3 or None),"DateInBrowserTitle":(date1 or None),"HtmlComicTitle":(title or None)}

f=open("metadataegs3.txt","w")
f.write(repr(d2))
f.close()
