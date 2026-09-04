from video_spec import get_video_spec


def validate_video(
    platform,
    width,
    height,
    seconds,
    fps,
    file_mb,
    file_format,
    video_codec,
    audio_codec
):

    spec = get_video_spec(platform)

    errors = []

    if width != spec["width"]:
        errors.append("해상도 오류")

    if height != spec["height"]:
        errors.append("해상도 오류")

    if seconds < spec["min_seconds"]:
        errors.append("영상 길이 부족")

    if seconds > spec["max_seconds"]:
        errors.append("영상 길이 초과")

    if fps < spec["fps_min"]:
        errors.append("FPS 부족")

    if fps > spec["fps_max"]:
        errors.append("FPS 초과")

    if file_format.lower() != spec["format"]:
        errors.append("파일 형식 오류")

    if video_codec != spec["video_codec"]:
        errors.append("영상 코덱 오류")

    if audio_codec != spec["audio_codec"]:
        errors.append("오디오 코덱 오류")

    if file_mb > spec["max_file_mb"]:
        errors.append("파일 용량 초과")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
