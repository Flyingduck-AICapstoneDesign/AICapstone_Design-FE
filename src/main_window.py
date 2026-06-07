from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import QSize, Qt, QTimer

# areas 불러오기
from areas.input_area import InputArea
from areas.chat_area import ChatArea
from areas.history_area import HistoryArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AI 캡스톤 디자인 - 민사 소송 AI 상담")
        self.setMinimumSize(QSize(1080, 720))
        
        # 가장 밑바탕 레이아웃 flex-row
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0) # margin 제거
        main_layout.setSpacing(0) # gap 제거
        
        # 왼쪽 사이드바 (과거 기록)
        self.sidebar_widget = HistoryArea()

        # 오른쪽 전체 영역
        right_widget = QWidget()
        right_layout = QVBoxLayout() # flex-col
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_widget.setStyleSheet("background-color: #EAEFEF;")
        right_layout.setSpacing(0)

        # 대화창 영역
        self.chat_widget = ChatArea()

        # 입력창 영역
        self.input_widget = InputArea()
        
        # --- 신호 연결 ---
        # InputArea의 'clicked_send' 신호 'handle_send_question'에 연결
        self.input_widget.clicked_send.connect(self.handle_send_question)

        # 조립
        # 오른쪽 영역
        right_layout.addWidget(self.chat_widget)
        right_layout.addWidget(self.input_widget)
        right_widget.setLayout(right_layout)

        # 메인 영역
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(right_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # 질문 전송 컨트롤 로직
    def handle_send_question(self, text):
        """
        사용자가 입력한 텍스트를 처리하고 AI 응답을 기다리는 함수
        """
        print(f"전송된 질문: {text}")
        
        # 로딩 상태 시작
        self.input_widget.set_loading(True)
        
        # AI 응답 대기
        # 테스트를 위해 3초 뒤에 로딩을 해제하도록 타이머 설정
        QTimer.singleShot(3000, self.finish_loading)

    def finish_loading(self):
        # 로딩 상태 해제
        self.input_widget.set_loading(False)
        print("AI 응답이 완료되었습니다.")