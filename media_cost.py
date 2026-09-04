MEDIA_COST = {

    "UNSPLASH": {
        "cost": 0
    },

    "PEXELS": {
        "cost": 0
    },

    "PIXABAY": {
        "cost": 0
    },

    "OPENAI_IMAGE": {
        "cost_per_image": 0.04
    },

    "VIDEO_GENERATION": {
        "cost_per_video": 0
    }
}


def calculate_cost(
    source,
    quantity=1
):

    if source not in MEDIA_COST:
        return 0

    item = MEDIA_COST[source]

    if "cost" in item:
        return item["cost"] * quantity

    if "cost_per_image" in item:
        return item["cost_per_image"] * quantity

    if "cost_per_video" in item:
        return item["cost_per_video"] * quantity

    return 0
