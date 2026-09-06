from photo_search import get_best_photo
from media_validator import validate_image
from media_ranker import select_best_photo
from media_cost import calculate_cost
from diversity_controller import get_next_tone_category


def create_media_package(
    keyword
):

    tone_constraint = get_next_tone_category()

    photo_candidates = get_best_photo(
        keyword
    )


    if not photo_candidates:
        return {
            "status": "failed",
            "photo": None,
            "reason": "검색 결과 없음",
            "tone_constraint": tone_constraint
        }



    if isinstance(photo_candidates, dict):

        photos = [
            photo_candidates
        ]

    else:

        photos = photo_candidates



    valid_photos = []


    for photo in photos:

        result = validate_image(
            width=photo.get("width", 0),
            height=photo.get("height", 0),
            file_mb=photo.get("file_mb", 1),
            file_format=photo.get("format", "jpg"),
            media_type="BLOG_IMAGE"
        )


        if result["valid"]:

            valid_photos.append(
                photo
            )



    if not valid_photos:

        return {
            "status": "failed",
            "photo": None,
            "reason": "검증 통과 사진 없음",
            "tone_constraint": tone_constraint
        }



    best_photo = select_best_photo(
        valid_photos
    )


    cost = calculate_cost(
        best_photo.get("source", "").upper()
    )


    return {
        "status": "success",
        "photo": best_photo,
        "cost": cost,
        "tone_constraint": tone_constraint
    }
