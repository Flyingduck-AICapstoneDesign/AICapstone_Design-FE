from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from components.chat_bubble import ChatBubble

class ChatArea(QWidget):
    def __init__(self):
        super().__init__()
        
        # ChatArea 자체의 레이아웃
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 스크롤 영역 생성 및 설정
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)   # 내부 위젯 크기 자동 조절
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)    # 테두리 제거
        self.scroll_area.setStyleSheet("background-color: #EAEFEF;")    # 배경색 설정
        
        # 스크롤 안에 들어갈 실제 메시지 표시용 위젯
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        
        # 레이아웃 설정
        self.chat_layout = QVBoxLayout(self.content_widget)
        self.chat_layout.setContentsMargins(40, 20, 40, 20) 
        self.chat_layout.setSpacing(40)
        
        # 조립
        self.scroll_area.setWidget(self.content_widget)
        self.main_layout.addWidget(self.scroll_area)
         
        # 레이아웃
        self.chat_layout.addStretch()

    def add_message(self, text, is_user):
        bubble = ChatBubble(text, is_user)
        
        # 정렬 방향 결정
        align = Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft
        
        # 빈 공간이 항상 맨 밑에 있도록 위쪽에 삽입
        # 세 번째 인자로 alignment 전달하여 너비 팽창 방지
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble, alignment=align)

    def clear_chat(self):
        """
        화면에 있는 모든 채팅 말풍선을 삭제하여 빈 화면으로 만듭니다.
        """
        # 마지막 빈 공간(addStretch)은 남겨두기 위해 1개가 남을 때까지 반복 삭제
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()    # 메모리에서 완전히 제거