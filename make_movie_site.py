#!/usr/bin/python3
import segno, os, sys

youtube_com = 'https://www.youtube.com/watch?v='
wikipedia = 'https://en.wikipedia.org/wiki/'
wiki_upload = 'https://upload.wikimedia.org/wikipedia/en/'
movieposters = 'https://www.movieposters.com/collections/shop?q='
autoplay = '&autoplay=1'
style_data = "<style>body {background-color:#aaaadd;}</style>\n"
info_data = ''
info_dict=dict()
html_data=dict()
distr=dict()
year=""

def read_distr(fname):
    global distr
    f = open(fname, "r")
    if f:
        for line in f.readlines():
            if line[0]=='\n':
                continue
            line = line.strip().split('\t')
            if line[0] not in distr:
                distr[line[0]] = line[1]
    f.close()


def qr_file_save(youtube_code):
    global youtube_com
    qrfile = "images/"+youtube_code+".png"
    if not os.path.isfile(qrfile):
        qrcode = segno.make_qr(youtube_com + youtube_code)
        qrcode.save(qrfile, scale=5)
    return qrfile


def add_year(new_year):
    global year, html_data
    if year != new_year:
        if year != "":
            html_data[year] += "</table>\n</body>\n</html>\n"
        if new_year not in html_data:
            year = new_year
            html_data[year] = "<html>\n"+style_data+"<body>\n<table style=\"font-size:42px;font-weight:500;\">\n"


def read_movies(fname):
    global html_data, youtube_com, wikipedia, distr
    f = open(fname, "r")
    if f:
        for line in f.readlines():
            if line[0] == '\n' or line[0] == '#':
                continue
            tokens = line.strip().split('\t')
            #print(tokens)
            add_year(tokens[4])
            html_data[year] += "<tr>\n"
            html_data[year] += "<td>" + tokens[0] + "</td>\n"
            html_data[year] += "<td><a href='"+movieposters+tokens[1].replace("'","&apos;").replace(' ','+')+"'><img src='" +wiki_upload + tokens[5]+"' width=160px height=200px></img></a></td>\n"
            html_data[year] += "<td><a href='"+ wikipedia+tokens[3].replace("'","&apos;") +"'>" + tokens[1] + "</a></td>\n"
            html_data[year] += "<td><a href='"+ wikipedia+distr[tokens[2]]+"'>"+ tokens[2]+"</a></td>\n"
            qrfile = "../"+qr_file_save(tokens[6])
            html_data[year] += "<td><a href='"+ youtube_com + tokens[6] +"'><img src='"+qrfile+"' width=200px height=200px></img></a></td>"
            key = tokens[0]+tokens[4]
            if len(info_data)>0 and key in info_dict:
                html_data[year] += "<td><a style=\"font-size:18px;\" href='"+info_data+info_dict[key]+"'>"+info_dict[key]+"</a></td>"
            html_data[year] += "</tr>\n"
    f.close()


def read_info(fname):
    f = open(fname, "r")
    if f:
        for line in f.readlines():
            tokens = line.strip().split('\t')
            if len(tokens)<3:
                continue
            key = tokens[0]+tokens[1]
            if key not in info_dict:
                info_dict[key] = tokens[2]
    f.close()


def save_index(prefix):
    global html_data
    index_html = "<html>\n<body style=\"font-size:42px;background-color:#dddd88;\">\n"
    index_html += "<p>The Most Successful Movies of the Year</p>"
    for year_key in html_data.keys():
        index_html += "<div><a href='"+"pages/"+prefix+year_key+".html'>~~~~~~~~~~~"+ year_key+"~~~~~~~~~~</a></div>"
    index_html += "</body>\n</html>\n"
    f_html = open(prefix+".html", "w")
    if f_html:
        f_html.write(index_html)
    f_html.close()


def save_html(prefix):
    global html_data, style_data
    for year_key in html_data.keys():
        f_html = open("pages/"+prefix+year_key+".html", "w")
        if f_html:
            f_html.write(html_data[year_key])
        f_html.close()


if __name__ == "__main__":
    prefix = "index"
    if len(sys.argv) > 2:
        fname = sys.argv[2]
        info_data = sys.argv[1]
        read_info(fname)
        prefix = fname.split(".txt")[0]
    read_distr("distributors.txt")
    read_movies("movies.txt")
    save_html(prefix)
    save_index(prefix)
