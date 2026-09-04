from media_validator import validate_image
from media_spec import get_media_spec

import urllib.parse
import urllib.request
import json


UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"


def search_unsplash(query, access_key, per_page=10):

    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
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

        photo = {
            "id": item.get("id"),
            "width": item.get("width", 0),
            "height": item.get("height", 0),
            "url": item.get("urls", {}).get("regular", ""),
            "source": "Unsplash",
            "author": item.get("user", {}).get("name", "")
        }

        photos.append(photo)

    return photos



def filter_photos(photos):

    approved = []

    for photo in photos:

        result = validate_image(
            width=photo["width"],
            height=photo["height"],
            file_mb=1,
            file_format="jpg",
            media_type="BLOG_IMAGE"
        )

        if result["valid"]:
            approved.append(photo)

    return approved



def score_photo(photo):

    score = 0

    spec = get_media_spec(
        "BLOG_IMAGE"
    )

    if photo["width"] >= spec["preferred_width"]:
        score += 40

    if photo["height"] >= spec["preferred_height"]:
        score += 40

    score += 20

    return score



def select_best_photo(photos):

    if not photos:
        return None

    ranked = sorted(
        photos,
        key=score_photo,
        reverse=True
    )

    return ranked[0]



def get_best_photo(
    query,
    access_key
):

    photos = search_unsplash(
        query,
        access_key
    )

    valid = filter_photos(
        photos
    )

    return select_best_photo(
        valid
    )
