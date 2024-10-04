#!/usr/bin/python3

import requests, sys
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib
WIKI = "https://en.wikipedia.org"
URL_TEMPLATE = "https://en.wikipedia.org/wiki/List_of_American_films_of_"
POSTER_PREF = "//upload.wikimedia.org/wikipedia/en/thumb/"
POSTER_PREF_SET = "//upload.wikimedia.org/wikipedia/en/"
POSTER_PREF_COMMON = "//upload.wikimedia.org/wikipedia/commons/thumb/"
DISTRIBUTORS = dict()


def load_distributors():
    f = open("distributors.txt","r")
    if f:
        for line in f.readlines():
            if not len(line.strip()):
                continue
            tokens = line.strip().split('\t')
            name = tokens[0]
            link = tokens[1]
            try:
                logo = tokens[2]
            except:
                logo = ""
            DISTRIBUTORS[link] = [name, logo]
        f.close()


def get_poster(r1):
    soup1 = bs(r1.text, "html.parser")
    for line in soup1.find_all("td", {"class" : "infobox-image"}):
        img_line = line.next_element.next_element.next_element
        if 'src' in img_line.attrs and img_line.attrs['src'].find(POSTER_PREF) != -1:
            return urllib.parse.unquote('en/'+img_line.attrs['src'].split(POSTER_PREF)[1])
        if 'src' in img_line.attrs and img_line.attrs['src'].find(POSTER_PREF_SET) != -1:
            return urllib.parse.unquote('en/'+img_line.attrs['src'].split(POSTER_PREF_SET)[1])
        if 'src' in img_line.attrs and img_line.attrs['src'].find(POSTER_PREF_COMMON) != -1:
            return urllib.parse.unquote('commons/'+img_line.attrs['src'].split(POSTER_PREF_COMMON)[1])
    return ""


def update_distributors(link, text):
    if link.split('/wiki/')[1] not in DISTRIBUTORS:
        r = requests.get(WIKI+link)
        soup = bs(r.text, "html.parser")
        logo = ""
        try:
            img_line = soup.find("td", {"class" : "infobox-image logo"})
            img_line = img_line.next_element.next_element.next_element
            logo = 'https:'+urllib.parse.unquote(img_line.attrs['src'].split('thumb/')[0] + img_line.attrs['src'].split('thumb/')[1].split('/220px')[0])
        except:
            pass
        print(logo)
        DISTRIBUTORS[link.split('/wiki/')[1]] = [text, logo]
        return text
    return DISTRIBUTORS[link.split('/wiki/')[1]][0]


def get_distributor(r1):
    soup1 = bs(r1.text, "html.parser")
    distr_by = soup1.find(text="Distributed by")
    if distr_by:
        link = distr_by.next_element.next_element
        try:
            if link.get('href') and link.text:
                return update_distributors(link.get('href'), link.text)
        except:
            pass
    return link.text


def save_distributors():
    f_distr = open("distributors.txt", "w")
    for link in DISTRIBUTORS:
        f_distr.write(DISTRIBUTORS[link][0]+'\t'+link+'\t'+DISTRIBUTORS[link][1]+'\n')
    f_distr.close()


def parse(year):
    url = URL_TEMPLATE + year
    result_list = {'rank' :[], 'title': [], 'distributor': [], 'href': [], 'year': [], 'poster': [], 'trailer': []}
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    print(soup.title)
    table = soup.find("caption")
    movie_list = table.next_sibling.next_sibling
    rank = 1
    for movies in movie_list.find_all('i'):
        link = movies.contents[0]
        text = link.text
        try:
            print(link.text, link.get('href'))
        except:
            link = movies.previous_element
            print(text, link.get('href'))
        result_list['rank'].append(str(rank))
        result_list['href'].append(urllib.parse.unquote(link.get('href').split('/wiki/')[1]))
        result_list['title'].append(text)
        r1 = requests.get(WIKI+link.get('href'))
        result_list['poster'].append(get_poster(r1).split('/220px')[0])
        result_list['year'].append(year)
        result_list['trailer'].append("")
        result_list['distributor'].append(get_distributor(r1))
        rank += 1
    return result_list


if __name__ == "__main__":
    year = "1980"
    load_distributors()
    if len(sys.argv)>1:
        year = sys.argv[1]
    df = pd.DataFrame(data=parse(year))
    df.to_csv(year+'_movies_en.txt', sep='\t', index=False)
    save_distributors()
