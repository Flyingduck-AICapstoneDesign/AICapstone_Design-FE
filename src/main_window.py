import time
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import QSize

# areas 불러오기
from areas.input_area import InputArea
from areas.chat_area import ChatArea
from areas.history_area import HistoryArea

# 분리해둔 통신 워커들 불러오기
from workers.api_workers import HistoryWorker, HistoryListWorker, AIWorker

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

        # 신호 연결
        self.sidebar_widget.session_selected.connect(self.handle_session_click)
        
        self.start_time = 0.0

        # 앱이 켜질 때 사이드바 목록도 불러오기 실행
        self.load_history_list()

    def handle_session_click(self, session_id):
        print(f"[{session_id}] 대화 기록을 불러옵니다...")
        self.chat_widget.clear_chat() # 1. 기존 화면을 싹 비운다.
        self.load_history(session_id)

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
            session_id = session.get("session_id", "")
            title = session.get("title", "제목 없음")
            self.sidebar_widget.add_history(session_id, title)

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