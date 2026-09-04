from video_validator import validate_video


def create_video_package(
    platform,
    video_info
):

    result = validate_video(
        platform=platform,
        width=video_info["width"],
        height=video_info["height"],
        seconds=video_info["seconds"],
        fps=video_info["fps"],
        file_mb=video_info["file_mb"],
        file_format=video_info["format"],
        video_codec=video_info["video_codec"],
        audio_codec=video_info["audio_codec"]
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
