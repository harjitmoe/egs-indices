# Copyright (c) Thomas Hori 2015.
#
#  THIS WORK IS PROVIDED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES,
#  INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT WILL THE AUTHORS OR CONTRIBUTORS
#  BE HELD LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE),
#  ARISING IN ANY WAY OUT OF THE USE OF THIS WORK, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
#  Permission is granted to anyone to use this work for any purpose, including
#  commercial applications, and to alter it and/or redistribute it freely in any
#  form, with or without modification, subject to the following restrictions:
#
#  1. The origin of this work must not be misrepresented; you must not claim that
#     you authored the original work. If you use this work in a product, an
#     acknowledgment in the product documentation would be appreciated but is not
#     required.
#
#  2. Altered versions in any form must not be misrepresented as being the 
#     original work, and neither the name of Thomas Hori nor the names of authors or
#     contributors may be used to endorse or promote products derived from this
#     work without specific prior written permission.
#
#  3. The text of this notice must be included, unaltered, with any distribution.
#

import utility

def extract_reddit_info():
    print (">>> extract_reddit_info")
    initiator='<a class="title may-blank " href="http://www.egscomics.com/'
    init2='<li class="first"><a href="'
    #
    reddit_titles={"story":{},"sketch":{},"np":{}}
    reddit_links={"story":{},"sketch":{},"np":{}}
    #
    import os
    files=os.listdir("Reddit Titles")
    for file in files:
        f=open("Reddit Titles/"+file)
        b=f.read().replace("loggedin ","").replace("outbound ","").replace("&#32;"," ")
        b=utility.deentity(b,3)
        f.close()
        b=b.replace("https://","http://")
        while initiator in b:
            b=b.split(initiator,1)[1]
            #Very old links break this
            if ".jpg" in b.split('"',1)[0]:
                continue #Cannot parse, forget it.
            if "?date" in b.split('"',1)[0]:
                continue #Cannot parse, forget it.
            type,b=b.split("?id=",1)
            id,b=b.split('"',1)
            id=int(id.split("&")[0])
            type={"egsnp":"np","index":"story","sketchbook":"sketch","filler":"sketch","":"story"}[type.split(".")[0].strip("/")]
            b=b.split(">",1)[1]
            title,b=b.split('</a>',1)
            title=utility.deentity(title,2)
            b=b.split(' by <a href="http://www.reddit.com/user/',1)[1]
            submitter,b=b.split('"',1)
            if "Comic for" not in title and "Sketchbook for" not in title: #Older links, dates given rather than titles
                if id!=1974: #Haven't time to work out what went badly wrong here
                    reddit_titles[type][id]=title+" ("+submitter+")"
            b=b.split(init2,1)[1]
            link,b=b.split('"',1)
            if id!=1974: #Haven't time to work out what went badly wrong here
                reddit_links[type][id]=(link,False)
    f=open("Megathread.dat")
    iterator=iter(f)
    link=iterator.next().rstrip()
    submitter=iterator.next().rstrip()
    for line in iterator:
        line=line.rstrip()
        id,title=line.split(" ",1)
        id=int(id)
        reddit_titles["sketch"][id]=title+" ("+submitter+")"
        reddit_links["sketch"][id]=(link,False)
    f.close()
    return reddit_titles,reddit_links

if __name__=="__main__":
    reddit_titles,reddit_links = extract_reddit_info()
    open(".build/reddit_titles.txt","w").write(repr(reddit_titles))
    open(".build/reddit_threads.txt","w").write(repr(reddit_links))
