# video_length_control.py


VIDEO_LENGTH_RULES = {

    "SHORT": {
        "min_seconds": 10,
        "max_seconds": 30
    },

    "STANDARD": {
        "min_seconds": 30,
        "max_seconds": 60
    },

    "LONG_SHORT": {
        "min_seconds": 60,
        "max_seconds": 180
    }

}



def decide_video_length(
    story,
    character_count=0,
    video_type=""
):

    if character_count <= 0:

        character_count = len(
            story
        )


    if video_type in [
        "news",
        "fact",
        "history"
    ]:

        if character_count >= 2000:

            return {
                "type": "LONG_SHORT",
                "seconds": 120,
                "reason": "정보 전달형 긴 영상"
            }


        return {
            "type": "STANDARD",
            "seconds": 60,
            "reason": "정보 전달형"
        }



    if video_type in [
        "emotional",
        "story",
        "documentary"
    ]:

        if character_count >= 1500:

            return {
                "type": "STANDARD",
                "seconds": 60,
                "reason": "스토리 전달 필요"
            }


        return {
            "type": "SHORT",
            "seconds": 30,
            "reason": "핵심 장면 중심"
        }



    if character_count >= 2500:

        return {
            "type": "LONG_SHORT",
            "seconds": 90,
            "reason": "긴 콘텐츠 가치 있음"
        }


    if character_count >= 1000:

        return {
            "type": "STANDARD",
            "seconds": 45,
            "reason": "일반 숏츠"
        }


    return {
        "type": "SHORT",
        "seconds": 20,
        "reason": "짧은 전달"
    }



def validate_video_length(
    seconds,
    length_type
):

    if length_type not in VIDEO_LENGTH_RULES:

        return {
            "valid": False,
            "error": "알 수 없는 영상 길이 타입"
        }


    rule = VIDEO_LENGTH_RULES[
        length_type
    ]


    if seconds < rule["min_seconds"]:

        return {
            "valid": False,
            "error": "영상 길이 부족"
        }


    if seconds > rule["max_seconds"]:

        return {
            "valid": False,
            "error": "영상 길이 초과"
        }


    return {
        "valid": True,
        "error": ""
    }



def calculate_monthly_video_target(
    selected_contents,
    target=200
):

    if len(selected_contents) <= target:

        return selected_contents


    return selected_contents[
        :target
    ]
