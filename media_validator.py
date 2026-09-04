from media_spec import get_media_spec


def check_ratio(width, height, target_ratio, tolerance=0.03):
    if height == 0:
        return False

    ratio = width / height

    return abs(ratio - target_ratio) <= tolerance



def validate_image(
    width,
    height,
    file_mb,
    file_format,
    media_type="BLOG_IMAGE"
):

    spec = get_media_spec(media_type)

    errors = []


    if width < spec["min_width"]:
        errors.append("가로 해상도 부족")


    if height < spec["min_height"]:
        errors.append("세로 해상도 부족")


    if file_mb < spec["min_file_mb"]:
        errors.append("파일 용량 부족")


    if file_mb > spec["max_file_mb"]:
        errors.append("파일 용량 초과")


    if file_format.lower() not in spec["formats"]:
        errors.append("지원하지 않는 이미지 형식")


    valid = len(errors) == 0


    return {
        "valid": valid,
        "errors": errors
    }



def validate_video(
    width,
    height,
    seconds,
    file_mb,
    fps,
    container,
    video_codec,
    audio_codec
):

    spec = get_media_spec(
        "SHORT_VIDEO"
    )

    errors = []


    if width < spec["width"]:
        errors.append("가로 해상도 부족")


    if height < spec["height"]:
        errors.append("세로 해상도 부족")


    if not check_ratio(
        width,
        height,
        spec["ratio"]
    ):
        errors.append("9:16 비율 아님")


    if seconds < spec["min_seconds"]:
        errors.append("영상 길이 부족")


    if seconds > spec["max_seconds"]:
        errors.append("영상 길이 초과")


    if file_mb < spec["min_file_mb"]:
        errors.append("영상 용량 부족")


    if file_mb > spec["max_file_mb"]:
        errors.append("영상 용량 초과")


    if container.lower() != spec["container"]:
        errors.append("MP4 아님")


    if video_codec != spec["video_codec"]:
        errors.append("영상 코덱 불일치")


    if audio_codec != spec["audio_codec"]:
        errors.append("음성 코덱 불일치")


    if fps < spec["fps_min"]:
        errors.append("FPS 부족")


    if fps > spec["fps_max"]:
        errors.append("FPS 초과")


    valid = len(errors) == 0


    return {
        "valid": valid,
        "errors": errors
    }
