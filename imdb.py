from bs4 import BeautifulSoup
import requests
import re
import json
import time 
from lxml import html

myImage = ''
myDesc = ''
newGenre = ''

headers = {

'Host': 'www.imdb.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Cookie': 'uu=BCYvKwW25B4_tYyEKoD33JhrjcJhRWBKwBkMjDBloz1x_YjsrUXqZdZ4XV4GwIO0PDJhAZ9S2_6i%0D%0AJS3Tq0m5SuJEC5K3AyWHFsq_GEqzcMPHpJ3UW1Uw20mtHfIN-Kn2W1ElCMlcjFgKeJeuc942Srg1%0D%0AHQ%0D%0A; session-id=132-5605447-6451900; session-id-time=2082787201l; csm-hit=tb:s-4VKQT4AK9W4XN0P8TAN1|1596743630865&t:1596743632710&adb:adblk_no; ubid-main=131-9877764-3908213; session-token=VgAZZTHkm7HU3zqDCYRZZYNXQU3n2nzNy/NlQ/LpEWfMzRoAP2B/gSLAz9LxGchpaY0BBXVlMDKpbgJmkitfZnj4eE3BIsnnixQZFNPqZLc0ClI1gQJGD30Ly3pbVie4u8+XHvrYSIVvZKY+3Qn2Q4Jr7zRqnHBWMgSfM+D324YyC26l6vWHOiEp2ChwscUI; adblk=adblk_no',
'Upgrade-Insecure-Requests': '1',
'Cache-Control': 'max-age=0',
'TE': 'Trailers',
}

url = 'http://www.imdb.com/chart/top'
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]
images = [a.attrs.get('src') for a in soup.select('td.posterColumn img')]

imdb = []
index = 0
# Store each item into dictionary (data), then put those into a list (imdb)
#for index in range(0, len(movies)):
while index <  len(movies):   
    # Seperate movie into: 'place', 'title', 'year'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    try:
        url = 'https://www.imdb.com'+links[index]
       
        page = requests.get(url)
    except:
        continue
    doc = html.fromstring(str(page.content, 'utf-8'))

    img = doc.xpath('//*[@id="title-overview-widget"]/div[1]/div[3]/div[1]/a/img/@src')
    desc = doc.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[1]//text()')
    genre = doc.xpath("//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/div/a[contains(@href,'/search/title?genres=')]//text()")


    for s in img:
        myImage = s

    for text in desc:
        myDesc = text.strip()    
    
    newGenre = ', '.join(genre)
       
   
    data = {"index": index+1,
            "title": movie_title,
            "genre": newGenre,
            "description": myDesc,
            "year": year,
            "rating": ratings[index],
            "image":myImage

            }
    imdb.append(data)
    
    index = index+1
    
    if index >= 10 and index % 10 == 0:
        print(str(index))
        
    
jsonFile = open('imdb.json','w', newline='\n', encoding='utf-8')

json.dump(imdb,jsonFile,indent=4,ensure_ascii=False)
