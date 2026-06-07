import requests
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import QSize, QThread, pyqtSignal

# areas 불러오기
from areas.input_area import InputArea
from areas.chat_area import ChatArea
from areas.history_area import HistoryArea

# API 통신 담당
class AIWorker(QThread):
    # AI 응답이 완료되면 UI(메인창)로 텍스트를 전달할 신호
    answer_received = pyqtSignal(str)

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            # 1. AI 서버의 API 주소
            url = "http://220.69.241.162:8000" 
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # 질문
            data = {
                "question": self.user_text
            }
            
            # AI로 전송
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            # 서버 응답 확인
            if response.status_code == 200:
                result = response.json()
                
                # 답변
                ai_answer = result.get("answer", "서버 응답 데이터 구조가 다릅니다.")
            else:
                ai_answer = f"서버 오류가 발생했습니다. (코드: {response.status_code})"
                
        except requests.exceptions.Timeout:
            ai_answer = "서버 응답 시간이 초과되었습니다. (Timeout)"
        except Exception as e:
            ai_answer = f"서버 연결 실패: 인공지능 서버가 켜져 있는지 확인하세요.\n({str(e)})"
        
        # 완료된 답변을 메인 UI 창으로 던져줍니다.
        self.answer_received.emit(ai_answer)

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
        if not text.strip(): # 빈 메시지 방지
            return
        
        print(f"전송된 질문: {text}")
        
        # 질문 대화창에 띄우기
        self.chat_widget.add_message(text, is_user=True)
        
        # 로딩 상태 시작
        self.input_widget.set_loading(True)
        
        self.ai_worker = AIWorker(text)
        # AI가 응답을 완료하면 finish_loading 함수가 호출되도록 연결
        self.ai_worker.answer_received.connect(self.finish_loading)

        self.ai_worker.start()

    def finish_loading(self, ai_answer):
        # 로딩 상태 해제
        self.input_widget.set_loading(False)
        print("AI 응답이 완료되었습니다.")

        # AI 답변 대화창에 띄우기
        self.chat_widget.add_message(ai_answer, is_user=False)