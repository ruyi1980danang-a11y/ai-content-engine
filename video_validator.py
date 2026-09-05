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
    audio_codec,
    estimated_cost=0,
    narration_used=False,
    narration_required=False,
    caption_used=True,
    caption_length=0
):

    spec = get_video_spec(platform)

    errors = []


    # =========================
    # RESOLUTION
    # =========================

    if width != spec["width"]:
        errors.append("해상도 오류")

    if height != spec["height"]:
        errors.append("해상도 오류")


    if width < spec["min_width"]:
        errors.append("최소 해상도 부족")

    if height < spec["min_height"]:
        errors.append("최소 해상도 부족")


    # =========================
    # LENGTH
    # =========================

    if seconds < spec["min_seconds"]:
        errors.append("영상 길이 부족")

    if seconds > spec["max_seconds"]:
        errors.append("영상 길이 초과")


    # =========================
    # FPS
    # =========================

    if fps < spec["fps_min"]:
        errors.append("FPS 부족")

    if fps > spec["fps_max"]:
        errors.append("FPS 초과")

    if fps < spec["min_fps"]:
        errors.append("최소 FPS 부족")


    # =========================
    # FORMAT
    # =========================

    if file_format.lower() != spec["format"]:
        errors.append("파일 형식 오류")


    # =========================
    # CODEC
    # =========================

    if video_codec != spec["video_codec"]:
        errors.append("영상 코덱 오류")


    if audio_codec != spec["audio_codec"]:
        errors.append("오디오 코덱 오류")


    # =========================
    # FILE SIZE
    # =========================

    if file_mb > spec["max_file_mb"]:
        errors.append("파일 용량 초과")


    # =========================
    # COST CONTROL
    # =========================

    if estimated_cost > spec["max_cost_usd"]:
        errors.append(
            "영상 제작 비용 초과"
        )


    # =========================
    # NARRATION
    # =========================

    if (
        narration_required
        and not narration_used
    ):
        errors.append(
            "필수 나레이션 없음"
        )


    # =========================
    # CAPTION
    # =========================

    if (
        spec["caption_required"]
        and not caption_used
    ):
        errors.append(
            "필수 자막 없음"
        )


    if caption_length > spec["caption_max_length"]:
        errors.append(
            "자막 길이 초과"
        )


    return {

        "valid": len(errors) == 0,

        "errors": errors,

        "platform": platform,

        "spec": spec

    }
