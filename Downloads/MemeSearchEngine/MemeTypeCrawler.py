import urllib2
from lxml import html
headers = { 'User-Agent' : 'Mozilla/5.0' }

url =  "https://imgflip.com/memetemplates"
memetext = open("memetext", "wb")
links = []
while True:
    req = urllib2.Request(url, None, headers)
    f = urllib2.urlopen(req).read()
    data = f.replace('\n',' ')
    document = html.document_fromstring(data)
    anchors = document.xpath("//h3[@class='mt-title']/a")
    for anchor in anchors:
        print anchor.text
        links.append(anchor.text)
        memetext.write(anchor.text)
        memetext.write("\n")
    next = document.xpath("//a[@class='pager-next l but']")
    try:
        print next[0].get('href')
        url = "https://imgflip.com" + next[0].get('href')
    except:
        break
memetext.close()

blank_url = "https://imgflip.com/s/meme/"
for link in links:
    try:
        hyphened_link = link.replace(' ','-')
        #print hyphened_link
        req = urllib2.Request(blank_url + hyphened_link+".jpg", None, headers)
        f = urllib2.urlopen(req).read()

        with open("templates/"+hyphened_link+".jpg", "wb") as p:
            p.write(f)
    except:
        print "failed:", hyphened_link
        continue
    
