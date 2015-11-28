#!/usr/bin/env python
# -*- python -*-
"""fetch transcripts, fix titles"""

from titlebank import *

# Copyright (c) HarJIT 2014, 2015.
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
#  commercial applications, and to alter and/or distribute it freely in any form,
#  with or without modification, provided that the following conditions are met:
#
#  1. The origin of this work must not be misrepresented; you must not claim that
#     you authored the original work. If you use this work in a product, an
#     acknowledgment in the product documentation would be appreciated but is not
#     required.
#
#  2. Altered versions in any form may not be misrepresented as being the original
#     work, and neither the name of HarJIT nor the names of authors or
#     contributors may be used to endorse or promote products derived from this
#     work without specific prior written permission.
#
#  3. The text of this notice must be included, unaltered, with any distribution.

mytitles={

#Source: HarJIT (own)

1665:"Make Me Stay",1736:"Feline rumours",1737:"Nothing makes sense",1738:"That's one enormous bandwagon",1739:"Sarah has a good heart",1740:"Mongoose Diane",1741:"Catalina's plan",1742:"Creepy Catalina",1743:"Train wreck",1744:"It's fine",1745:"Success despite idiocy",1746:"Wait a minute",1747:"Who is Ronin",1748:"Cecil making waves",1749:"Oh Susan",1750:"Hammer Queen",1751:"Susan is a badass",
#yeah, I am deferring the use of Ashley's name for a reason
1752:"Ponytail girl is angry",1753:"Fun on the beach",1754:"Elliot is adorable",1755:"Glaring Grace",1756:"Explain what happened",1757:"Good question",1758:"Grace, use hug!",1759:"Happy to hug... or not",1760:"I have better friends now",1761:"Thoughtful Justin",1762:"Insightful Justin",1763:"Logic... or not",1764:"I am the captain",1765:"Scheming Tom",1767:"That's half of the protagonists",1766:"Spartacus, eh?",1768:"Conflicted",1769:"Jumping to conclusions",1770:"Meet new people",1771:"Awkward",1772:"Yeah, absolutely nobody",1773:"Victory... wait, what?",1774:"Overactive imagination",1775:"Cutting it close",1776:"Watched and seen",1777:"Everything's fine if it's got pandas",
#May use it now
1778:"Want a lookout?",1779:"No, Elliot, it wasn't",1780:"Want to watch",1781:"Manipulative Tom",1782:"Dramatic Ashley",1783:"Tom's tactics",1784:"Misconceptions... or not",1785:"Open confession",1786:"Awkward Ashley",1787:"Enthusiastic Ashley",1788:"Chessmaster Tom",1789:"Not interested",1790:"Totally unsuspicious",1791:"Concealed no longer",1792:"Fantastic liar",1793:"Everyone's a liar",1794:"The truth",1795:"Something more now",1796:"Hugs",1797:"About time",1798:"Nervous Ashley",1799:"Easier",1800:"Not an idiot",1801:"Susan is SO COOL",1802:"You don't say, Sarah",1803:"They will date!",1804:"Boing, Tedd?  Boing?",1805:"No, seriously, don't ask.",1806:"Shocking!",1807:"Sexuality euphamism fail!",1808:"Susan stunned",1809:"Hair hug!",1810:"Wake up, sheeple!",1811:"Introducing good Tom",1812:"Cecil is the odd one out",1813:"Ronin realises",1814:"Go easy on Justin, it's a whole schoolday of significant events!",1815:"This seems to amount to a good summary of Susan's romantic history.",1816:"A useful insight into the mind of Diane",1817:"Diane realises"

}

sbmytitles={

#Source: HarJIT (own)

708:"Hair, the Reprise",709:"Party Heidi",710:"Fairy Nanase is Fairylike",711:"Clone-army",712:"Cross my heart",714:"Wardrobe functions",715:"Oblivious Wand V2",716:"Because staves are cool",717:"Chromabunnies",718:"Fatcat Grace",719:"Semi-mammalian",720:"Clingy",721:"Nanase storms in",722:"Unconventional walking styles",723:"Fluffy Susan",724:"Sure thing",725:"Griffin with map",726:"Lesbians Who Have Kissed Elliot Count = 2 (thankyou SMJB, EGS Strip Slaying, Page 271)",727:"Fluffy Susan 2",729:"Did You See (Her) Coming",728:"Too many people at once?",730:"But why",731:"Introducing Tom",732:"Adorable Elliot",733:"Dreamy Elliot/Tedd",734:"It'd better be",735:"Manners",736:"Captain of my destiny",737:"Withdrawn",738:"Harassed by my dreams",739:"Pink?",740:"Angry girl is angry",741:"Dreamy Elliot/Tedd, the Reprise",742:"The power of script",743:"Christmas Sketchbook 2013",744:"You... transformed",745:"The power of size",746:"Panel time",747:"Doom",748:"Has caused an error in KERNEL32.DLL",749:"Body swap shenanigans",750:"Genius, frankly?",751:"Psychic Elliot",752:"Beg pardon?",753:"Puppy",754:"Susan, you SO COOL!",755:"Hufflepuff!",757:"BOING! 757",758:"Yearn to brush it",759:"Switched",760:"Up for battle",761:"Solitude",762:"Company",763:"Coordinated",764:"Balance",765:"Vampiric",766:"Seductive"

}

import os,utility

alldat=eval(open(".build/AllMegaDb.txt","rU").read())
for arc in utility.specific_section(alldat,"story")["StoryArcs"]:
    for strip in arc['Comics']:
        if os.path.exists("..\\Transcripts\\"+strip['Date']+".txt"):
            #print strip["Date"]
            transcript=open("..\\Transcripts\\"+strip['Date']+".txt","rU").read()
            #Thank goodness for Python mutables
            #I can change strip and it also changes in alldat
            # on account of referencing the same object
            strip["Transcript"]=utility.scour(transcript.rstrip("\n")+"\n\n")
        else:
            #print strip['Date']
            strip["Transcript"]=None
        if ("Official" not in strip['Titles']):
            if strip['Id'] in megatitles:
                strip['Titles']["Official"]=megatitles[strip['Id']]
            if strip['Id'] in mytitles:
                strip['Titles']["HarJIT"]=mytitles[strip['Id']]
            if strip['Id'] in titles:
                strip['Titles']["Tumblr"]=titles[strip['Id']]

locals().update(utility.open_dbs("sketch"))
marker="<strong>Requested by"
marker2="<strong><a href=\"http://www.patreon.com/egscomics\">Requested</a> by"
marker3="<strong><a href=\"http://www.patreon.com/egscomics\"> Requested</a> by"
marker4="<strong> Requested</strong></a><strong> by"
for arc in utility.specific_section(alldat,"sketch")["StoryArcs"]:
    for strip in arc['Comics']:        
        if ("Official" not in strip['Titles']):
            if strip['Id'] in sbmytitles:
                strip['Titles']["HarJIT"]=sbmytitles[strip['Id']]
            if strip['Id'] in sbmegatitles: #NOT elif
                strip['Titles']["Official"]=sbmegatitles[strip['Id']]
            elif strip['Id'] in metadataegs: #YES elif
                c=utility.dirty(metadataegs[strip['Id']]["Commentary"])
                if c.count(marker):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                elif c.count(marker2):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker2,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                elif c.count(marker3):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker3,1)[1].split("</p>",1)[0].split("<br />",1)[0])
                elif c.count(marker4):
                    strip['Titles']["Official"]="Requested by"+utility.detag(c.split(marker4,1)[1].split("</p>",1)[0].split("<br />",1)[0])

open(".build/AllMegaDb.txt","w").write(repr(alldat))
