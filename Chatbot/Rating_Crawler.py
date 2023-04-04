import re
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'https://www.imdb.com/title/tt4642970/reviews'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html5lib')
    ratings = soup.findAll('div', attrs = {'class':'text show-more__control'})
    with open('llama_ratings.txt', 'w', encoding='utf-8') as wfile:
        for rate in ratings:
            rate = rate.__str__()
            rate = re.sub('<div class="text show-more__control">', ' ', str(rate))
            rate = re.sub('<br/><br/>Tmelapse<br/><br/>', ' ', rate)
            rate = re.sub('<br/><br/>', ' ', rate)
            rate = re.sub('\n', ' ', rate)
            rate = re.sub('\n', ' ', rate)
            rate = re.sub('</div>', '\n', rate)
            wfile.write(rate)
        wfile.close()
