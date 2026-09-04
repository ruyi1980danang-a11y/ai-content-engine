import os
import json
import urllib.request
import urllib.error
import uuid
from pathlib import Path
from datetime import datetime, timezone
from photo_search import get_best_photo
from media_pipeline import create_media_package
from video_pipeline import create_video_package

# ============================================================
# AI STORY CONTENT ENGINE
# main.py
# ============================================================

SPREADSHEET_URL = os.environ.get("GOOGLE_SHEET_URL")

OPENAI_API_URL = "https://api.openai.com/v1/responses"

MODEL = "gpt-5.6-sol"

# ------------------------------------------------------------
# COST CONTROL
# ------------------------------------------------------------

MONTHLY_LIMIT_USD = 150.00
DAILY_LIMIT_USD = 10.00
RUN_LIMIT_USD = 5.00
SOURCE_LIMIT_USD = 1.00

MAX_REGENERATIONS_PER_SOURCE = 2

INPUT_PRICE_PER_1M = 4.00
OUTPUT_PRICE_PER_1M = 20.00

COST_SAFETY_FACTOR = 1.20

MAX_OUTPUT_TOKENS = 12000


# ------------------------------------------------------------
# 12 ACCOUNTS
# ------------------------------------------------------------

ACCOUNTS = [
    ("Angel 10", "ANGEL"),
    ("Angel 20", "ANGEL"),
    ("Angel 30", "ANGEL"),
    ("Angel 40", "ANGEL"),
    ("Angel 50", "ANGEL"),
    ("Angel 60", "ANGEL"),
    ("Devil 10", "DEVIL"),
    ("Devil 20", "DEVIL"),
    ("Devil 30", "DEVIL"),
    ("Devil 40", "DEVIL"),
    ("Devil 50", "DEVIL"),
    ("Devil 60", "DEVIL"),
]


# ============================================================
# COST
# ============================================================

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
        f"예상 최대 실행 비용: ${estimated_cost:.4f}"
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
    if not SPREADSHEET_URL:
        raise RuntimeError(
            "GOOGLE_SHEET_URL이 설정되어 있지 않습니다."
        )

    request = urllib.request.Request(
        SPREADSHEET_URL,
        method="GET"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        return result

    except urllib.error.HTTPError as error:
        error_body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            "Google Sheets 읽기 오류: "
            f"{error_body}"
        )


def save_rows_to_google_sheet(rows):
    if not SPREADSHEET_URL:
        raise RuntimeError(
            "GOOGLE_SHEET_URL이 설정되어 있지 않습니다."
        )

    payload = {
        "action": "save_rows",
        "rows": rows
    }

    data = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    request = urllib.request.Request(
        SPREADSHEET_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        if not result.get("success"):
            raise RuntimeError(
                "Google Sheets 저장 실패: "
                f"{result}"
            )

        return result

    except urllib.error.HTTPError as error:
        error_body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            "Google Sheets 저장 오류: "
            f"{error_body}"
        )


# ============================================================
# OPENAI STRUCTURED OUTPUT SCHEMA
# ============================================================

def build_schema():
    account_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "account": {
                "type": "string"
            },
            "account_type": {
                "type": "string"
            },
            "title": {
                "type": "string"
            },
            "story": {
                "type": "string"
            },
            "photo_plan": {
                "type": "string"
            },
            "keywords": {
                "type": "string"
            },
            "story_memory": {
                "type": "string"
            },
            "character_count": {
                "type": "integer"
            },
            "quality_result": {
                "type": "string"
            },
            "video_decision": {
                "type": "string"
            },
            "video_type": {
                "type": "string"
            },
            "video_length": {
                "type": "string"
            },
            "video_hook": {
                "type": "string"
            },
            "video_core": {
                "type": "string"
            },
            "video_script": {
                "type": "string"
            },
            "video_scene_plan": {
                "type": "string"
            },
            "video_visual_plan": {
                "type": "string"
            },
            "video_captions": {
                "type": "string"
            },
            "video_narration": {
                "type": "string"
            },
            "video_cta": {
                "type": "string"
            },
            "video_series": {
                "type": "string"
            },
            "platform_adaptation": {
                "type": "string"
            }
        },
        "required": [
            "account",
            "account_type",
            "title",
            "story",
            "photo_plan",
            "keywords",
            "story_memory",
            "character_count",
            "quality_result",
            "video_decision",
            "video_type",
            "video_length",
            "video_hook",
            "video_core",
            "video_script",
            "video_scene_plan",
            "video_visual_plan",
            "video_captions",
            "video_narration",
            "video_cta",
            "video_series",
            "platform_adaptation"
        ]
    }

    return {
        "type": "json_schema",
        "name": "ai_story_content_engine",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "accounts": {
                    "type": "array",
                    "items": account_schema,
                    "minItems": 12,
                    "maxItems": 12
                }
            },
            "required": [
                "accounts"
            ]
        }
    }


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

    account_instruction = "\n".join(
        [
            f"{index}. {name} ({account_type})"
            for index, (name, account_type)
            in enumerate(ACCOUNTS, start=1)
        ]
    )

    input_text = f"""
당신은 AI STORY CONTENT ENGINE의 콘텐츠 생성 엔진이다.

MASTER_PROMPT의 모든 규칙을 반드시 적용한다.

[실제 소재]
{material}

[실제 원자료]
{original_data}

[12개 계정]
{account_instruction}

==================================================
핵심 작업
==================================================

하나의 소재와 원자료를 이용하여
12개 계정 각각에 대해 독립적인 콘텐츠를 생성한다.

중요:

1. 하나의 소재를 12개 계정에 모두 적용한다.

2. 12개 콘텐츠는 서로 독립적이어야 한다.

3. 단순히 제목이나 문장만 바꾸는 방식으로
   같은 글을 복제하지 않는다.

4. 각 계정의 관점, 질문, 해석, 이야기 구조,
   인간적 관심사를 자연스럽게 차별화한다.

5. Angel/Devil 성격을 기계적인 선악 구도로
   만들지 않는다.

6. 나이는 고정된 성격이나 편견으로 사용하지 않는다.

7. 실제 원자료에 없는 사실을 만들어내지 않는다.

8. 약한 자료를 억지로 긴 이야기로 늘리지 않는다.

9. STORY는 최대 3,000자이며
   3,000자를 채우는 것이 목적이 아니다.

10. 품질이 부족하면 QUALITY RESULT를
    REWRITE 또는 DISCARD로 판단한다.

11. 사진은 필요한 경우에만 PHOTO PLAN을 작성한다.

12. 사진이 정확하지 않다면 억지로 사용하지 않는다.

13. 영상은 각 콘텐츠별로 독립적으로 판단한다.

14. 영상 가치가 충분하지 않으면
    VIDEO DECISION = SKIP으로 한다.

15. 영상 가치가 충분한 경우에만
    VIDEO DECISION = CREATE로 한다.

16. 영상은 긴 글을 단순히 줄이는 방식이 아니라
    영상에 적합한 구조로 재구성한다.

17. 영상 시리즈는 필요한 경우에만 사용한다.

18. 최종 결과는 사람이 검토한 후
    수동 업로드한다.

19. 모든 12개 계정을 반드시 반환한다.

20. 계정 이름은 다음 12개 이름과 정확히 일치해야 한다.
{account_instruction}
"""

    estimated_cost = check_source_cost(
        input_text,
        master_prompt
    )

    request_data = {
        "model": MODEL,
        "instructions": master_prompt,
        "input": input_text,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "text": {
            "format": build_schema()
        }
    }

    request = urllib.request.Request(
        OPENAI_API_URL,
        data=json.dumps(
            request_data,
            ensure_ascii=False
        ).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=300
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:
        error_body = error.read().decode(
            "utf-8",
            errors="replace"
        )

        if any(
            keyword in error_body
            for keyword in [
                "spend_limit",
                "insufficient_quota",
                "usage_limit"
            ]
        ):
            raise RuntimeError(
                "COST_LIMIT_STOP: "
                f"{error_body}"
            )

        raise RuntimeError(
            f"OpenAI API 오류: {error_body}"
        )

    output_text = result.get(
        "output_text",
        ""
    )

    if not output_text:
        raise RuntimeError(
            "OpenAI 응답에 output_text가 없습니다."
        )

    try:
        structured = json.loads(
            output_text
        )
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "OpenAI 구조화 결과 JSON 파싱 실패: "
            f"{error}"
        )

    usage = result.get(
        "usage",
        {}
    )

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
            output_text
        )
    )

    actual_cost = estimate_cost(
        input_tokens,
        output_tokens
    )

    print(
        f"실제 추정 API 비용: ${actual_cost:.6f}"
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
        "accounts": structured.get(
            "accounts",
            []
        ),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": actual_cost,
        "estimated_max_cost_usd": estimated_cost
    }


# ============================================================
# VALIDATION
# ============================================================

def validate_accounts(accounts):
    if not isinstance(accounts, list):
        raise RuntimeError(
            "AI 결과의 accounts가 배열이 아닙니다."
        )

    if len(accounts) != 12:
        raise RuntimeError(
            "AI가 12개 계정을 반환하지 않았습니다. "
            f"현재 {len(accounts)}개"
        )

    expected_names = {
        account[0]
        for account in ACCOUNTS
    }

    actual_names = {
        account.get("account")
        for account in accounts
    }

    if actual_names != expected_names:
        raise RuntimeError(
            "12개 계정 이름이 정확하지 않습니다."
        )

    for account in accounts:

        if not account.get("title"):
            raise RuntimeError(
                f"{account.get('account')} 제목이 없습니다."
            )

        if not account.get("story"):
            raise RuntimeError(
                f"{account.get('account')} 글이 없습니다."
            )

        quality = account.get(
            "quality_result"
        )

        if quality not in [
            "PASS",
            "REWRITE",
            "DISCARD",
            "HUMAN ESCALATION"
        ]:
            raise RuntimeError(
                f"{account.get('account')} "
                f"품질 결과가 올바르지 않습니다: {quality}"
            )

        video_decision = account.get(
            "video_decision"
        )

        if video_decision not in [
            "CREATE",
            "SKIP"
        ]:
            raise RuntimeError(
                f"{account.get('account')} "
                f"영상 결정이 올바르지 않습니다: "
                f"{video_decision}"
            )


# ============================================================
# ROW MAPPING
# ============================================================

def create_source_id():
    return (
        datetime.now(timezone.utc)
        .strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:10]
    )


def create_run_id():
    return (
        datetime.now(timezone.utc)
        .strftime("%Y%m%d%H%M%S")
        + "-"
        + uuid.uuid4().hex[:8]
    )


def account_to_sheet_row(
    account,
    material,
    original_data,
    source_id,
    run_id,
    source_cost
):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    quality_result = account.get(
        "quality_result",
        ""
    )

    video_decision = account.get(
        "video_decision",
        "SKIP"
    )

    video_status = (
        "CREATE"
        if video_decision == "CREATE"
        else "SKIP"
    )

    return {
        "소재": material,
        "원자료": original_data,

        "원자료출처": "",
        "자료검증": "",
        "검증결과": "",
        "검증일": "",

        "제목": account.get(
            "title",
            ""
        ),

        "계정": account.get(
            "account",
            ""
        ),

        "계정유형": account.get(
            "account_type",
            ""
        ),

        "상태": "검토대기",

        "날짜": now,

        "글": account.get(
            "story",
            ""
        ),

        "사진": account.get(
            "photo_plan",
            ""
        ),

        "키워드": account.get(
            "keywords",
            ""
        ),

        "콘텐츠결과": quality_result,

        "영상상태": video_status,

        "영상플랫폼": account.get(
            "platform_adaptation",
            ""
        ),

        "영상제목": account.get(
            "title",
            ""
        ),

        "영상훅": account.get(
            "video_hook",
            ""
        ),

        "영상스크립트": account.get(
            "video_script",
            ""
        ),

        "영상씬플랜": account.get(
            "video_scene_plan",
            ""
        ),

        "영상자막": account.get(
            "video_captions",
            ""
        ),

        "영상내레이션": account.get(
            "video_narration",
            ""
        ),

        "영상CTA": account.get(
            "video_cta",
            ""
        ),

        "영상비주얼": account.get(
            "video_visual_plan",
            ""
        ),

        "영상라이선스": "",

        "영상검증": "",

        "영상시리즈": account.get(
            "video_series",
            ""
        ),

        "영상결과": "",

        "검색횟수": 0,

        "검색비용": 0,

        "AI비용": source_cost,

        "이미지검색비용": 0,

        "영상검색비용": 0,

        "영상생성비용": 0,

        "총비용": source_cost,

        "재생성횟수": 0,

        "실행ID": run_id,

        "소재ID": source_id,

        "처리단계": "AI생성완료",

        "오류": "",

        "성과조회수": "",

        "성과완주율": "",

        "성과좋아요": "",

        "성과댓글": "",

        "성과공유": "",

        "성과팔로우": "",

        "성과점수": "",

        "학습반영": "미반영",

        "프롬프트버전": "MASTER_PROMPT",

        "모델버전": MODEL
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("AI STORY CONTENT ENGINE 시작")
    print("=" * 60)

    print(
        f"모델: {MODEL}"
    )

    print(
        f"월간 전체 비용 상한: ${MONTHLY_LIMIT_USD:.2f}"
    )

    print(
        f"1회 실행 상한: ${RUN_LIMIT_USD:.2f}"
    )

    print(
        f"소재 1개 상한: ${SOURCE_LIMIT_USD:.2f}"
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

    if not material or not original_data:
        raise RuntimeError(
            "소재 또는 원자료가 없습니다."
        )

    print(
        f"처리 대상 행: {row_number}"
    )

    print(
        f"소재: {material}"
    )

    print(
        "OpenAI 12계정 콘텐츠 생성 시작"
    )

    result = ask_openai(
        master_prompt,
        material,
        original_data
    )

    accounts = result.get(
        "accounts",
        []
    )

    validate_accounts(
        accounts
    )

    print(
        "12개 계정 구조 검증 완료"
    )

    source_id = create_source_id()
    run_id = create_run_id()

    source_cost = result.get(
        "estimated_cost_usd",
        0
    )

    rows = []

    for account in accounts:

        row = account_to_sheet_row(
            account=account,
            material=material,
            original_data=original_data,
            source_id=source_id,
            run_id=run_id,
            source_cost=source_cost
        )

        rows.append(row)

    if len(rows) != 12:
        raise RuntimeError(
            "저장할 행이 12개가 아닙니다."
        )

    print(
        "Google Sheets에 12개 콘텐츠 저장 시작"
    )

    save_result = save_rows_to_google_sheet(
        rows
    )

    print(
        f"Google Sheets 저장 결과: {save_result}"
    )

    print("=" * 60)
    print("AI STORY CONTENT ENGINE 작업 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
