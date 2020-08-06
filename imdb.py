from bs4 import BeautifulSoup
import requests
import re
import json
import time 
from lxml import html

myImage = ''

url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
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
    for s in img:
        myImage = s
   
    data = {"index": index+1,
            "movie_title": movie_title,
            "year": year,
            "rating": ratings[index],
            "image":myImage
            }
    imdb.append(data)
    
    index = index+1
    
    if index > 10 and index % 10 == 0:
        print(str(index))
    
jsonFile = open('imdb.json','w', newline='\n', encoding='utf-8')

json.dump(imdb,jsonFile,indent=4,ensure_ascii=False)
