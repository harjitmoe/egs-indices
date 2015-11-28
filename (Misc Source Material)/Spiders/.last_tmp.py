import re, os, time

i = 1
dab={}
#wget="..\\wget.exe"
wget="wget-gnu"
names={"index":"story","egsnp":"np","sketchbook":"sketch"}

if os.path.exists("a.txt"):
    f=open("a.txt")
    dab=eval(f.read())
    f.close()

for interface in ("index","egsnp","sketchbook"):
    fs=0
    print "I",interface
    while 1:
        try:
            if names[interface]+"-"+str(i) not in dab.keys():
                url = "http://www.egscomics.com/"+interface+".php?id="+str(i)
                #time.sleep(0.5)
                os.system(wget+" -O \""+interface+".php@id="+str(i)+"\" \""+url+"\" >> wgetlog.txt 2>&1")
                if not os.path.exists(interface+".php@id="+str(i)):
                    print "A"
                    continue
                rd = open(interface+".php@id="+str(i),"rU")
                data = rd.read()
                rd.close()
                os.unlink(interface+".php@id="+str(i))
                res = re.search("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]</title>", data)
                res2 = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
                if not res2:
                    print "F",i
                    fs+=1
                    if fs>=5:
                        i=1
                        break
                    else:
                        i+=1
                        continue
                else:
                    fs=0
                comment=data.split('<div id="newsarea">',1)[1].split('<div id="boxad">',1)[0]
                date1=""
                if res:
                    date1=res.group()[:-8]
                title=""
                date2=""
                if 'title="' in data:
                    date2,title=(data.split('title="',1)[1].split('"',1)[0]+"-").split("-",1)
                    date2=date2.strip()
                    title=title.strip().rstrip("-")
                date3=""
                if '">Comic for ' in data:
                    date3=data.split('">Comic for ',1)[1].split("</div>",1)[0].split(", ",1)[1]
                    date3=date3.replace(", "," ")
                    month,day,year=date3.split(" ",3)
                    month="%02d"%([None,"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(month[:3]))
                    day="%02d"%int(day)
                    date3=year+"-"+month+"-"+day
                dab[names[interface]+"-"+str(i)]=(date1,date2,date3,title,comment)
            else:
                fs=0
        except Exception,e:
            print "Pfail",i,str(e)
        i += 1

f=open("metadataegs2.txt","w")
f.write(`dab`)
f.close()

raw_input()