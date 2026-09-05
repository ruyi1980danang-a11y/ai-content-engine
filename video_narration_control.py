def decide_narration(
    content_type,
    story_length,
    video_length
):

    result = {
        "narration": False,
        "reason": "",
        "estimated_seconds": 0
    }


    # 정보 전달형
    if content_type == "INFO":
        result["narration"] = True
        result["reason"] = "정보 전달 필요"
    

    # 스토리형
    elif content_type == "STORY":
        result["narration"] = True
        result["reason"] = "감정 전달 필요"


    # 짧은 이미지 중심
    elif content_type == "IMAGE":
        result["narration"] = False
        result["reason"] = "자막만 사용"


    # 기본 판단
    else:
        if story_length > 500:
            result["narration"] = True
            result["reason"] = "긴 원고 전달 필요"
        else:
            result["narration"] = False
            result["reason"] = "비용 절감"


    if result["narration"]:
        result["estimated_seconds"] = video_length


    return result
