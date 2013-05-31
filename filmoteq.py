#!/usr/bin/env python 
# -*- coding: utf-8 -*-

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                              #
#                                                                              #
# filmoteq is a movie cataloger wich runs on the shell and generates a minimal,#
# eye candy webpage containing posters of your movies and links to their       #
# imdb's info.                                                                 #
#                                                                              #
# filmoteq's idea and development by g0to                                      #
#                                                                              #
#                                                                              #
# HOW TO USE:                                                                  #
#                                                                              #
#   -a TITLE PATH_TO_IMAGE : add movie TITLE to database as well as save image #
#                            file on PATH_TO_IMAGE as movie poster.            #
#                                                                              #
#   -l : list all movie titles preceded by its database ID                     #
#                                                                              #
#   -d ID : delete movie record associated to ID                               #
#                                                                              #
#   -g : generate new html catalog                                             #
#                                                                              #
#                                                                              #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


import os
import shutil
import sqlite3
import sys


db_filename = "filmoteq.db"
create_table = "CREATE TABLE IF NOT EXISTS movie (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, poster BLOB)"
insert_element = "INSERT INTO movie (title, poster) VALUES (?,?)"
select_all = "SELECT * FROM movie ORDER BY UPPER(title)"
delete_element = "DELETE FROM movie WHERE id=?"


conn = sqlite3.connect(db_filename)
conn.row_factory = sqlite3.Row  # it allows you to access rows by name instead of index
conn.text_factory = str # UTF-8 encoding by default. Mucho bueno for Spanish!
cursor = conn.cursor()
cursor.execute(create_table)

if sys.argv[1] == '-a':
    with open(sys.argv[3], "rb") as poster_image:
        ablob = poster_image.read()
    cursor.execute(insert_element, (sys.argv[2],sqlite3.Binary(ablob),))
    conn.commit()
    conn.close()

elif sys.argv[1] == '-l':
    cursor.execute(select_all)
    for row in cursor:
        print "{0:3}".format(row['id']) + " - " + row['title']
    conn.close()

elif sys.argv[1] == '-d':
    cursor.execute(delete_element, [sys.argv[2]])
    conn.commit()
    conn.close()

elif sys.argv[1] == '-g':
    html_head =  '<html>'
    html_head += '<head>'
    html_head += '<title>filmoteq by g0to</title>'
    html_head += '</head>'
    html_body =  '<body bgcolor="#2d2d2d">'
    html_tail =  '</body>'
    html_tail += '</html>'

    shutil.rmtree('posters', True)
    os.makedirs('posters')
    cursor.execute(select_all)
    for row in cursor:
        with open("posters/%d" % (row['id']), "wb") as poster_image:
            ablob = row['poster']
            poster_image.write(ablob) 
        html_body += '''<a href="http://www.imdb.com/find?q=%s&s=tt"><img
        src="posters/%d" alt="%s" height="450" width="300"
        style="margin:50"/></a>\n''' % (row['title'], row['id'],row['title'])

    conn.close()
    filmoteq_html = open('filmoteq.html', 'w')
    filmoteq_html.write(html_head + html_body + html_tail)
    filmoteq_html.close()
