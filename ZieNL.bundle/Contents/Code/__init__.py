#Zie.nl VideoPlugin v1.0
#Created by Matthijs Drenth

import sys
import urllib 
import re

####################################################################################################

VIDEO_PREFIX = "/video/ZieNL"

NAME = L('Title')

ART  = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = 1
	

####################################################################################################

def VideoMainMenu():

	dir = MediaContainer(viewGroup="List")
	#dir.Append(Function(DirectoryItem(ShowLatest, 'Nieuwste video\'s', None)))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Algemeen', None),rss='http://www.zie.nl/rss/list/2147'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Opmerkelijk', None),rss='http://www.zie.nl/rss/list/2157'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Achterklap', None),rss='http://www.zie.nl/rss/list/2224'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Sport', None),rss='http://www.zie.nl/rss/list/2234'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Wetenschap', None),rss='http://www.zie.nl/rss/list/2243'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Auto', None),rss='http://www.zie.nl/rss/list/2250'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Economie', None),rss='http://www.zie.nl/rss/list/2258'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Lifestyle', None),rss='http://www.zie.nl/rss/list/2265'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Weer', None),rss='http://www.zie.nl/rss/list/2787'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Film', None),rss='http://www.zie.nl/rss/list/2282'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Games', None),rss='http://www.zie.nl/rss/list/2231'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Muziek', None),rss='http://www.zie.nl/rss/list/2401'))
	dir.Append(Function(DirectoryItem(ShowLatest, 'Tech', None),rss='http://www.zie.nl/rss/list/2381'))
	return dir

####################################################################################################

def ShowLatest(sender, rss):

    dir = MediaContainer(viewGroup="InfoList")
   
    page = XML.ElementFromURL(rss)
    for item in page.getiterator('item'):
    	link=item.findtext("link")
        title=item.findtext("title")
        pubDate=item.findtext("pubDate")
        description=remove_html_tags(item.findtext("description"))
        description=description.encode("utf-8").encode('ascii', 'xmlcharrefreplace').encode('ascii', 'xmlcharrefreplace')
        dir.Append(Function(VideoItem(GetUrl, title=title, summary=description, subtitle=pubDate, thumb=Function(GetThumb, vl=link)), url=link, title=title))
    return dir

####################################################################################################

def GetUrl(sender, url, title):
	sock = urllib.urlopen(url) 
	sdpagecontent = sock.read()                            
	sock.close()
	m1 = re.search('&file=(.{0,})(&logo)', sdpagecontent)
	Log(m1.group(2))
	VideoLinkFLV = m1.group(1)
	return Redirect(VideoLinkFLV)
		
####################################################################################################

def GetThumb(vl):
	sock = urllib.urlopen(vl) 
	pagecontent = sock.read()                            
	sock.close()
	
	m2 = re.search('<meta property=\"og:image\" content=\"(.{0,})(\">)', pagecontent)
	thumb = m2.group(1)
	try:
		image = HTTP.Request(thumb, cacheTime=CACHE_1MONTH).content
		return DataObject(image, 'image/jpeg')
	except:
		return Redirect(R(PLUGIN_ICON_DEFAULT))
		
####################################################################################################

def remove_html_tags(data):
    p = re.compile('<.*?>|&nbsp;|Lezersreacties(.{0,})|Uw reactie plaatsen|\s\s')
    return p.sub('', data)

def empty(sender):
	sys.exit()
	return sender