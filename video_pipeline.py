from video_validator import validate_video
from video_spec import get_video_spec


def estimate_video_length(
    story,
    video_type
):

    length = len(story)

    if video_type in [
        "FACT",
        "DISCOVERY"
    ]:
        if length < 500:
            return 30
        elif length < 1500:
            return 60
        else:
            return 90


    if video_type in [
        "HUMAN",
        "EXPERIENCE"
    ]:
        if length < 700:
            return 45
        else:
            return 75


    if video_type == "LOCATION":

        if length < 500:
            return 30

        return 60


    return 30



def decide_narration(
    video_type
):

    if video_type == "FACT":
        return True

    if video_type == "DISCOVERY":
        return True

    return False



def estimate_video_cost(
    seconds
):

    # 기본 예상 비용
    # 실제 생성 API 연결 시 교체

    base_cost = 0.01

    return round(
        base_cost * seconds,
        4
    )



def create_video_package(
    platform,
    video_info=None,
    story="",
    video_type="STORY",
    video_decision="CREATE"
):

    if video_decision != "CREATE":

        return {
            "status": "skipped",
            "reason": "영상 제작 대상 아님"
        }



    if video_info is None:

        return {
            "status": "failed",
            "errors": [
                "video_info 없음"
            ]
        }



    spec = get_video_spec(
        platform
    )



    seconds = video_info.get(
        "seconds",
        estimate_video_length(
            story,
            video_type
        )
    )



    narration = decide_narration(
        video_type
    )



    estimated_cost = estimate_video_cost(
        seconds
    )



    if estimated_cost > spec["max_cost_usd"]:

        return {
            "status": "failed",
            "errors": [
                "영상 제작 비용 초과"
            ],
            "estimated_cost": estimated_cost
        }



    validation = validate_video(

        platform=platform,

        width=video_info.get(
            "width",
            0
        ),

        height=video_info.get(
            "height",
            0
        ),

        seconds=seconds,

        fps=video_info.get(
            "fps",
            0
        ),

        file_mb=video_info.get(
            "file_mb",
            0
        ),

        file_format=video_info.get(
            "format",
            ""
        ),

        video_codec=video_info.get(
            "video_codec",
            ""
        ),

        audio_codec=video_info.get(
            "audio_codec",
            ""
        ),

        estimated_cost=estimated_cost,

        narration_used=narration,

        narration_required=spec.get(
            "narration_required",
            False
        )

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

            "type": video_type,

            "seconds": seconds,

            "narration": narration,

            "estimated_cost": estimated_cost,

            "width": video_info["width"],

            "height": video_info["height"],

            "fps": video_info["fps"],

            "format": video_info["format"],

            "video_codec": video_info["video_codec"],

            "audio_codec": video_info["audio_codec"]

        }

    }
