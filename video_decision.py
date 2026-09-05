# video_decision.py


VIDEO_TARGET_MONTHLY = 200


VIDEO_DECISION_RULES = {

    "MIN_CHARACTER_COUNT": 500,

    "MIN_HOOK_SCORE": 7,

    "MIN_STORY_VALUE": 7,

    "MAX_DAILY_VIDEO": 10

}



def calculate_video_score(
    character_count=0,
    hook_score=0,
    story_value=0,
    emotional_score=0
):

    score = (
        character_count_score(character_count)
        + hook_score
        + story_value
        + emotional_score
    )

    return score



def character_count_score(
    character_count
):

    if character_count >= 2000:
        return 3

    if character_count >= 1000:
        return 2

    if character_count >= 500:
        return 1

    return 0



def decide_video_creation(
    content
):

    character_count = content.get(
        "character_count",
        0
    )

    hook_score = content.get(
        "hook_score",
        0
    )

    story_value = content.get(
        "story_value",
        0
    )

    emotional_score = content.get(
        "emotional_score",
        0
    )


    score = calculate_video_score(
        character_count,
        hook_score,
        story_value,
        emotional_score
    )


    if score >= 12:

        return {
            "decision": "CREATE",
            "score": score,
            "reason": "영상 제작 가치 충분"
        }


    return {
        "decision": "SKIP",
        "score": score,
        "reason": "영상 제작 가치 부족"
    }



def decide_narration(
    video_data
):

    if video_data.get(
        "decision"
    ) != "CREATE":

        return {
            "narration": "SKIP"
        }


    if video_data.get(
        "story_type"
    ) in [
        "history",
        "documentary",
        "explanation",
        "emotional"
    ]:

        return {
            "narration": "CREATE"
        }


    return {
        "narration": "OPTIONAL"
    }



def select_monthly_video(
    contents
):

    selected = []


    for content in contents:

        result = decide_video_creation(
            content
        )

        if result["decision"] == "CREATE":

            content["video_score"] = result["score"]

            selected.append(
                content
            )


    selected.sort(
        key=lambda x: x.get(
            "video_score",
            0
        ),
        reverse=True
    )


    return selected[
        :VIDEO_TARGET_MONTHLY
    ]
