MEDIA_SPEC = {

    "BLOG_IMAGE": {
        "min_width": 1600,
        "min_height": 1000,

        "preferred_width": 2000,
        "preferred_height": 1333,

        "ratios": [
            1.5,
            1.777
        ],

        "min_file_mb": 0.3,
        "max_file_mb": 5,

        "formats": [
            "jpg",
            "jpeg",
            "png"
        ]
    },


    "SHORT_VIDEO": {

        "width": 1080,
        "height": 1920,

        "ratio": 0.5625,

        "min_seconds": 10,
        "preferred_min_seconds": 20,
        "preferred_max_seconds": 45,
        "max_seconds": 180,

        "fps_min": 24,
        "fps_max": 60,

        "min_file_mb": 1,
        "max_file_mb": 500,

        "container": "mp4",

        "video_codec": "H.264",
        "audio_codec": "AAC"
    },


    "THUMBNAIL": {

        "width": 1080,
        "height": 1920,

        "ratio": 0.5625,

        "max_file_mb": 10,

        "formats": [
            "jpg",
            "jpeg",
            "png"
        ]
    },


    "SOCIAL_POST": {

        "min_width": 1080,
        "min_height": 1080,

        "preferred_ratios": [
            1,
            0.8,
            0.5625
        ],

        "max_file_mb": 10
    }
}


def get_media_spec(media_type):

    if media_type not in MEDIA_SPEC:
        raise ValueError(
            f"지원하지 않는 미디어 타입: {media_type}"
        )

    return MEDIA_SPEC[media_type]
