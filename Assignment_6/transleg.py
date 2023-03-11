# Wyatt Kirby
# IRK180000
# Cs 4395.001
# WebCrawler

import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import os
from nltk.tokenize import sent_tokenize


# This functions finds urls based on the initial url given. I set up limitations as I didn't want anything from a social
# media coming up in urls. I also made sure certain words I saw that seemed to be used in irrelevant urls were not
# included in the possible links that were found.
def webcrawler(url, file):
    ulist = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    count = 0
    for curlink in soup.find_all('a'):
        link_str = str(curlink.get('href'))
        if 'Trans' in link_str or 'trans' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str:
                if 'facebook' not in link_str and 'instagram' not in link_str and 'linkedin' not in link_str and 'twitter' not in link_str:
                    if 'mailto' not in link_str and 'Special' not in link_str and 'index' not in link_str and 'search' not in link_str and link_str not in ulist:
                        file.write(link_str + '\n')
                        ulist.append(link_str)
                        count += 1
        if count == 20:
            break
    return ulist


# This function makes sure that the things that are being scraped from the website are actually from the main body of
# the text.
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title'] or re.match(',!--.*-->', str((
                                                                                                              element.encode(
                                                                                                                      'utf-8')))):
        return False
    return True


def scraper(urlList):
    count = int(1)
    used_files = []
    # Making the file names needed for each website
    for url in urlList:
        num = "%s" % count
        file_name = 'Trans_Link_' + num + '.txt'

        count += 1
        # Getting the information from the website and putting it in it's file.
        with open(file_name, 'w', encoding='utf-8') as write:
            try:
                # This gathers all of the information from the website
                html = urllib.request.urlopen(url)
                soup = BeautifulSoup(html, features="html.parser")
                data = soup.findAll(string=True)
                result = filter(visible, data)
                temp_list = list(result)
                temp_str = ' '.join(temp_list)
                write.write(temp_str)
                write.close()
                used_files.append(
                    file_name)  # Wanted to get the names of all of the files that were created and filled.
            except:
                # This is triggered if there are issues harvesting the information from the website used. This is most
                # likely caused by anit-scraping bots on the websites. I honestly didn't want to bother trying to get
                # around those bots, though it is possible.
                print("Cannot scrape this website: ", url)
                write.close()
                os.remove(file_name)
    return used_files


# This function is for removing redundant \n and \t as well as extra spaces. It also separates the file by adding \n
# between sentences.
def filesent(filelist):
    for fileUse in filelist:
        raw_text = ''
        # I probably could have done this in a more efficient way by nesting one of the opens in the other but this
        # works and I'm too lazy to change it.
        with open(fileUse, 'r', encoding='utf-8') as rfile:
            raw_text = rfile.read()
            rfile.close()
        with open(fileUse, 'w', encoding='utf-8') as wfile:
            raw_text = re.sub("\t", " ", raw_text)
            raw_text = re.sub("\n", " ", raw_text)
            raw_text = re.sub(r'\[[^)]*\]', "", raw_text)
            raw_text = re.sub("\s\s+", " ", raw_text)
            wfile.write(raw_text)
            wfile.close()
        with open(fileUse, 'r', encoding='utf-8') as rfile:
            file_text = rfile.read()
            rfile.close()
            sentences = sent_tokenize(file_text)
        with open(fileUse, 'w', encoding='utf-8') as wfile:
            for sent in sentences:
                wfile.write(sent + "\n")
            wfile.close()


if __name__ == '__main__':

    # I used a google search as my url to try and get the most diverse set of links possible
    url = 'https://www.google.com/search?q=trans+legislation&rlz=1C1ONGR_enUS1027US1027&sxsrf=AJOqlzVCJkvR7joR-Hah7blK3rNTE4BAYw%3A1678565234974&ei=ct8MZMvhOo-2qtsPioyeoAs&ved=0ahUKEwjL4r_k1tT9AhUPm2oFHQqGB7QQ4dUDCBA&uact=5&oq=trans+legislation&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQ6BwgjELACECc6BwgAEA0QgAQ6BggAEB4QDToECAAQHjoFCAAQhgNKBAhBGAFQnAZYsjBgwDJoAXAAeACAAVyIAYMJkgECMTeYAQCgAQHAAQE&sclient=gws-wiz-serp'

    # This will save all of the urls found by the crawler
    with open('urls3.txt', 'w', encoding='utf-8') as wFile:
        ulist = webcrawler(url, wFile)
        wFile.close()

    # This shows all the links found to the user. I couldn't decide how I wanted to output this info, so I did a basic
    # print as well as writing to a file.
    for link in ulist:
        print(link + '\n')

    text_scraped = scraper(ulist)
    filesent(text_scraped)

    # This saves the names of all the files correctly generated for easy access with the other program
    with open('filename3.txt', 'w', encoding='utf-8') as wFile:
        for file in text_scraped:
            wFile.write(file + '\n')
        wFile.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
