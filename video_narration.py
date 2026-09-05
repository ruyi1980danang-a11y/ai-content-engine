# video_narration.py


NARRATION_RULES = {

    "REQUIRED_TYPES": [
        "history",
        "documentary",
        "explanation",
        "emotional",
        "story"
    ],

    "OPTIONAL_TYPES": [
        "short_news",
        "review",
        "experience"
    ],

    "SKIP_TYPES": [
        "simple_showcase",
        "image_only",
        "music_visual"
    ]

}



def check_narration_need(
    video_type,
    story_length=0,
    emotional_score=0
):

    if video_type in NARRATION_RULES["REQUIRED_TYPES"]:

        return {
            "decision": "CREATE",
            "reason": "스토리 전달 필요"
        }


    if video_type in NARRATION_RULES["SKIP_TYPES"]:

        return {
            "decision": "SKIP",
            "reason": "나레이션 불필요"
        }


    if (
        story_length >= 1000
        or emotional_score >= 7
    ):

        return {
            "decision": "CREATE",
            "reason": "추가 설명 필요"
        }


    return {
        "decision": "OPTIONAL",
        "reason": "영상 특성 판단 필요"
    }



def create_narration_package(
    script,
    narration_decision,
    voice_type="natural"
):

    if narration_decision != "CREATE":

        return {
            "status": "skip",
            "narration": None
        }


    if not script:

        return {
            "status": "failed",
            "error": "스크립트 없음"
        }


    return {

        "status": "success",

        "narration": {

            "script": script,

            "voice_type": voice_type,

            "language": "ko"

        }

    }



def validate_narration(
    narration
):

    errors = []


    if not narration:

        errors.append(
            "나레이션 데이터 없음"
        )


    if len(errors) > 0:

        return {

            "valid": False,

            "errors": errors

        }


    return {

        "valid": True,

        "errors": []

    }
