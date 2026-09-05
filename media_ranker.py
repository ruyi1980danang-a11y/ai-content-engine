# media_ranker.py


def calculate_quality_score(photo):

    score = 0


    # 해상도 점수
    width = photo.get("width", 0)
    height = photo.get("height", 0)


    if width >= 2000:
        score += 40
    elif width >= 1600:
        score += 30
    elif width >= 1200:
        score += 20


    if height >= 1200:
        score += 30
    elif height >= 900:
        score += 20
    elif height >= 700:
        score += 10



    # 출처 점수

    source = photo.get("source", "")


    if source == "Unsplash":
        score += 20

    elif source == "Pexels":
        score += 15

    elif source == "Pixabay":
        score += 10



    return score



def rank_photos(photos):

    for photo in photos:
        photo["score"] = calculate_quality_score(photo)


    return sorted(
        photos,
        key=lambda x: x["score"],
        reverse=True
    )



def select_best_photo(photos):

    ranked = rank_photos(photos)


    if ranked:
        return ranked[0]


    return None
