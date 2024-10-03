#!/usr/bin/python3
import segno, os, sys, requests

style_data = "<style>body {background-color:#aaaadd;}</style>\n"
info_data = ''
info_data1 = ''
info_dict=dict()
html_data=dict()
index_img_dict=dict()
config=dict()
distr=dict()
year=""


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


def add_year(prefix, new_year):
    global year, html_data, index_img_dict
    if year != new_year:
        if year != "":
            html_data[year] += "</table>\n</body>\n</html>\n"
        if new_year not in index_img_dict:
            index_img_dict[new_year]=[]
        if new_year not in html_data:
            year = new_year
            html_data[year] = "<html>\n"+style_data+"<body>\n"
            html_data[year] += "<div style=\"font-size:42px;\">"
            html_data[year] += "<a href='../"+prefix+".html'><img src=../images/film.png height=50px></a>"
            html_data[year] += "<a href='"+config['wiki']+year+"_in_film'>"+year+"</a></div>"
            html_data[year] += "<table style=\"font-size:42px;\">\n"


def read_movies(fname, prefix):
    global html_data, youtube_com, wikipedia, distr, info_data, info_data1
    f = open(fname, "r")
    if f:
        for line in f.readlines():
            if line[0] == '\n' or line[0] == '#':
                ##print(line.strip())
                continue
            tokens = line.strip().split('\t')
            if len(tokens)<6:
                print(tokens)
                ##print(line.strip())
                continue
            #print(tokens)
            ##tokens[5] = 'en/'+tokens[5]
            ##print('\t'.join(tokens))
            add_year(prefix, tokens[4])    
            key = tokens[0]+tokens[4]
            link = ""
            rem  = ""
            if len(info_data)>0:
                if key in info_dict:
                    if len(info_dict[key].split("\t"))>1:
                        link = info_dict[key].split("\t")[0]
                        rem  = info_dict[key].split("\t")[1]
                    else:
                        link = info_dict[key]

            html_data[year] += "<tr>\n"
            html_data[year] += "<td>" + tokens[0] + "</td>\n"
            html_data[year] += "<td><a href='"+ config['trailer_search'] + (tokens[1].replace("'", "&apos;")+" "+year+" trailer").replace(" ", "+")+"'>\n"
            html_data[year] += "<img src='" + config['poster'] + tokens[5].replace("'","&apos;")+"' width=150px height=200px></a></td>\n"
            index_img_dict[year].append("<img src='" + config['poster'] + tokens[5].replace("'","&apos;")+"' width=75px height=100px>\n")
            if len(link)>0:
                html_data[year] += "<td><a href='"+info_data+link.replace("'","&apos;")+"'><img src='../images/play.png' width=100px height=100px></a>\n"
            else:
                if info_data1:
                    html_data[year] += "<td><a href='"+info_data1+tokens[1].replace("'","&apos;")+ "' target=_blank><img src='../images/search.png' width=100px height=100px></a>\n"
                else:
                    html_data[year] += "<td>\n"
            html_data[year] += "<a href='"+ config['wiki']+tokens[3].replace("'","&apos;") +"'>" + tokens[1] + "</a></td>\n"
            try:
                if len(distr[tokens[2]])>1:
                    logo = "<img src='"+ distr[tokens[2]][1] +"' width=200px height=100px>"
                else:
                    logo = distr[tokens[2]][0]
            except:
                print(tokens)
                print("Error")
                sys.exit()

            html_data[year] += "<td><a href='"+ config['wiki']+distr[tokens[2]][0]+"'>"+logo+"</a></td>\n"
            html_data[year] += "<td><a style=\"font-size:18px;\">"+rem+"</td>\n"
            html_data[year] += "</tr>\n"
    f.close()


def read_info(fname):
    global info_data, info_data1
    f = open(fname, "r")
    if f:
        line = f.readline()
        if line[0]=='#':
            tokens = line[1:].split('\t')
            info_data = tokens[0]
            if len(tokens)==2:
                info_data1 = tokens[1]
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
    global html_data, index_img_dict
    index_html = "<html>\n<body style=\"font-size:42px;background-color:#dddd88;\">\n"
    index_html += "<p><a href='"+prefix+".html'><img src=images/film.png height=50px></a>The Most Successful Movies of the Year</p>"
    for year_key in html_data.keys():
        index_html += "<div><a href='"+"pages/"+prefix+year_key+".html'>"
        for img_index in range(5):
            index_html += index_img_dict[year_key][img_index]
        index_html += year_key
        for img_index in range(5, len(index_img_dict[year_key])):
            index_html += index_img_dict[year_key][img_index]
        index_html += "</a></div>"
    index_html += "</body>\n</html>\n"
    f_html = open(prefix+".html", "w")
    if f_html:
        f_html.write(index_html)
    f_html.close()


def save_html(prefix):
    global html_data, style_data
    for year_key in html_data.keys():
        try:
            f_check = open("pages/"+prefix+year_key+".html", "r")
            if f_check:
                if f_check.read() == html_data[year_key]:
                    f_check.close()
                    continue
                f_check.close()
        except:
            pass
        f_html = open("pages/"+prefix+year_key+".html", "w")   
        if f_html:
            f_html.write(html_data[year_key])
        f_html.close()
        print("pages/"+prefix+year_key+".html"+" updated")


if __name__ == "__main__":
    prefix = "index"
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        read_info(fname)
        prefix = fname.split(".txt")[0]
    movie_file_name = load_config()
    read_distr("distributors.txt")
    read_movies(movie_file_name, prefix)
    save_html(prefix)
    save_index(prefix)

