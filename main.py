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


def ask_openai(master_prompt):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    url = "https://api.openai.com/v1/responses"

    data = {
        "model": "gpt-5.6-sol",
        "instructions": master_prompt,
        "input": "AI STORY CONTENT ENGINE이 준비되었는지 확인하고, '시스템 준비 완료'라고 답해줘."
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
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


if __name__ == "__main__":
    master_prompt = load_master_prompt()

    print("MASTER_PROMPT.md 불러오기 성공")
    print("OpenAI API 연결을 시작합니다.")

    result = ask_openai(master_prompt)

    print("=" * 60)
    print(result)
    print("=" * 60)
