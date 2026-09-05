import os
import urllib.parse
import urllib.request
import json

from media_validator import validate_image
from media_spec import get_media_spec
from media_ranker import select_best_photo


UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"
PEXELS_API_URL = "https://api.pexels.com/v1/search"
PIXABAY_API_URL = "https://pixabay.com/api/"


MAX_RESULTS_PER_SOURCE = 5

MIN_WIDTH = 1200
MIN_HEIGHT = 700



def search_unsplash(query, access_key):

    params = urllib.parse.urlencode({
        "query": query,
        "per_page": MAX_RESULTS_PER_SOURCE,
        "orientation": "landscape"
    })

    url = f"{UNSPLASH_API_URL}?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Client-ID {access_key}"
        }
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    photos = []

    for item in data.get("results", []):

        photos.append({
            "id": item.get("id"),
            "width": item.get("width", 0),
            "height": item.get("height", 0),
            "url": item.get("urls", {}).get("regular", ""),
            "source": "Unsplash",
            "author": item.get("user", {}).get("name", "")
        })

    return photos



def search_pexels(query, api_key):

    params = urllib.parse.urlencode({
        "query": query,
        "per_page": MAX_RESULTS_PER_SOURCE,
        "orientation": "landscape"
    })

    url = f"{PEXELS_API_URL}?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": api_key
        }
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    photos = []

    for item in data.get("photos", []):

        photos.append({
            "id": item.get("id"),
            "width": item.get("width", 0),
            "height": item.get("height", 0),
            "url": item.get("src", {}).get("large", ""),
            "source": "Pexels",
            "author": item.get("photographer", "")
        })

    return photos



def search_pixabay(query, api_key):

    params = urllib.parse.urlencode({
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": MAX_RESULTS_PER_SOURCE
    })

    url = f"{PIXABAY_API_URL}?{params}"

    with urllib.request.urlopen(url) as response:

        data = json.loads(
            response.read().decode("utf-8")
        )


    photos = []

    for item in data.get("hits", []):

        photos.append({
            "id": item.get("id"),
            "width": item.get("imageWidth", 0),
            "height": item.get("imageHeight", 0),
            "url": item.get("largeImageURL", ""),
            "source": "Pixabay",
            "author": item.get("user", "")
        })

    return photos



def filter_photos(photos):

    approved = []

    for photo in photos:

        if photo["width"] < MIN_WIDTH:
            continue

        if photo["height"] < MIN_HEIGHT:
            continue


        result = validate_image(
            width=photo["width"],
            height=photo["height"],
            file_mb=2,
            file_format="jpg",
            media_type="BLOG_IMAGE"
        )


        if result["valid"]:
            approved.append(photo)


    return approved



def get_best_photo(query):

    all_photos = []


    unsplash_key = os.environ.get(
        "UNSPLASH_ACCESS_KEY"
    )

    pexels_key = os.environ.get(
        "PEXELS_API_KEY"
    )

    pixabay_key = os.environ.get(
        "PIXABAY_API_KEY"
    )


    if unsplash_key:
        all_photos.extend(
            search_unsplash(
                query,
                unsplash_key
            )
        )


    if pexels_key:
        all_photos.extend(
            search_pexels(
                query,
                pexels_key
            )
        )


    if pixabay_key:
        all_photos.extend(
            search_pixabay(
                query,
                pixabay_key
            )
        )


    valid_photos = filter_photos(
        all_photos
    )


    return select_best_photo(
        valid_photos
    )
