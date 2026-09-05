# video_cost_control.py


VIDEO_COST_LIMITS = {

    "MONTHLY_LIMIT_USD": 100.00,

    "DAILY_LIMIT_USD": 10.00,

    "RUN_LIMIT_USD": 5.00,

    "VIDEO_LIMIT_USD": 1.00

}


VIDEO_COST = {

    "GENERATION": 0,

    "SEARCH": 0,

    "VOICE": 0,

    "MUSIC": 0,

    "TOTAL": 0

}



def estimate_video_cost(
    generation_cost=0,
    search_cost=0,
    voice_cost=0,
    music_cost=0
):

    total = (
        generation_cost
        + search_cost
        + voice_cost
        + music_cost
    )

    return {
        "generation": generation_cost,
        "search": search_cost,
        "voice": voice_cost,
        "music": music_cost,
        "total": total
    }



def validate_video_cost(cost_data):

    errors = []

    total = cost_data.get(
        "total",
        0
    )


    if total > VIDEO_COST_LIMITS["VIDEO_LIMIT_USD"]:

        errors.append(
            "영상 1개 비용 초과"
        )


    if total > VIDEO_COST_LIMITS["RUN_LIMIT_USD"]:

        errors.append(
            "실행 비용 초과"
        )


    return {

        "valid": len(errors) == 0,

        "errors": errors,

        "cost": total

    }



def add_video_cost(cost_data):

    VIDEO_COST["GENERATION"] += cost_data.get(
        "generation",
        0
    )

    VIDEO_COST["SEARCH"] += cost_data.get(
        "search",
        0
    )

    VIDEO_COST["VOICE"] += cost_data.get(
        "voice",
        0
    )

    VIDEO_COST["MUSIC"] += cost_data.get(
        "music",
        0
    )

    VIDEO_COST["TOTAL"] += cost_data.get(
        "total",
        0
    )


def get_video_cost():

    return VIDEO_COST
