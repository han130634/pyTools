# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:45:03 2015

@author: aneasystone
"""

# https://github.com/aaronsw/html2text
import html2text
# https://pypi.python.org/pypi/MySQL-python/1.2.5
import MySQLdb

import os
import codecs
import configs

class Post(object):
    pass

def get_all_posts():
    
    posts = []    
    try:
        conn = MySQLdb.connect(host=configs.host,user=configs.user,passwd=configs.pwd,port=configs.port,charset='utf8')
        cur = conn.cursor()
        conn.select_db(configs.db)
 
        count = cur.execute('select * from typecho_contents')
        print 'there has %s posts' % count
    
        print '==' * 10
    
        results = cur.fetchall()
        for r in results:
            p = Post()
            p.title = r[1]
            p.content = r[5]
            posts.append(p)
            
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return posts

def handle_post(post):
    
    # save to html file
    htmlname = 'files/' + post.title + '.html'
    html = post.content
    #t = open(htmlname, "wb")
    t = codecs.open(htmlname, 'wb', 'utf-8');
    t.write(html)
    t.close()
    
    # save to markdown file
    mdname = 'files/' + post.title + '.md'
    md = html2text.html2text(post.content)
    #t = open(mdname, "wb")
    t = codecs.open(mdname, 'wb', 'utf-8');
    t.write(md)
    t.close()
    return
    
def main():
    
    if not os.path.exists('files'):
        os.makedirs('files')    
    
    posts = get_all_posts()
    for p in posts:
        print p.title
        #print p.content
        if p.content:
            handle_post(p)

    return
    
if __name__ == '__main__':
    main()