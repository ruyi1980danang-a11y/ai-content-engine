from video_validator import validate_video


def create_video_package(
    platform,
    video_info=None
):

    if not video_info:
        return {
            "status": "failed",
            "errors": [
                "video_info 없음"
            ]
        }


    result = validate_video(
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


    if not result["valid"]:
        return {
            "status": "failed",
            "errors": result["errors"]
        }


    return {
        "status": "success",
        "video": video_info
    }
