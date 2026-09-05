from video_validator import validate_video


def create_video_package(
    platform,
    video_info=None
):

    if video_info is None:
        return {
            "status": "failed",
            "errors": [
                "video_info 없음"
            ]
        }


    validation = validate_video(
        platform=platform,
        width=video_info.get("width", 0),
        height=video_info.get("height", 0),
        seconds=video_info.get("seconds", 0),
        fps=video_info.get("fps", 0),
        file_mb=video_info.get("file_mb", 0),
        file_format=video_info.get("format", ""),
        video_codec=video_info.get("video_codec", ""),
        audio_codec=video_info.get("audio_codec", "")
    )


    if not validation["valid"]:

        return {
            "status": "failed",
            "platform": platform,
            "errors": validation["errors"]
        }



    return {
        "status": "success",
        "platform": platform,
        "video": {
            "width": video_info["width"],
            "height": video_info["height"],
            "seconds": video_info["seconds"],
            "fps": video_info["fps"],
            "format": video_info["format"],
            "video_codec": video_info["video_codec"],
            "audio_codec": video_info["audio_codec"]
        }
    }
