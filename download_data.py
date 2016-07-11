# We will be using MemeGenerator's API to fetch around
# 1000 memes and their underlying images
import json
from urllib2 import urlopen, HTTPError, URLError
import os
import math

page_size = 24
display_names = {}

def meme_instances_popular(page_index = 0):
    url = "http://version1.api.memegenerator.net/Instances_Select_ByPopular"
    params = "languageCode=en&pageIndex=%d&pageSize=%d&days=7" % (page_index, page_size)
    res = urlopen("%s?%s" % (url, params)).read()
    hres = json.loads(res)[u'result']
    memes = []
    for meme in hres:
        memes.append((
            meme[u'displayName'],
            meme[u'imageUrl'],
            meme[u'instanceImageUrl']
        ))

    return memes

# ml_cat means "Machine Learning Category", like train or validation
# cat is just "Category", like meme or not_meme
def download(url, name, ml_cat, cat):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url + " as " + name

        # Open our local file for writing
        with open("data/%s/%s/%s" % (ml_cat, cat, name), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

def format_name(name, j, kind):
    base = name.lower().replace(" ", "_").replace("/", "")
    return "%s_%d_%s.jpg" % (base, j, kind)

def download_memes_and_underlying_images(total_count, ml_cat):
    pages = int(math.ceil(total_count / page_size))
    memes = []
    j = 0
    for index in range(pages):
        for meme in meme_instances_popular(index):
            memes.append(meme)
            j += 2
            not_meme_name = format_name(meme[0], j+1, "not_memes")
            not_meme_url = meme[1]
            meme_name = format_name(meme[0], j+2, "memes")
            meme_url = meme[2]
            download(meme_url, meme_name, ml_cat, "memes")
            if not(meme[0] in display_names):
                download(not_meme_url, not_meme_name, ml_cat, "not_memes")
                display_names[meme[0]] = 1


if not(os.path.exists("data/train/memes")):
    os.makedirs("data/train/memes")
    os.makedirs("data/train/not_memes")
    os.makedirs("data/validation/memes")
    os.makedirs("data/validation/not_memes")

download_memes_and_underlying_images(2000, "train")
download_memes_and_underlying_images(800, "validation")
