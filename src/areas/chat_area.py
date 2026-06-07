from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from components.chat_bubble import ChatBubble

class ChatArea(QWidget):
    def __init__(self):
        super().__init__()
        
        # ChatArea 자체의 레이아웃
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 60, 0, 0)
        
        # 스크롤 영역 생성 및 설정
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) # 내부 위젯 크기 자동 조절
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame) # 테두리 제거
        self.scroll_area.setStyleSheet("background-color: #EAEFEF;") # 배경색 설정
        
        # 스크롤 안에 들어갈 실제 메시지 표시용 위젯
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        
        # 레이아웃 설정
        self.chat_layout = QVBoxLayout(self.content_widget)
        self.chat_layout.setContentsMargins(40, 0, 40, 20) 
        self.chat_layout.setSpacing(40)
        
        # 조립
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
         
        # 레이아웃
        self.chat_layout.addStretch()

        # 테스트용 메시지 추가 
        self.add_message("안녕하세요. 법률 상담 AI 챗봇입니다. 민사 소송과 관련하여 궁금하신 점이 있으신가요? 상황을 말씀해 주시면 절차와 필요한 서류를 안내해 드리겠습니다.", is_user=False)
        self.add_message("친구가 작년에 급하다고 해서 500만 원을 빌려줬는데, 계속 준다고 말만 하고 1년째 안 주고 있어요. 차용증은 따로 안 썼는데 카톡이랑 계좌 이체 내역만 있어도 소송이 가능한가요?", is_user=True)
        self.add_message("네, 차용증이 없더라도 대여금 사실을 증명할 수 있는 다른 객관적 자료가 있다면 소송이 가능합니다. 말씀하신 계좌 이체 내역(돈을 보낸 사실)과 카카오톡 대화 내용(돈을 빌렸다는 인정 및 갚겠다는 약속)은 아주 중요한 증거가 됩니다. 우선 정식 소송 전에 '지급명령' 신청을 고려해 보시는 건 어떨까요?", is_user=False)

    def add_message(self, text, is_user):
        bubble = ChatBubble(text, is_user)
        
        # 정렬 방향 결정
        align = Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft
        
        # 빈 공간이 항상 맨 밑에 있도록 위쪽에 삽입
        # 세 번째 인자로 alignment 전달하여 너비 팽창 방지
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble, alignment=align)