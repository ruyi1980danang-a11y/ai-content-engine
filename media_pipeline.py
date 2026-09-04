from photo_search import get_best_photo


def create_media_package(
    keyword,
    unsplash_key
):

    photo = get_best_photo(
        keyword,
        unsplash_key
    )

    if not photo:
        return {
            "status": "failed",
            "photo": None
        }

    return {
        "status": "success",
        "photo": photo
    }
