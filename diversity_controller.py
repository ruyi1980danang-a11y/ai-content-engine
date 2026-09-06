import os
import gspread
from google.oauth2.service_account import Credentials

def get_google_sheet_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    
    # 로컬 환경(credentials.json) 또는 환경 변수 지원 분기
    if os.path.exists("credentials.json"):
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
    else:
        # GitHub Actions 등 환경 변수 활용 시 대비
        import json
        creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        if creds_json:
            creds_info = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
            client = gspread.authorize(creds)
        else:
            raise ValueError("Google credentials not found in environment or local files.")
    
    return client

def get_next_tone_category(sheet_name="시트1", limit=5):
    """
    구글 시트의 AZ열(Tone_Category)에서 최근 콘텐츠들의 톤 이력을 분석하여,
    에코 체임버를 방지하고 균형 잡힌 톤 순환을 위한 다음 톤을 결정합니다.
    """
    try:
        client = get_google_sheet_client()
        
        # 스프레드시트 및 시트 연결 (기존 '자동화' 스프레드시트 가정)
        # 팡트/시트 명칭 확인 필요 시 수정
        spreadsheet = client.open("자동화")
        worksheet = spreadsheet.worksheet(sheet_name)
        
        # AZ열의 모든 값 가져오기 (AZ는 52번째 열)
        # 또는 col_values(52) 활용
        az_values = worksheet.col_values(52)
        
        # 헤더('Tone_Category') 제외하고 데이터가 있는 행만 필터링
        if len(az_values) > 1:
            history = [val.strip() for val in az_values[1:] if val.strip()]
        else:
            history = []
            
        # 최근 기록 추출 (기본 최근 5개)
        recent_history = history[-limit:] if len(history) >= limit else history
        
        # 순환할 톤 풀 정의 (필요에 따라 확장 가능)
        available_tones = ["Comedy", "Serious", "Info"]
        
        # 최근에 사용된 톤이 있다면, 단순 순환 또는 가중치 기반으로 다음 톤 선정
        if not recent_history:
            return available_tones[0]
            
        last_tone = recent_history[-1]
        
        # 직전 톤과 다른 톤을 우선 선택하도록 순환 로직 적용
        for tone in available_tones:
            if tone != last_tone:
                return tone
                
        return available_tones[0]
        
    except Exception as e:
        print(f"Error in diversity controller: {e}")
        return "Info" # 오류 발생 시 기본값 반환

def save_tone_category(tone, sheet_name="시트1"):
    """
    사용된 톤을 구글 시트 AZ열(Tone_Category)의 다음 빈 행에 기록합니다.
    """
    try:
        client = get_google_sheet_client()
        spreadsheet = client.open("자동화")
        worksheet = spreadsheet.worksheet(sheet_name)
        
        az_values = worksheet.col_values(52)
        next_row = len(az_values) + 1 if len(az_values) > 0 else 1
        
        if next_row == 1:
            worksheet.update_cell(1, 52, "Tone_Category")
            next_row = 2
            
        worksheet.update_cell(next_row, 52, tone)
        
    except Exception as e:
        print(f"Error saving tone category: {e}")

if __name__ == "__main__":
    # 단독 테스트용
    next_tone = get_next_tone_category()
    print(f"Recommended Next Tone: {next_tone}")
