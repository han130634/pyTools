# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 19:15:34 2015

@author: aneasystone
"""

import libtorrent as lt
import time

def bt2mag(tfile):
    info = lt.torrent_info(tfile)
    print "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())

def magnet2t(link,tfile):
    sess = lt.session()
    
    #'''
    sess.add_dht_router('router.bittorrent.com', 6881)
    sess.add_dht_router('router.utorrent.com', 6881)
    sess.add_dht_router('router.bitcomet.com', 6881)
    sess.add_dht_router('dht.transmissionbt.com', 6881)
    sess.start_dht();    
    #'''
    
    params = {
             "save_path": 'D:\\Desktop',
             "storage_mode":lt.storage_mode_t.storage_mode_sparse,
             "paused": True,
             "auto_managed": True,
             "duplicate_is_error": True
           }

    print link 
    handle = lt.add_magnet_uri(sess, link, params)
 
    while (not handle.has_metadata()):
        time.sleep(5)
        print handle.has_metadata()
        
    print 'got metadata, starting torrent download...'
    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3f' % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state], s.total_download/1000000)
        time.sleep(5)
  
    torinfo = handle.get_torrent_info()

    fs = lt.file_storage()
    for f in torinfo.files():
        fs.add_file(f)
 
    torfile = lt.create_torrent(fs)
    torfile.set_comment(torinfo.comment())
    torfile.set_creator(torinfo.creator())
     
    #for i in xrange(0, torinfo.num_pieces()):
    #    hashes = torinfo.hash_for_piece(i)
    #    torfile.set_hash(i, hashes)
 
    #for url_seed in torinfo.url_seeds():
    #    torfile.add_url_seed(url_seed)
 
    #for http_seed in torinfo.http_seeds():
    #    torfile.add_http_seed(http_seed)
 
    for node in torinfo.nodes():
        torfile.add_node(node)
 
    for tracker in torinfo.trackers():
        torfile.add_tracker(tracker)
 
    torfile.set_priv(torinfo.priv())
  
    t = open(tfile, "wb")
    t.write(lt.bencode(torfile.generate()))
    t.close()
    print '%s  generated!'% tfile
 
def main():

    bt2mag("torrents\\ubuntu.torrent")    
    magnet2t(
        'magnet:?xt=urn:btih:1619ecc9373c3639f4ee3e261638f29b33a6cbd6&dn=ubuntu-14.10-desktop-i386.iso', 
        't.torrent')
    
    '''
    magnet2t(
        #'magnet:?xt=urn:btih:51df6808c739174c8f264701ba94460c5238d6ce',
        'magnet:?xt=urn:btih:fd8b1062af0d8c2426cb4d180b86815ffa91b479&dn=Game.of.Thrones.S05E01.HDTV.x264-Xclusive.mp4',
        't.torrent')
    '''
 
if __name__ == '__main__':
    main()