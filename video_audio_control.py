# video_audio_control.py


AUDIO_RULES = {

    "MAX_AUDIO_TRACKS": 2,

    "SUPPORTED_AUDIO": [
        "narration",
        "background_music",
        "sound_effect"
    ],

    "DEFAULT_VOLUME": {

        "narration": 100,

        "background_music": 25,

        "sound_effect": 40

    }

}



def decide_audio_structure(
    narration_status,
    video_type,
    music_required=False
):

    tracks = []


    if narration_status == "CREATE":

        tracks.append(
            {
                "type": "narration",
                "required": True,
                "volume": AUDIO_RULES["DEFAULT_VOLUME"]["narration"]
            }
        )


    if music_required:

        tracks.append(
            {
                "type": "background_music",
                "required": False,
                "volume": AUDIO_RULES["DEFAULT_VOLUME"]["background_music"]
            }
        )


    if video_type in [
        "documentary",
        "emotional",
        "story"
    ]:

        tracks.append(
            {
                "type": "sound_effect",
                "required": False,
                "volume": AUDIO_RULES["DEFAULT_VOLUME"]["sound_effect"]
            }
        )


    return {
        "audio_tracks": tracks,
        "track_count": len(tracks)
    }



def validate_audio_package(
    audio_package
):

    errors = []


    if not audio_package:

        errors.append(
            "오디오 데이터 없음"
        )


    track_count = audio_package.get(
        "track_count",
        0
    )


    if track_count > AUDIO_RULES["MAX_AUDIO_TRACKS"]:

        errors.append(
            "오디오 트랙 수 초과"
        )


    tracks = audio_package.get(
        "audio_tracks",
        []
    )


    for track in tracks:

        if track.get("type") not in AUDIO_RULES["SUPPORTED_AUDIO"]:

            errors.append(
                "지원하지 않는 오디오 타입"
            )


        if (
            track.get("volume", 0) < 0
            or track.get("volume", 0) > 100
        ):

            errors.append(
                "오디오 볼륨 범위 오류"
            )


    return {

        "valid": len(errors) == 0,

        "errors": errors

    }



def calculate_audio_cost(
    narration=False,
    music=False,
    sound_effect=False
):

    cost = 0


    if narration:

        cost += 0.02


    if music:

        cost += 0.005


    if sound_effect:

        cost += 0.005


    return round(
        cost,
        4
    )
