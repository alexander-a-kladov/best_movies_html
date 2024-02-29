#!/usr/bin/python3

import requests, sys
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib
WIKI = "https://en.wikipedia.org"
URL_TEMPLATE = "https://en.wikipedia.org/wiki/List_of_American_films_of_"
FILE_NAME = "test.txt"
POSTER_PREF = "//upload.wikimedia.org/wikipedia/en/thumb/"
POSTER_PREF_SET = "//upload.wikimedia.org/wikipedia/en/"


def get_poster(movie_url):
    r1 = requests.get(WIKI+movie_url)
    soup1 = bs(r1.text, "html.parser")
    for line in soup1.find_all("td", {"class" : "infobox-image"}):
        img_line = line.next_element.next_element.next_element
        if 'src' in img_line.attrs and img_line.attrs['src'].find(POSTER_PREF) != -1:
            return urllib.parse.unquote(img_line.attrs['src'].split(POSTER_PREF)[1])
        if 'src' in img_line.attrs and img_line.attrs['src'].find(POSTER_PREF_SET) != -1:
            return urllib.parse.unquote(img_line.attrs['src'].split(POSTER_PREF_SET)[1])
    return ""

    

def parse(url = URL_TEMPLATE):
    result_list = {'href': [], 'title': [], 'poster': []}
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    print(soup.title)
    table = soup.find("caption")
    movie_list = table.next_sibling.next_sibling
    for movies in movie_list.find_all('i'):
        link = movies.contents[0]
        #print(link)
        result_list['href'].append(link.get('href'))
        result_list['title'].append(link.get('title'))
        result_list['poster'].append(get_poster(link.get('href').strip()))
    return result_list


if __name__ == "__main__":
    year = "1980"
    if len(sys.argv)>1:
        year = sys.argv[1]
    year = URL_TEMPLATE + year
    df = pd.DataFrame(data=parse(year))
    print(df)