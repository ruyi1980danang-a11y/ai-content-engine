import os
import urllib.request
import urllib.parse
import json


PEXELS_VIDEO_API = "https://api.pexels.com/videos/search"
PIXABAY_VIDEO_API = "https://pixabay.com/api/videos/"


def search_pexels_video(keyword, per_page=3):

    api_key = os.environ.get("PEXELS_API_KEY")

    if not api_key:
        return None

    params = {
        "query": keyword,
        "per_page": per_page
    }

    url = (
        PEXELS_VIDEO_API
        + "?"
        + urllib.parse.urlencode(params)
    )

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": api_key
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        data = json.loads(
            response.read().decode("utf-8")
        )

    videos = data.get(
        "videos",
        []
    )

    if not videos:
        return None

    video = videos[0]

    return {
        "source": "PEXELS",
        "id": video.get("id"),
        "duration": video.get("duration"),
        "url": video.get("url"),
        "license": "PEXELS"
    }



def search_pixabay_video(keyword):

    api_key = os.environ.get(
        "PIXABAY_API_KEY"
    )

    if not api_key:
        return None


    params = {
        "key": api_key,
        "q": keyword,
        "per_page": 3
    }


    url = (
        PIXABAY_VIDEO_API
        + "?"
        + urllib.parse.urlencode(params)
    )


    with urllib.request.urlopen(
        url,
        timeout=30
    ) as response:

        data = json.loads(
            response.read().decode("utf-8")
        )


    videos = data.get(
        "hits",
        []
    )


    if not videos:
        return None


    video = videos[0]


    return {
        "source": "PIXABAY",
        "id": video.get("id"),
        "duration": video.get("duration"),
        "url": video.get("pageURL"),
        "license": "PIXABAY"
    }



def get_best_video(keyword):

    video = search_pexels_video(keyword)

    if video:
        return video


    video = search_pixabay_video(keyword)

    if video:
        return video


    return None
