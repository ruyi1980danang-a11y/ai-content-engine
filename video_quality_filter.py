# video_quality_filter.py


QUALITY_RULES = {

    "MIN_SCORE": 80,

    "CHECK_ITEMS": [

        "hook",

        "story",

        "visual",

        "audio",

        "length",

        "platform"

    ],

    "STATUS": [

        "PASS",

        "REWRITE",

        "DISCARD"

    ]

}



def calculate_quality_score(
    hook_score=0,
    story_score=0,
    visual_score=0,
    audio_score=0,
    length_score=0,
    platform_score=0
):

    total = (

        hook_score
        + story_score
        + visual_score
        + audio_score
        + length_score
        + platform_score

    )

    return round(
        total / 6,
        2
    )



def check_video_quality(
    video_data
):

    score = calculate_quality_score(

        video_data.get(
            "hook_score",
            0
        ),

        video_data.get(
            "story_score",
            0
        ),

        video_data.get(
            "visual_score",
            0
        ),

        video_data.get(
            "audio_score",
            0
        ),

        video_data.get(
            "length_score",
            0
        ),

        video_data.get(
            "platform_score",
            0
        )

    )


    if score >= QUALITY_RULES["MIN_SCORE"]:

        return {

            "quality": "PASS",

            "score": score,

            "reason": "제작 기준 통과"

        }


    if score >= 60:

        return {

            "quality": "REWRITE",

            "score": score,

            "reason": "수정 후 재검토 필요"

        }


    return {

        "quality": "DISCARD",

        "score": score,

        "reason": "제작 가치 부족"

    }



def validate_video_package(
    video_package
):

    errors = []


    required = [

        "title",

        "script",

        "scene_plan",

        "platform"

    ]


    for item in required:

        if not video_package.get(item):

            errors.append(
                f"{item} 없음"
            )


    return {

        "valid": len(errors) == 0,

        "errors": errors

    }
