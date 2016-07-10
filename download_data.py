# We will be using MemeGenerator's API to fetch around
# 1000 memes and their underlying images
import json
import urllib2
import math

page_size = 24

def meme_instances_popular(page_index = 0):
    url = "http://version1.api.memegenerator.net/Instances_Select_ByPopular"
    params = "languageCode=en&pageIndex=%d&pageSize=%d&days=7" % (page_index, page_size)
    res = urllib2.urlopen("%s?%s" % (url, params)).read()
    hres = json.loads(res)[u'result']
    memes = []
    for meme in hres:
        memes.append((
            meme[u'displayName'],
            meme[u'imageUrl'],
            meme[u'instanceImageUrl']
        ))

    return memes

def download_memes_and_underlying_images(total_count = 1024):
    pages = int(math.ceil(total_count / page_size))
    urls = []
    for index in range(pages):
        for url in meme_instances_popular(index):
            urls.append(url)
            print url



download_memes_and_underlying_images()
