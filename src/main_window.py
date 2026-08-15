import time
# [추가] QSize, Qt 등 누락된 기능 추가
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel
from PyQt6.QtCore import QSize, Qt 

# areas 불러오기
from areas.input_area import InputArea
from areas.chat_area import ChatArea
from areas.header_area import HeaderArea 

# 분리해둔 통신 워커들 불러오기
from workers.api_workers import HistoryWorker, HistoryListWorker, AIWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AI 캡스톤 디자인 - 민사 소송 AI 상담")
        self.setMinimumSize(QSize(1080, 720))
        
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
        self.history_page = QWidget()
        self.history_page.setStyleSheet("background-color: #EAEFEF;")
        history_layout = QVBoxLayout(self.history_page)
        history_label = QLabel("여기는 과거 기록 페이지입니다.")
        history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        history_layout.addWidget(history_label)

        # 추가 정보 화면 임시 세팅
        self.info_page = QWidget()
        self.info_page.setStyleSheet("background-color: #EAEFEF;")
        info_layout = QVBoxLayout(self.info_page)
        info_label = QLabel("여기는 추가 정보 페이지입니다.")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(info_label)

        # 페이지를 스케치북에 적용
        self.stacked_widget.addWidget(self.chat_page)  
        self.stacked_widget.addWidget(self.history_page) 
        self.stacked_widget.addWidget(self.info_page)  

        # 완성된 스케치북 메인 레이아웃에 적용
        main_layout.addWidget(self.stacked_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.start_time = 0.0
        
        # 네비게이션 버튼 신호 연결
        self.header_widget.go_to_chat.connect(self.handle_go_to_chat)
        self.header_widget.go_to_history.connect(self.handle_go_to_history)
        self.header_widget.go_to_info.connect(self.handle_go_to_info)

    def handle_go_to_chat(self):
        print("메인 채팅 페이지로 이동하며, 대화 내용을 초기화합니다.")
        self.stacked_widget.setCurrentIndex(0)
        self.chat_widget.clear_chat()

    def handle_go_to_history(self):
        print("버튼 클릭됨: 과거 기록 페이지로 이동해야 합니다!")
        self.stacked_widget.setCurrentIndex(1)

    def handle_go_to_info(self):
        print("버튼 클릭됨: 추가 정보 페이지로 이동해야 합니다!")
        self.stacked_widget.setCurrentIndex(2)

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