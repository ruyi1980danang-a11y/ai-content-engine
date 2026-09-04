from video_spec import get_video_spec


PLATFORMS = [
    "YOUTUBE_SHORTS",
    "INSTAGRAM_REELS",
    "TIKTOK",
    "NAVER_CLIP"
]


def get_platform_rule(platform):

    if platform not in PLATFORMS:
        return None

    return get_video_spec(platform)



def validate_platform_support(platform):

    rule = get_platform_rule(platform)

    if rule is None:
        return {
            "supported": False
        }

    return {
        "supported": True,
        "platform": platform,
        "rule": rule
    }
