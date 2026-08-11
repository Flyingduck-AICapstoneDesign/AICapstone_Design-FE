import os 
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import QSize, QThread, pyqtSignal
import time 

load_dotenv()

# areas 불러오기
from areas.input_area import InputArea
from areas.chat_area import ChatArea
from areas.history_area import HistoryArea

# [역할 1] 특정 대화방의 채팅 '내용'을 불러오는 통신 담당
class HistoryWorker(QThread):
    history_received = pyqtSignal(list)

    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id

    def run(self):
        try:
            base_url = os.getenv("BE_API_URL", "http://127.0.0.1:8000")
            url = f"{base_url}/api/history/{self.session_id}" 
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                messages = result.get("messages", [])
                self.history_received.emit(messages)
            else:
                self.history_received.emit([])
        except Exception as e:
            print(f"과거 대화 내용 불러오기 실패: {e}")
            self.history_received.emit([])

# [역할 2] 사이드바에 띄울 '전체 방 목록'을 불러오는 통신 담당
class HistoryListWorker(QThread):
    list_received = pyqtSignal(list)

    def run(self):
        try:
            base_url = os.getenv("BE_API_URL", "http://127.0.0.1:8000")
            url = f"{base_url}/api/history" 
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                self.list_received.emit(response.json())
            else:
                self.list_received.emit([])
        except Exception as e:
            print(f"사이드바 목록 불러오기 실패: {e}")
            self.list_received.emit([])

# API 통신 담당 (질문 전송)
class AIWorker(QThread):
    answer_received = pyqtSignal(str)

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            base_url = os.getenv("BE_API_URL", "http://127.0.0.1:8000")
            url = f"{base_url}/chat"
            
            headers = {
                "Content-Type": "application/json", 
                "ngrok-skip-browser-warning": "true"  
            }
            
            data = {
                "session_id": "session_123", 
                "user_id": "test_user",      
                "message": self.user_text    
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=300)
            
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AI 캡스톤 디자인 - 민사 소송 AI 상담")
        self.setMinimumSize(QSize(1080, 720))
        
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 
        
        self.sidebar_widget = HistoryArea()

        right_widget = QWidget()
        right_layout = QVBoxLayout() 
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_widget.setStyleSheet("background-color: #EAEFEF;")
        right_layout.setSpacing(0)

        self.chat_widget = ChatArea()
        self.input_widget = InputArea()
        
        self.input_widget.clicked_send.connect(self.handle_send_question)

        right_layout.addWidget(self.chat_widget)
        right_layout.addWidget(self.input_widget)
        right_widget.setLayout(right_layout)

        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(right_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self.start_time = 0.0  # 들여쓰기 오류 수정됨

        # 기존에 있던 채팅 내용 불러오기
        self.load_history("session_123") 
        
        # 앱이 켜질 때 사이드바 목록도 불러오기 실행
        self.load_history_list()

    # 사이드바 목록 불러오기 로직
    def load_history_list(self):
        self.list_worker = HistoryListWorker()
        self.list_worker.list_received.connect(self.display_history_list)
        self.list_worker.start()

    # 사이드바에 제목들 그려주기
    def display_history_list(self, sessions):
        if not sessions:
            print("사이드바에 띄울 목록이 없습니다.")
            return
            
        for session in sessions:
            title = session.get("title", "제목 없음")
            self.sidebar_widget.add_history(title)

    # 특정 채팅 내용 불러오기 로직
    def load_history(self, session_id):
        self.history_worker = HistoryWorker(session_id)
        self.history_worker.history_received.connect(self.display_history)
        self.history_worker.start()

    # 불러온 내용을 화면에 그리는 로직
    def display_history(self, messages):
        if not messages:
            print("불러올 과거 대화 기록이 없습니다.")
            return
            
        print(f"과거 대화 내용 {len(messages)}개를 불러왔습니다.")
        
        for msg in messages:
            sender = msg.get("sender", "")
            text = msg.get("text", "")
            
            is_user = (sender != "AI") 
            self.chat_widget.add_message(text, is_user)

    # 질문 전송 컨트롤 로직
    def handle_send_question(self, text):
        if not text.strip(): 
            return
        
        print(f"전송된 질문: {text}")
        self.start_time = time.time()
        
        self.chat_widget.add_message(text, is_user=True)
        self.input_widget.set_loading(True)
        
        self.ai_worker = AIWorker(text)
        self.ai_worker.answer_received.connect(self.finish_loading)
        self.ai_worker.start()

    def finish_loading(self, ai_answer):
        elapsed_time = time.time() - self.start_time

        self.input_widget.set_loading(False)
        print("AI 응답이 완료되었습니다.")
        print(f"--> [소요 시간]: {elapsed_time:.2f}초")

        self.chat_widget.add_message(ai_answer, is_user=False)