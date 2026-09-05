# ============================================================
# AI STORY CONTENT ENGINE
# video_spec.py
# ============================================================


VIDEO_TYPES = {

    "STORY": {
        "description": "하나의 이야기를 전달하는 영상",
        "narration": "optional",
        "caption": "required"
    },

    "DISCOVERY": {
        "description": "새로운 사실이나 발견 중심",
        "narration": "recommended",
        "caption": "required"
    },

    "FACT": {
        "description": "정보 전달 중심 영상",
        "narration": "required",
        "caption": "required"
    },

    "EXPERIENCE": {
        "description": "여행 경험과 현장 분위기 중심",
        "narration": "optional",
        "caption": "required"
    },

    "HUMAN": {
        "description": "사람과 관계 중심 이야기",
        "narration": "optional",
        "caption": "required"
    },

    "LOCATION": {
        "description": "장소 소개 및 공간 중심",
        "narration": "optional",
        "caption": "required"
    }

}



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

        "max_file_mb": 200,

        # COST CONTROL
        "max_cost_usd": 1.00,

        # QUALITY CONTROL
        "min_width": 720,
        "min_height": 1280,
        "min_fps": 24,
        "min_bitrate_kbps": 2500,

        # AUDIO RULE
        "narration_required": False,
        "narration_optional": True,
        "narration_skip": True,

        # CAPTION RULE
        "caption_required": True,
        "caption_max_length": 80

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

        "max_file_mb": 200,

        # COST CONTROL
        "max_cost_usd": 1.00,

        # QUALITY CONTROL
        "min_width": 720,
        "min_height": 1280,
        "min_fps": 24,
        "min_bitrate_kbps": 2500,

        # AUDIO RULE
        "narration_required": False,
        "narration_optional": True,
        "narration_skip": True,

        # CAPTION RULE
        "caption_required": True,
        "caption_max_length": 80

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

        "max_file_mb": 500,

        # COST CONTROL
        "max_cost_usd": 1.50,

        # QUALITY CONTROL
        "min_width": 720,
        "min_height": 1280,
        "min_fps": 24,
        "min_bitrate_kbps": 2500,

        # AUDIO RULE
        "narration_required": False,
        "narration_optional": True,
        "narration_skip": True,

        # CAPTION RULE
        "caption_required": True,
        "caption_max_length": 80

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

        "max_file_mb": 500,

        # COST CONTROL
        "max_cost_usd": 1.50,

        # QUALITY CONTROL
        "min_width": 720,
        "min_height": 1280,
        "min_fps": 24,
        "min_bitrate_kbps": 2500,

        # AUDIO RULE
        "narration_required": False,
        "narration_optional": True,
        "narration_skip": True,

        # CAPTION RULE
        "caption_required": True,
        "caption_max_length": 80

    }

}



def get_video_spec(platform):

    if platform not in VIDEO_SPEC:
        raise ValueError(
            f"지원하지 않는 플랫폼: {platform}"
        )

    return VIDEO_SPEC[platform]



def get_video_type(video_type):

    if video_type not in VIDEO_TYPES:
        raise ValueError(
            f"지원하지 않는 영상 타입: {video_type}"
        )

    return VIDEO_TYPES[video_type]
