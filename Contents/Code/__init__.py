import json

PREFIX = '/video/goodparts'
TITLE = 'The Good Parts'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
API_URL = 'http://localhost:8000/api/get_some_scenes/'


def Start():
    # Setup the default attributes for the ObjectContainer
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = TITLE

    # Setup the default attributes for the other objects
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


@handler(PREFIX, TITLE)
def MainMenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(LiveMenu), title="Live"))
    return oc


@route(PREFIX + '/livemenu')
def LiveMenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(ChannelMenu, channel=1), title="Channel 1"))
    oc.add(DirectoryObject(key=Callback(ChannelMenu, channel=2), title="Channel 2"))
    oc.add(DirectoryObject(key=Callback(ChannelMenu, channel=3), title="Channel 3"))
    return oc


@route(PREFIX + '/channelmenu')
def ChannelMenu(channel=None):
    oc = ObjectContainer()
    items = json.loads(HTTP.Request(API_URL).content)
    for i in items:
        oc.add(VideoClipObject(
            url = i['video_path'],
            title = i['scene_name'],
            summary = i['description'],
            thumb = i['movie_poster'],
        ))
    # read items as json, parse data out
    # reference https://forums.plex.tv/discussion/28084/plex-plugin-development-walkthrough
    return oc
