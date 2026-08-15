import time
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QSize

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
        
        self.header_widget = HeaderArea()

        self.chat_widget = ChatArea()
        self.input_widget = InputArea()
        
        self.input_widget.clicked_send.connect(self.handle_send_question)

        main_layout.addWidget(self.header_widget)
        main_layout.addWidget(self.chat_widget)
        main_layout.addWidget(self.input_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.start_time = 0.0
        
        # 네비게이션 버튼 신호 연결
        self.header_widget.go_to_history.connect(self.handle_go_to_history)
        self.header_widget.go_to_info.connect(self.handle_go_to_info)

    def handle_go_to_history(self):
        print("버튼 클릭됨: 과거 기록 페이지로 이동해야 합니다!")
        # 나중에 여기에 페이지를 전환하는 코드 입력

    def handle_go_to_info(self):
        print("버튼 클릭됨: 추가 정보 페이지로 이동해야 합니다!")
        # 나중에 여기에 페이지를 전환하는 코드 입력

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