import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# COST CONTROL
# ============================================================

MONTHLY_LIMIT_USD = 100.00
DAILY_LIMIT_USD = 10.00
RUN_LIMIT_USD = 5.00
SOURCE_LIMIT_USD = 1.00

MAX_REGENERATIONS_PER_SOURCE = 2

INPUT_PRICE_PER_1M = 4.00
OUTPUT_PRICE_PER_1M = 20.00

COST_SAFETY_FACTOR = 1.20

MAX_OUTPUT_TOKENS = 12000


def estimate_cost(input_tokens, output_tokens):
    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_PRICE_PER_1M

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_PRICE_PER_1M

    return (
        input_cost + output_cost
    ) * COST_SAFETY_FACTOR


def count_tokens_estimate(text):
    if not text:
        return 0

    return max(1, len(text) // 4)


def check_source_cost(input_text, master_prompt):
    estimated_input_tokens = (
        count_tokens_estimate(master_prompt)
        + count_tokens_estimate(input_text)
    )

    estimated_output_tokens = MAX_OUTPUT_TOKENS

    estimated_cost = estimate_cost(
        estimated_input_tokens,
        estimated_output_tokens
    )

    print(
        f"예상 최대 실행 비용: "
        f"${estimated_cost:.4f}"
    )

    if estimated_cost > RUN_LIMIT_USD:
        raise RuntimeError(
            "COST_LIMIT_STOP: "
            f"예상 실행 비용 ${estimated_cost:.4f} "
            f"> 실행 한도 ${RUN_LIMIT_USD:.2f}"
        )

    if estimated_cost > SOURCE_LIMIT_USD:
        raise RuntimeError(
            "COST_LIMIT_STOP: "
            f"예상 소재 비용 ${estimated_cost:.4f} "
            f"> 소재 한도 ${SOURCE_LIMIT_USD:.2f}"
        )

    return estimated_cost


# ============================================================
# MASTER PROMPT
# ============================================================

def load_master_prompt():
    prompt_path = (
        Path(__file__).parent
        / "MASTER_PROMPT.md"
    )

    if not prompt_path.exists():
        raise FileNotFoundError(
            "MASTER_PROMPT.md 파일을 찾을 수 없습니다."
        )

    return prompt_path.read_text(
        encoding="utf-8"
    )


# ============================================================
# GOOGLE SHEETS
# ============================================================

def get_google_sheet_data():
    sheet_url = os.environ.get(
        "GOOGLE_SHEET_URL"
    )

    if not sheet_url:
        raise RuntimeError(
            "GOOGLE_SHEET_URL이 설정되어 있지 않습니다."
        )

    request = urllib.request.Request(
        sheet_url,
        method="GET"
    )

    try:
        with urllib.request.urlopen(
            request
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result

    except urllib.error.HTTPError as error:
        error_body = error.read().decode(
            "utf-8"
        )

        raise RuntimeError(
            f"Google Sheets 읽기 오류: "
            f"{error_body}"
        )


def save_result_to_google_sheet(
    story_data
):
    sheet_url = os.environ.get(
        "GOOGLE_SHEET_URL"
    )

    if not sheet_url:
        raise RuntimeError(
            "GOOGLE_SHEET_URL가 설정되어 있지 않습니다."
        )

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
        with urllib.request.urlopen(
            request
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result

    except urllib.error.HTTPError as error:
        error_body = error.read().decode(
            "utf-8"
        )

        raise RuntimeError(
            f"Google Sheets 저장 오류: "
            f"{error_body}"
        )


# ============================================================
# OPENAI
# ============================================================

def ask_openai(
    master_prompt,
    material,
    original_data
):

    api_key = os.environ.get(
        "OPENAI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY가 설정되어 있지 않습니다."
        )

    input_text = f"""
다음 실제 원자료를 바탕으로
MASTER_PROMPT의 모든 규칙을 적용하여
콘텐츠를 생성하라.

[소재]
{material}

[원자료]
{original_data}

중요 규칙:

1. 하나의 소재에 대해 12개 계정의
   독립적인 콘텐츠를 생성한다.

2. 12개 계정은 각각 하나의 완성된
   콘텐츠를 가져야 한다.

3. 계정별 관점과 이야기 구조를
   자연스럽게 차별화한다.

4. 사실을 확인할 수 없는 내용을
   사실처럼 만들지 않는다.

5. 사진은 필요한 경우에만 사용한다.

6. 영상은 필요한 경우에만 CREATE한다.

7. 사진과 영상의 정확성이 확인되지
   않으면 사용하지 않는다.

8. 불필요한 검색과 생성은 하지 않는다.

9. MASTER_PROMPT의 최종 출력 형식을
   반드시 따른다.

10. 최종 결과는 사람이 검토한 뒤
    수동 업로드할 것을 전제로 한다.
"""

    estimated_cost = check_source_cost(
        input_text,
        master_prompt
    )

    data = {
        "model": "gpt-5.6-sol",
        "instructions": master_prompt,
        "input": input_text,
        "max_output_tokens": MAX_OUTPUT_TOKENS
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8"),
        headers={
            "Authorization":
                f"Bearer {api_key}",
            "Content-Type":
                "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:
        error_body = error.read().decode(
            "utf-8"
        )

        if (
            "spend_limit" in error_body
            or "insufficient_quota" in error_body
            or "usage_limit" in error_body
        ):
            raise RuntimeError(
                "COST_LIMIT_STOP: "
                f"{error_body}"
            )

        raise RuntimeError(
            f"OpenAI API 오류: "
            f"{error_body}"
        )

    usage = result.get("usage", {})

    input_tokens = usage.get(
        "input_tokens",
        count_tokens_estimate(
            master_prompt
        ) + count_tokens_estimate(
            input_text
        )
    )

    output_tokens = usage.get(
        "output_tokens",
        count_tokens_estimate(
            result.get("output_text", "")
        )
    )

    actual_cost = estimate_cost(
        input_tokens,
        output_tokens
    )

    print(
        f"실제 추정 API 비용: "
        f"${actual_cost:.6f}"
    )

    if actual_cost > RUN_LIMIT_USD:
        raise RuntimeError(
            "COST_LIMIT_STOP: "
            f"실제 추정 실행 비용 "
            f"${actual_cost:.6f} "
            f"> ${RUN_LIMIT_USD:.2f}"
        )

    if actual_cost > SOURCE_LIMIT_USD:
        raise RuntimeError(
            "COST_LIMIT_STOP: "
            f"실제 추정 소재 비용 "
            f"${actual_cost:.6f} "
            f"> ${SOURCE_LIMIT_USD:.2f}"
        )

    return {
        "story": result.get(
            "output_text",
            ""
        ),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": actual_cost,
        "estimated_max_cost_usd":
            estimated_cost
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("AI STORY ENGINE 시작")

    print(
        f"월간 비용 상한: "
        f"${MONTHLY_LIMIT_USD:.2f}"
    )

    print(
        f"일일 비용 상한: "
        f"${DAILY_LIMIT_USD:.2f}"
    )

    print(
        f"1회 실행 상한: "
        f"${RUN_LIMIT_USD:.2f}"
    )

    print(
        f"소재 1개 상한: "
        f"${SOURCE_LIMIT_USD:.2f}"
    )

    print(
        "소재당 최대 재생성: "
        f"{MAX_REGENERATIONS_PER_SOURCE}회"
    )

    master_prompt = load_master_prompt()

    print(
        "MASTER_PROMPT.md 불러오기 성공"
    )

    source_data = get_google_sheet_data()

    if not source_data.get("success"):
        print(
            "처리할 소재가 없습니다."
        )
        return

    material = source_data.get(
        "소재",
        ""
    )

    original_data = source_data.get(
        "원자료",
        ""
    )

    row_number = source_data.get(
        "row"
    )

    if not material and not original_data:
        print(
            "처리할 소재가 없습니다."
        )
        return

    print("소재 확인 완료")

    if row_number:
        print(
            f"처리 대상 행: {row_number}"
        )

    print(
        "OpenAI 콘텐츠 생성 시작"
    )

    result = ask_openai(
        master_prompt,
        material,
        original_data
    )

    story = result.get(
        "story",
        ""
    )

    if not story:
        raise RuntimeError(
            "OpenAI에서 콘텐츠를 생성하지 못했습니다."
        )

    print(
        "콘텐츠 생성 완료"
    )

    result_data = {
        "row": row_number,
        "소재": material,
        "원자료": original_data,
        "글": story,
        "상태": "생성완료",
        "결과": "PASS"
    }

    save_result_to_google_sheet(
        result_data
    )

    print(
        "Google Sheets 저장 완료"
    )

    print(
        "AI STORY ENGINE 작업 완료"
    )


if __name__ == "__main__":
    main()
