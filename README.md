# best_movies_html
Html pages generator with best movies


1. Use ./get_wiki_info.py year, to get data from wikipedia about top 10 movies of the year save results into file year_movies.txt.
  Then copy all information from several files into general file movies.txt, only for config 'en'

2. When you have filled movies.txt use ./make_movie_site.py it will get additional parameters from config.txt.
  It creates html-pages for each year from movies.txt, and directory html-pages with covers of all movies in year order

3. You can also use ./make_movie_site.py kinopoisk.txt to create html-pages with kinopoisk.ru links where you can probably watch that film

or ./make_movie_site.py info.txt to create html-pages with your comments and local paths to film files

