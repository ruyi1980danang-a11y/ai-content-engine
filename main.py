from pathlib import Path


def load_master_prompt():
    prompt_path = Path(__file__).parent / "MASTER_PROMPT.md"

    if not prompt_path.exists():
        raise FileNotFoundError("MASTER_PROMPT.md 파일을 찾을 수 없습니다.")

    return prompt_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    master_prompt = load_master_prompt()

    print("MASTER_PROMPT.md 불러오기 성공")
    print("=" * 60)
    print(master_prompt[:1000])
    print("=" * 60)
