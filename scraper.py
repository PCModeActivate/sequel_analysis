import requests
from bs4 import BeautifulSoup
import copy

def isOG(link):
    r = requests.get(link)
    html = BeautifulSoup(r.content, 'html.parser')
    prt_tag = html.find(text="Parent story:")
    prq_tag = html.find(text="Prequel:")
    return prq_tag is None and prt_tag is None

overall = []
result = []
search_queue = []
traversal_queue = []
traversed_links = set()

def traverse (link):
    if link in traversed_links:
        return
    r = requests.get(link)
    html = BeautifulSoup(r.content, 'html.parser')
    traversed_links.add(link)

    name = html.find('title').contents[0].split(" - MyAnimeList.net")[0][1:]
    score_tag = html.find('span', class_="score-label")
    
    if html.find(text="TV"):
        score = score_tag.contents[0]
        result.append(name)
        result.append(score)
    if traversal_queue:
        traversal_queue.pop(0)


    side_tag = html.find(text="Side story:")
    if side_tag is not None:
        side_tag = (side_tag.next.find_all('a'))
        for tag in side_tag:
            link = "https://myanimelist.net" + tag['href']
            if link not in traversed_links:
                traversal_queue.append(link)

    seq_tag = html.find(text="Sequel:")
    if seq_tag is not None:
        seq_tag = (seq_tag.next.find_all('a'))
        for tag in seq_tag:
            link = "https://myanimelist.net" + tag['href']
            if link not in traversed_links:
                traversal_queue.append(link)
    
    if not traversal_queue:
        return
    else:
        traverse(traversal_queue[0])
original = "https://myanimelist.net/topanime.php"
start = 8650 
page = 27 
for pgnum in range(0, page):
    print(str(pgnum*50 + start))
    r = requests.get(original + "?limit=" + str(start + pgnum * 50))
    html = BeautifulSoup(r.content, 'html.parser')
    for tag in html.find_all("a", class_="hoverinfo_trigger fl-l ml12 mr8"):
        search_queue.append(tag["href"])
    for link in search_queue:
        print(link)
        if isOG(link):
            result = []
            traversal_queue = []
            traverse(link)
            if len(result) > 2:
                overall.append(result)
    search_queue = []
    print(overall)
print (overall)
with open('anime_rating.csv', 'w') as csv:
    for row in overall:
        csv.write(','.join(row))
        csv.write("\n")
