import urllib
import zlib
import re
import datetime
import os.path
import xml.etree.ElementTree as ET
from Utils.BetaserisUtils import BetaserieUtils
from Utils.ColumnDisplayUtils import DisplayListUtils
from Utils.InteractionUtils import InteractionUtils

def findTorrentsForEpisode(anEpisode):
    print(anEpisode)
    episodePath =  anEpisode.replace(' ', '%20')
    episodePath = re.sub(r'\([0-9][0-9][0-9][0-9]\)', '', episodePath)
    urlEpisode = ("https://kat.cr/usearch/%s/?rss=1" % episodePath)
    try:
        f = urllib.request.urlopen(urlEpisode)
        decompressed_data=zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            decompressed_data=None
        else:
            raise
    return decompressed_data

def createWebPageReult(result, downloadDir):
    pageName = str(datetime.datetime.now().date())+'.html'
    f = open(os.path.join(downloadDir,pageName),'w')
    message = """<html>
                <head></head>
                <body>"""+str(datetime.datetime.now().date())+"""<ul>"""
    for anItem in result:
        message += '<li><a href="'+anItem['link']+'">'+anItem['title']+'</a></li>'
    message += """</ul></body></html>"""

    f.write(message)
    f.close()

downloadDir = r"C:\Users\nogebour\Videos\Others\LinkToTorrent"
aBetaObject = BetaserieUtils()
episodes = aBetaObject.getTodayEpisode()
result = []
for anEpisode in episodes:
    rssResult = findTorrentsForEpisode(anEpisode)
    torrentList = []
    if rssResult is not None:
        root = ET.fromstring(rssResult)
        for channel in root.iter('channel'):
            for anItem in channel.iter('item'):
                title= None
                linkTorrent = None
                seeds = None
                peers = None
                torrentFileName = None
                rawLinkTorrent = None
                ns = {'torrent':'//kastatic.com/xmlns/0.1/'}
                for aTorrentFile in anItem.findall('torrent:seeds', ns):
                    seeds= int(aTorrentFile.text)
                for aTorrentFile in anItem.findall('torrent:peers', ns):
                    peers = int(aTorrentFile.text)
                for aTorrentFile in anItem.findall('torrent:fileName', ns):
                    title = (aTorrentFile.text).replace('.torrent','')
                for aTorrentFile in anItem.iter('enclosure'):
                    rawLinkTorrent = aTorrentFile.attrib['url']
                    torrentFileName = (re.search('\?title=(.*)', rawLinkTorrent, re.IGNORECASE).group(1))+'.torrent'
                    linkTorrent = re.sub(r'\?title=.*', '', rawLinkTorrent)
                if torrentFileName is not None:
                    torrentList.append({'title':title, 'rawLink': rawLinkTorrent, 'link':linkTorrent, 'fileName': torrentFileName, 'seeds':seeds, 'peers': peers})
    if len(torrentList) > 0:
        sortedTorrent = sorted(torrentList, key=lambda k: k['seeds'], reverse=True)
        anIndex = 0
        for aTorrent in sortedTorrent:
            aTorrent['index'] = anIndex
            anIndex += 1
        aDisplayObject = DisplayListUtils()
        print('Choose the torrent to download for %s' % anEpisode)
        aDisplayObject.displayList(sortedTorrent,
                                   ['index', 'title', 'seeds', 'peers'],
                                   {'index':'c','title':'l','seeds':'c','peers':'c'})
        theChoice = InteractionUtils.query_int('> Make your Choice :')
        result.append({'title':anEpisode, 'link':sortedTorrent[theChoice]['rawLink']})
createWebPageReult(result, downloadDir)
