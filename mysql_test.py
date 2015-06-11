# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:06:01 2015

@author: aneasystone
"""

import MySQLdb
import config

try:
    conn = MySQLdb.connect(host=config.host,user=config.user,passwd=config.pwd,port=config.port,charset='utf8')
    cur = conn.cursor()
    conn.select_db(config.db)
 
    count = cur.execute('select * from bd_city')
    print 'there has %s cities' % count
    
    print '==' * 10    
    
    result = cur.fetchone()
    print result
    
    print '==' * 10
    
    results = cur.fetchmany(5)
    for r in results:
        print r
    '''    
    print '==' * 10
    cur.scroll(0, mode='absolute')
    results=cur.fetchall()
    for r in results:
        print r[1]
    '''
    conn.commit()
    cur.close()
    conn.close()
 
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])