import re, os, time

i = 1
dab={}
#wget="..\\wget.exe"
wget="wget"
names={"index":"story","egsnp":"np","sketchbook":"sketch"}

f=open("metadataegs3.txt")
dob=eval(f.read())
f.close()

for interface in ("index","egsnp","sketchbook"):
  for styla in ("DateInBrowserTitle","DateStatedAboveComic"):
    fs=0
    sub=dob[names[interface]]
    print "I",interface
    while 1:
        if i not in sub.keys():
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
        try:
            if names[interface]+"-"+str(i) not in dab.keys():
                url = "http://www.egscomics.com/"+interface+".php?date="+(sub[i][styla])
                #time.sleep(0.5)
                os.system(wget+" -O \""+interface+".php@id="+str(i)+"\" \""+url+"\" >> wgetlog.txt 2>&1")
                if not os.path.exists(interface+".php@id="+str(i)):
                    print "A"
                    continue
                rd = open(interface+".php@id="+str(i),"rU")
                data = rd.read()
                rd.close()
                os.unlink(interface+".php@id="+str(i))
                res2 = re.search("comics/[-a-zA-Z0-9_()]*.(jpg|gif|png)", data)
                works=sub[i][styla]
                if not res2:
                    works=None
                dab[names[interface]+"-"+styla+"-"+str(i)]=(works,res2.group())
            else:
                fs=0
        except Exception,e:
            print "Pfail",i,str(e)
        i += 1

f=open("dateswork.txt","w")
f.write(`dab`)
f.close()

raw_input()
