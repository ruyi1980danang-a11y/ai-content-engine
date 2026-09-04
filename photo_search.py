import json
import urllib.parse
import urllib.request


UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"


def search_photos(query, access_key, per_page=5):
    if not query:
        return []

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

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    results = []

    for photo in data.get("results", []):
        results.append({
            "photo_id": photo.get("id", ""),
            "description": photo.get("description", ""),
            "alt_description": photo.get(
                "alt_description", ""
            ),
            "image_url": photo.get(
                "urls", {}
            ).get("regular", ""),
            "source": "Unsplash",
            "source_url": photo.get(
                "links", {}
            ).get("html", ""),
            "photographer": photo.get(
                "user", {}
            ).get("name", ""),
            "license_status": "확인필요"
        })

    return results
