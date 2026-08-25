import time
import uuid
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel
from PyQt6.QtCore import QSize, Qt 

# areas 불러오기
from areas.input_area import InputArea
from areas.chat_area import ChatArea
from areas.header_area import HeaderArea
from areas.history_area import HistoryArea 
from areas.info_area import InfoArea

# 분리해둔 통신 워커들 불러오기
from workers.api_workers import HistoryWorker, HistoryListWorker, AIWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AI 캡스톤 디자인 - 민사 소송 AI 상담")
        self.setMinimumSize(QSize(1080, 720))
        
        # 현재 채팅방의 고유 세션 ID 생성
        self.current_session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0) 

        # 헤더 구역 고정
        self.header_widget = HeaderArea()
        main_layout.addWidget(self.header_widget)

        # 스케치북 생성
        self.stacked_widget = QStackedWidget()

        # 메인 채팅 화면 세팅
        self.chat_page = QWidget()
        chat_layout = QVBoxLayout(self.chat_page)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)

        self.chat_widget = ChatArea()
        self.input_widget = InputArea()
        
        self.input_widget.clicked_send.connect(self.handle_send_question)

        chat_layout.addWidget(self.chat_widget)
        chat_layout.addWidget(self.input_widget)

        # 과거 기록 화면 임시 세팅
        self.history_page = HistoryArea()
        self.history_page.session_selected.connect(self.handle_session_click)

        # 추가 정보 화면 임시 세팅
        self.info_page = InfoArea()

        # 페이지를 스케치북에 적용
        self.stacked_widget.addWidget(self.chat_page)  
        self.stacked_widget.addWidget(self.history_page) 
        self.stacked_widget.addWidget(self.info_page)  

        # 완성된 스케치북 메인 레이아웃에 적용
        main_layout.addWidget(self.stacked_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.start_time = 0.0

        self.load_history_list()
        
        # 네비게이션 버튼 신호 연결
        self.header_widget.go_to_chat.connect(self.handle_go_to_chat)
        self.header_widget.go_to_history.connect(self.handle_go_to_history)
        self.header_widget.go_to_info.connect(self.handle_go_to_info)

    def handle_go_to_chat(self):
        print("메인 채팅 페이지로 이동하며, 대화 내용을 초기화합니다.")
        # 새 세션 ID 부여 및 화면 리셋
        self.current_session_id = f"session_{uuid.uuid4().hex[:8]}"
        self.stacked_widget.setCurrentIndex(0)
        self.chat_widget.clear_chat()

    def handle_go_to_history(self):
        print("버튼 클릭됨: 과거 기록 페이지로 이동해야 합니다!")
        self.load_history_list()
        self.stacked_widget.setCurrentIndex(1)

    def handle_go_to_info(self):
        print("버튼 클릭됨: 추가 정보 페이지로 이동해야 합니다!")
        self.stacked_widget.setCurrentIndex(2)

    # 과거 기록 카드 클릭 시 실행되는 로직
    def handle_session_click(self, session_id):
        print(f"[{session_id}] 대화 기록을 불러옵니다...")
        self.current_session_id = session_id
        self.stacked_widget.setCurrentIndex(0) 
        self.chat_widget.clear_chat()   
        self.load_history(session_id)  

    # 과거 기록 전체 목록 요청 로직
    def load_history_list(self):
        self.list_worker = HistoryListWorker()
        self.list_worker.list_received.connect(self.display_history_list)
        self.list_worker.start()

    # 받아온 목록을 HistoryArea에 그려주는 로직
    def display_history_list(self, sessions):
        self.history_page.clear_history()
        if not sessions:
            print("불러올 과거 기록 목록이 없습니다.")
            return
            
        for session in sessions:
            session_id = session.get("session_id", "")
            title = session.get("title", "제목 없음")
            date = session.get("date", "날짜 없음")
            
            self.history_page.add_history(session_id, title, date)

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
        
        # 현재 활성화된 세션 ID를 넘겨서 질문 전송
        self.ai_worker = AIWorker(text, self.current_session_id)
        self.ai_worker.answer_received.connect(self.finish_loading)
        self.ai_worker.start()

    def finish_loading(self, ai_answer):
        elapsed_time = time.time() - self.start_time

        self.input_widget.set_loading(False)
        print("AI 응답이 완료되었습니다.")
        print(f"--> [소요 시간]: {elapsed_time:.2f}초")

        self.chat_widget.add_message(ai_answer, is_user=False)