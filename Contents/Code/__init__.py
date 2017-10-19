TITLE = 'The Good Parts'
RSS_FEED = 'http://thegoodparts.michaelstadtmiller.com/rss'
NS = {}
ART = 'art-default.jpg'
ICON = 'icon-default.png'
ICON_SEARCH = 'icon-search.png'
#MLS reference TED
#https://github.com/plexinc-plugins/TED-Talks.bundle/blob/master/Contents/Code/__init__.py
def Start():
    Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    # Setup the default attributes for the ObjectContainer
    ObjectContainer.title1 = TITLE
    ObjectContainer.view_group = 'List'
    ObjectContainer.art = R(ART)

    # Setup the default attributes for the other objects
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


@handler('/video/thegoodparts', TITLE)
def MainMenu():
    oc = ObjectContainer()
    # MLS: can specify customer art or thumb here. default is ART and ICON above.
    
    for video in XML.ElementFromURL(RSS_FEED).xpath('//item'):

    url = video.xpath('./link')[0].text
    title = video.xpath('./title')[0].text
    date = video.xpath('./pubDate')[0].text
    date = Datetime.ParseDate(date)
    summary = video.xpath('./blip:puredescription', namespaces=NS)[0].text
    thumb = video.xpath('./media:thumbnail', namespaces=NS)[0].get('url')

    if thumb[0:4] != 'http':
      thumb = 'http://a.images.blip.tv' + thumb

    duration_text = video.xpath('./blip:runtime', namespaces=NS)[0].text
    duration = int(duration_text) * 1000

    oc.add(VideoClipObject(
      url = url,
      title = title,
      summary = summary,
      thumb = Callback(Thumb, url=thumb),
      duration = duration,
      originally_available_at = date
    ))
    
    return oc

def Thumb(url):
    try:
        data = HTTP.Request(url, cacheTime = CACHE_1MONTH).content
        return DataObject(data, 'image/jpeg')
    except:
        return Redirect(R(ICON))
