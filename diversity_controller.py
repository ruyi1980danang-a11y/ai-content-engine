import os
import gspread
from google.oauth2.service_account import Credentials

def get_recent_tone():
    # 구글 시트 연동 설정
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials_info = os.environ.get("GOOGLE_CREDENTIALS") # GitHub Secrets 연동 대비
    
    # 로컬 테스트 혹은 환경 변수 처리 (필요시 수정)
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) if os.path.exists("credentials.json") else None
    
    # 만약 환경변수 사용 구조라면 연동 코드 추가 가능, 현재는 기본 뼈대만 장착
    return "Comedy" # 기본값 반환 예시
