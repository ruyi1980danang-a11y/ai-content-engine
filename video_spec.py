VIDEO_SPEC = {

    "YOUTUBE_SHORTS": {
        "width": 1080,
        "height": 1920,
        "ratio": "9:16",
        "min_seconds": 10,
        "max_seconds": 180,
        "fps_min": 24,
        "fps_max": 60,
        "format": "mp4",
        "video_codec": "H.264",
        "audio_codec": "AAC",
        "max_file_mb": 200
    },

    "INSTAGRAM_REELS": {
        "width": 1080,
        "height": 1920,
        "ratio": "9:16",
        "min_seconds": 3,
        "max_seconds": 180,
        "fps_min": 24,
        "fps_max": 60,
        "format": "mp4",
        "video_codec": "H.264",
        "audio_codec": "AAC",
        "max_file_mb": 200
    },

    "TIKTOK": {
        "width": 1080,
        "height": 1920,
        "ratio": "9:16",
        "min_seconds": 10,
        "max_seconds": 180,
        "fps_min": 24,
        "fps_max": 60,
        "format": "mp4",
        "video_codec": "H.264",
        "audio_codec": "AAC",
        "max_file_mb": 500
    },

    "NAVER_CLIP": {
        "width": 1080,
        "height": 1920,
        "ratio": "9:16",
        "min_seconds": 3,
        "max_seconds": 180,
        "fps_min": 24,
        "fps_max": 60,
        "format": "mp4",
        "video_codec": "H.264",
        "audio_codec": "AAC",
        "max_file_mb": 500
    }
}


def get_video_spec(platform):
    return VIDEO_SPEC[platform]
