f=open("metadataegs2.txt","r")
id2date=eval(f.read())
f.close()
date2id=eval(open("Date2Id.txt","rU").read())

for category in ("story","sketch","np"):
    d2i=date2id[category]
    for date in sorted(d2i.keys()):
        index=category+"-"+str(d2i[date])
        if index in id2date:
            roundtrip1=id2date[index][0]
            roundtrip2=id2date[index][1]+"-"+id2date[index][3].split(" - ")[0]
            roundtrip3=id2date[index][2]
            roundtrip=(roundtrip3 if roundtrip3 else roundtrip1)
            if roundtrip1!=roundtrip2:
                print "Eh?",`category`,`date`,`d2i[date]`,`roundtrip1`,`roundtrip2`,`roundtrip3`
            if date not in (roundtrip,):
                print "Discrepancy",`category`,`date`,`d2i[date]`,`roundtrip1`,`roundtrip2`,`roundtrip3`
        else:
            print "Not grabbed",category,date,d2i[date]
