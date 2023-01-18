import random
import urllib

import yaml
from google_images_search import GoogleImagesSearch


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
]
with open('config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

api = data['api']
cx_id = data['cx_id']
gis = GoogleImagesSearch(api, cx_id)

def retrieve_image_cover(name):

    search_params = {
        'q': name,
        'num': 1
    }

    # define search params
    gis.search(search_params)

    # results
    gis.results()

    # retrieve the first image
    first_image_url = gis.results()[0].url

    return first_image_url


def load_image(audio, cover_image):
    url = cover_image

    # A list of user agents to choose from
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    ]

    headers = {'User-Agent': random.choice(user_agents)}
    req = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(req)
        content = response.read()
        audio.tag.images.set(3, content, "image/jpeg")
        audio.tag.save()
        return audio
    except urllib.error.HTTPError as e:
        return audio
        print(e)

