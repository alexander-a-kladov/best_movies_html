#!/usr/bin/python3
import segno, os, sys, requests

autoplay = '&autoplay=1'
style_data = "<style>body {background-color:#aaaadd;}</style>\n"
info_data = ''
info_dict=dict()
html_data=dict()
config=dict()
distr=dict()
year=""


def download_poster(youtube_code):
    global config
    url = config['cover'] + youtube_code + '/maxresdefault.jpg'
    local_f = "images/"+youtube_code+".png"
    if not os.path.isfile(local_f):
        r = requests.get(url)
        f = open(local_f, 'wb')
        for chunk in r.iter_content(chunk_size=512 * 1024): 
            if chunk:
                f.write(chunk)
        f.close()
    return local_f


def load_config():
    global config
    movie_file = "movies_"
    f = open("config.txt", "r")
    if f:
        line = f.readline().strip()
        movie_file += line.split('#')[1]
        movie_file += ".txt"
        for line in f.readlines():
            line = line.strip()
            if len(line)>0 and line[0]!='#':
                tokens = line.split('\t')
                if tokens[0] not in config:
                    config[tokens[0]]=tokens[1]
    f.close()
    return movie_file


def read_distr(fname):
    global distr
    f = open(fname, "r")
    if f:
        for line in f.readlines():
            if line[0]=='\n':
                continue
            line = line.strip().split('\t')
            if line[0] not in distr:
                distr[line[0]] = [line[1]]
                if len(line)>2:
                    distr[line[0]].append(line[2])
    f.close()


def qr_file_save(youtube_code):
    global config
    qrfile = "images/"+youtube_code+".png"
    if not os.path.isfile(qrfile):
        qrcode = segno.make_qr(config['trailer'] + youtube_code)
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


def read_movies(fname, prefix):
    global html_data, youtube_com, wikipedia, distr
    f = open(fname, "r")
    if f:
        for line in f.readlines():
            if line[0] == '\n' or line[0] == '#':
                continue
            tokens = line.strip().split('\t')
            if len(tokens)<7:
                continue
            #print(tokens)
            add_year(tokens[4])
            html_data[year] += "<tr>\n"
            html_data[year] += "<td>" + tokens[0] + "</td>\n"
            html_data[year] += "<td><a href='"+config['buy_poster']+tokens[1].replace("'","&apos;").replace(' ','+')+"'><img src='" + config['poster'] + tokens[5]+"' width=160px height=200px></img></a></td>\n"
            html_data[year] += "<td><a href='"+ config['wiki']+tokens[3].replace("'","&apos;") +"'>" + tokens[1] + "</a></td>\n"
            if len(distr[tokens[2]])>1:
                logo = "<img src='"+ distr[tokens[2]][1] +"' width=200px height=100px>"
            else:
                logo = distr[tokens[2]][0]
            html_data[year] += "<td><a href='"+ config['wiki']+distr[tokens[2]][0]+"'>"+logo+"</a></td>\n"
            qrfile = "../"+download_poster(tokens[6])
            html_data[year] += "<td><a href='"+ config['trailer'] + tokens[6] +"'><img src='"+qrfile+"' width=300px height=200px></img></a></td>\n"
            key = tokens[0]+tokens[4]
            if len(info_data)>0 and key in info_dict:
                if len(info_dict[key].split("\t"))>1:
                    link = info_dict[key].split("\t")[0]


                    rem  = info_dict[key].split("\t")[1]
                else:
                    link = info_dict[key]
                    rem  = ""
                html_data[year] += "<td><a style=\"font-size:18px;\" href='"+info_data+link.replace("'","&apos;")+"'><img src='../images/play.png' width=100px height=100px></a></td>"
                html_data[year] += "<td><a style=\"font-size:18px;\">"+rem+"</td>\n"
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
                if len(tokens)>3:
                    info_dict[key]+="\t"+tokens[3]
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
    movie_file_name = load_config()
    read_distr("distributors.txt")
    read_movies(movie_file_name, prefix)
    save_html(prefix)
    save_index(prefix)

