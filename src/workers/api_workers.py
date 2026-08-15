import os 
import requests
from dotenv import load_dotenv
from PyQt6.QtCore import QThread, pyqtSignal

load_dotenv()

# 공통 헤더
HEADERS = {
    "Content-Type": "application/json", 
    "ngrok-skip-browser-warning": "true"
}

# 특정 대화방의 채팅 내용을 불러오는 통신 담당
class HistoryWorker(QThread):
    history_received = pyqtSignal(list)

    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id

    def run(self):
        try:
            base_url = os.getenv("BE_API_URL", "http://127.0.0.1:8000")
            url = f"{base_url}/api/history/{self.session_id}" 
            
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                messages = result.get("messages", [])
                self.history_received.emit(messages)
            else:
                self.history_received.emit([])
        except Exception as e:
            print(f"과거 대화 내용 불러오기 실패: {e}")
            self.history_received.emit([])

# 헤더/페이지에 띄울 전체 방 목록을 불러오는 통신 담당
class HistoryListWorker(QThread):
    list_received = pyqtSignal(list)

    def run(self):
        try:
            base_url = os.getenv("BE_API_URL", "http://127.0.0.1:8000")
            url = f"{base_url}/api/history" 
            
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                self.list_received.emit(response.json())
            else:
                self.list_received.emit([])
        except Exception as e:
            print(f"과거 기록 목록 불러오기 실패: {e}")
            self.list_received.emit([])

# API 통신 담당 (질문 전송)
class AIWorker(QThread):
    answer_received = pyqtSignal(str)

    # session_id를 기본값과 함께 넘겨받도록 수정
    def __init__(self, user_text, session_id="session_123"):
        super().__init__()
        self.user_text = user_text
        self.session_id = session_id

    def run(self):
        try:
            base_url = os.getenv("BE_API_URL", "http://127.0.0.1:8000")
            url = f"{base_url}/chat"
            
            data = {
                "session_id": self.session_id, 
                "user_id": "test_user",      
                "message": self.user_text    
            }
            
            response = requests.post(url, headers=HEADERS, json=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                ai_answer = result.get("answer", "서버 응답 데이터 구조가 다릅니다.")
            else:
                ai_answer = f"서버 오류가 발생했습니다. (코드: {response.status_code})"
                
        except requests.exceptions.Timeout:
            ai_answer = "서버 응답 시간이 초과되었습니다. (Timeout)"
        except Exception as e:
            ai_answer = f"서버 연결 실패: 인공지능 서버가 켜져 있는지 확인하세요.\n({str(e)})"
        
        self.answer_received.emit(ai_answer)