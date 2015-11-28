f=open("dateswork.txt")
idat=eval(f.read())
f.close()

map={"DateStatedAboveComic":"WorksExternal","DateInBrowserTitle":"WorksInternal"}

spatulae={}

odat={"story":{},"sketch":{},"np":{}}

for i in idat.keys():
    section,dtyp,id=i.split("-")
    id=int(id)
    odat[section][id]={}
    date,path=idat[i]
    if path not in spatulae:
        spatulae[path]=0
    else:
        #if spatulae[path]:print path
        spatulae[path]+=1

for i in idat.keys():
    section,dtyp,id=i.split("-")
    id=int(id)
    date,path=idat[i]
    works=spatulae[path]<2 #not a recurring image (i.e. current comic)
    odat[section][id][map[dtyp]]=(works,date)

for s,sodat in odat.items():
    lastid=0
    for id in sorted(sodat.keys()):
        if (id-lastid)!=1:
            print s,id,lastid
        lastid=id

f=open("DatesWorkProcessed.txt","w")
f.write(repr(odat))
f.close()