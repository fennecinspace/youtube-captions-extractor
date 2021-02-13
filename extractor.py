import os
import sys
import json
import re
import requests

def get_available_captions(video_url):
    try:
        print('Getting captions list')

        response = requests.get(video_url)

        begin = response.text.index('captionTracks')
        begin = response.text.index('[', begin)
        end = response.text.index(']', begin)

        tracks_str = response.text[begin : end + 1]

        return json.loads(tracks_str)
    
    except Exception as e:
        print('Could not acquire captions list')
        return []


def get_caption(code, url):
    print('Getting', code)
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        VIDEO_CODE = sys.argv[1]
    
    else: # default demo / example
        VIDEO_CODE = "pNar3Dh9zDk"

    VIDEO_URL = 'https://www.youtube.com/watch?v=' + VIDEO_CODE

    captions = get_available_captions(VIDEO_URL)

    if captions:
        if not os.path.exists(VIDEO_CODE):
            os.mkdir(VIDEO_CODE)

        for caption in captions:
            caption_xml = get_caption(caption['languageCode'], caption['baseUrl'])
            caption_save_file = os.path.join( VIDEO_CODE, caption['languageCode'] + '.xml' )
            
            with open(caption_save_file, 'w') as f:
                f.write(caption_xml)

    else:
        print('No available captions')