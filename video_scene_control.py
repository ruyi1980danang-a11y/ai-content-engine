# video_scene_control.py


SCENE_RULES = {

    "MAX_SCENES": 12,

    "MIN_SCENES": 3

}



def create_scene_plan(
    video_length,
    video_type,
    visual_plan=""
):

    scenes = []


    if video_length <= 30:

        scene_count = 5

    elif video_length <= 60:

        scene_count = 8

    else:

        scene_count = 12


    for i in range(1, scene_count + 1):

        scenes.append({

            "scene": i,

            "duration": round(
                video_length / scene_count,
                1
            ),

            "visual": visual_plan,

            "caption": "",

            "narration": ""

        })


    return {

        "scene_count": scene_count,

        "scenes": scenes

    }



def validate_scene_plan(
    scene_plan
):

    errors = []


    if not scene_plan:

        errors.append(
            "씬 계획 없음"
        )

        return {
            "valid": False,
            "errors": errors
        }


    count = scene_plan.get(
        "scene_count",
        0
    )


    if count < SCENE_RULES["MIN_SCENES"]:

        errors.append(
            "씬 부족"
        )


    if count > SCENE_RULES["MAX_SCENES"]:

        errors.append(
            "씬 초과"
        )


    return {

        "valid": len(errors) == 0,

        "errors": errors

    }
