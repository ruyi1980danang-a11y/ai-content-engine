```python
import os
import urllib.request
import urllib.parse
import json


PEXELS_VIDEO_API = "https://api.pexels.com/videos/search"
PIXABAY_VIDEO_API = "https://pixabay.com/api/videos/"

DEFAULT_PER_PAGE = 5
REQUEST_TIMEOUT = 30


# ============================================================
# Pexels Video Search
# ============================================================

def search_pexels_video(keyword, per_page=DEFAULT_PER_PAGE):

    api_key = os.environ.get("PEXELS_API_KEY")

    if not api_key:
        return {
            "success": False,
            "source": "PEXELS",
            "error": "API_KEY_MISSING",
            "videos": []
        }

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

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

    except Exception as e:

        return {
            "success": False,
            "source": "PEXELS",
            "error": str(e),
            "videos": []
        }

    videos = data.get("videos", [])

    if not videos:

        return {
            "success": True,
            "source": "PEXELS",
            "error": "NO_RESULTS",
            "videos": []
        }

    results = []

    for video in videos:

        results.append({
            "source": "PEXELS",
            "id": video.get("id"),
            "duration": video.get("duration"),
            "width": video.get("width"),
            "height": video.get("height"),
            "url": video.get("url"),
            "license": "PEXELS",
            "search_cost": 0
        })

    return {
        "success": True,
        "source": "PEXELS",
        "error": None,
        "videos": results
    }


# ============================================================
# Pixabay Video Search
# ============================================================

def search_pixabay_video(
    keyword,
    per_page=DEFAULT_PER_PAGE
):

    api_key = os.environ.get("PIXABAY_API_KEY")

    if not api_key:
        return {
            "success": False,
            "source": "PIXABAY",
            "error": "API_KEY_MISSING",
            "videos": []
        }

    params = {
        "key": api_key,
        "q": keyword,
        "per_page": per_page
    }

    url = (
        PIXABAY_VIDEO_API
        + "?"
        + urllib.parse.urlencode(params)
    )

    try:

        with urllib.request.urlopen(
            url,
            timeout=REQUEST_TIMEOUT
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

    except Exception as e:

        return {
            "success": False,
            "source": "PIXABAY",
            "error": str(e),
            "videos": []
        }

    videos = data.get("hits", [])

    if not videos:

        return {
            "success": True,
            "source": "PIXABAY",
            "error": "NO_RESULTS",
            "videos": []
        }

    results = []

    for video in videos:

        videos_data = video.get("videos", {})

        large_video = videos_data.get("large", {})
        medium_video = videos_data.get("medium", {})
        small_video = videos_data.get("small", {})

        selected_video = (
            large_video
            or medium_video
            or small_video
        )

        results.append({
            "source": "PIXABAY",
            "id": video.get("id"),
            "duration": video.get("duration"),
            "width": selected_video.get("width"),
            "height": selected_video.get("height"),
            "url": selected_video.get("url"),
            "page_url": video.get("pageURL"),
            "license": "PIXABAY",
            "search_cost": 0
        })

    return {
        "success": True,
        "source": "PIXABAY",
        "error": None,
        "videos": results
    }


# ============================================================
# Candidate Score
# ============================================================

def score_video(video):

    score = 0

    width = video.get("width") or 0
    height = video.get("height") or 0
    duration = video.get("duration") or 0

    # 해상도
    if width >= 1920:
        score += 40
    elif width >= 1280:
        score += 30
    elif width >= 720:
        score += 20

    # 세로 영상 우선
    if height > width:
        score += 30

    # 너무 짧거나 긴 영상보다 적당한 영상 우선
    if 5 <= duration <= 30:
        score += 20
    elif 3 <= duration <= 60:
        score += 10

    # 공급원 기본 점수
    if video.get("source") == "PEXELS":
        score += 10
    elif video.get("source") == "PIXABAY":
        score += 8

    return score


# ============================================================
# Best Video Selection
# ============================================================

def select_best_video(videos):

    if not videos:
        return None

    for video in videos:
        video["score"] = score_video(video)

    videos.sort(
        key=lambda item: item.get("score", 0),
        reverse=True
    )

    return videos[0]


# ============================================================
# Search All Sources
# ============================================================

def search_all_video_sources(keyword):

    all_videos = []
    source_status = []

    # --------------------------------------------------------
    # Pexels
    # --------------------------------------------------------

    pexels_result = search_pexels_video(keyword)

    source_status.append({
        "source": "PEXELS",
        "success": pexels_result["success"],
        "error": pexels_result["error"]
    })

    all_videos.extend(
        pexels_result.get("videos", [])
    )

    # --------------------------------------------------------
    # Pixabay
    # --------------------------------------------------------

    pixabay_result = search_pixabay_video(keyword)

    source_status.append({
        "source": "PIXABAY",
        "success": pixabay_result["success"],
        "error": pixabay_result["error"]
    })

    all_videos.extend(
        pixabay_result.get("videos", [])
    )

    return {
        "success": len(all_videos) > 0,
        "keyword": keyword,
        "videos": all_videos,
        "source_status": source_status,
        "search_cost": 0
    }


# ============================================================
# Get Best Video
# ============================================================

def get_best_video(keyword):

    result = search_all_video_sources(keyword)

    videos = result.get("videos", [])

    if not videos:

        return {
            "success": False,
            "status": "NO_VIDEO_SOURCE",
            "keyword": keyword,
            "video": None,
            "search_cost": 0,
            "source_status": result.get(
                "source_status",
                []
            )
        }

    best_video = select_best_video(videos)

    return {
        "success": True,
        "status": "VIDEO_FOUND",
        "keyword": keyword,
        "video": best_video,
        "search_cost": 0,
        "source_status": result.get(
            "source_status",
            []
        )
    }
```
