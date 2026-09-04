import os
import json
import urllib.request
import urllib.error
from pathlib import Path


def load_master_prompt():
    prompt_path = Path(__file__).parent / "MASTER_PROMPT.md"

    if not prompt_path.exists():
        raise FileNotFoundError("MASTER_PROMPT.md 파일을 찾을 수 없습니다.")

    return prompt_path.read_text(encoding="utf-8")


def get_google_sheet_data():
    sheet_url = os.environ.get("GOOGLE_SHEET_URL")

    if not sheet_url:
        raise RuntimeError("GOOGLE_SHEET_URL이 설정되어 있지 않습니다.")

    request = urllib.request.Request(
        sheet_url,
        method="GET"
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")
        raise RuntimeError(f"Google Sheets 읽기 오류: {error_body}")


def ask_openai(master_prompt, material, original_data):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    url = "https://api.openai.com/v1/responses"

    input_text = f"""
다음 실제 원자료를 바탕으로 MASTER_PROMPT의 규칙에 따라 하나의 완성된 이야기를 만들어라.

[소재]
{material}

[원자료]
{original_data}

실제 사건·현상·경험을 기반으로 하되, 단순한 정보 나열이 아니라
스토리텔링으로 재구성하라.

MASTER_PROMPT의 최종 출력 형식을 반드시 따른다.
"""

    data = {
        "model": "gpt-5.6-sol",
        "instructions": master_prompt,
        "input": input_text
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result.get("output_text", "")

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")
        raise RuntimeError(f"OpenAI API 오류: {error_body}")


def save_result_to_google_sheet(story_data):
    sheet_url = os.environ.get("GOOGLE_SHEET_URL")

    if not sheet_url:
        raise RuntimeError("GOOGLE_SHEET_URL이 설정되어 있지 않습니다.")

    data = json.dumps(
        story_data,
        ensure_ascii=False
    ).encode("utf-8")

    request = urllib.request.Request(
        sheet_url,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")
        raise RuntimeError(f"Google Sheets 저장 오류: {error_body}")


def main():
    print("AI STORY ENGINE 시작")

    master_prompt = load_master_prompt()
    print("MASTER_PROMPT.md 불러오기 성공")

    source_data = get_google_sheet_data()

    if not source_data.get("success"):
        raise RuntimeError(
            "Google Sheets에서 사용할 소재를 가져오지 못했습니다."
        )

    material = source_data.get("소재", "")
    original_data = source_data.get("원자료", "")

    if not material and not original_data:
        print("처리할 소재가 없습니다.")
        return

    print("소재 확인 완료")
    print("OpenAI 이야기 생성 시작")

    story = ask_openai(
        master_prompt,
        material,
        original_data
    )

    if not story:
        raise RuntimeError("OpenAI에서 이야기를 생성하지 못했습니다.")

    print("이야기 생성 완료")

    result_data = {
        "소재": material,
        "원자료": original_data,
        "글": story,
        "상태": "생성완료",
        "결과": "PASS"
    }

    save_result_to_google_sheet(result_data)

    print("Google Sheets 저장 완료")
    print("AI STORY ENGINE 작업 완료")


if __name__ == "__main__":
    main()
