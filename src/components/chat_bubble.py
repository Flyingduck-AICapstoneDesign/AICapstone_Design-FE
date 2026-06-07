from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt

class ChatBubble(QWidget):
    def __init__(self, text, is_user=True):
        super().__init__()
        
        # 전체 가로 레이아웃
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15) # 프로필-말풍선 간격
        
        # 프로필
        self.profile = QLabel()
        self.profile.setFixedSize(60, 60)
        self.profile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 말풍선
        self.bubble_frame = QFrame()
        self.bubble_frame.setMaximumWidth(500)
        self.bubble_frame.setMinimumHeight(40)
        self.bubble_frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        # 말풍선 안의 텍스트 레이아웃
        bubble_layout = QVBoxLayout(self.bubble_frame)
        bubble_layout.setContentsMargins(25, 15, 25, 15) 
        bubble_layout.setSpacing(0)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True) # 긴 문장 자동 줄바꿈
        self.label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.label.setStyleSheet("background: transparent; border: none; padding: 0px; font-size: 14px;")
        bubble_layout.addWidget(self.label)
        
        # 타입에 따른 스타일 설정
        if is_user:
            # 사용자
            self.profile.setStyleSheet("""
                image: url('src/assets/user.png');
                padding: 10px;
                background-color: #E0E0E0;
                border-radius: 30px; 
                border: 2px solid #25343F;
            """)
            
            self.bubble_frame.setStyleSheet("background-color: #BFC9D1; border-radius: 10px;")
            
            # 배치
            main_layout.addStretch()
            main_layout.addWidget(self.bubble_frame)
            main_layout.addWidget(self.profile, alignment=Qt.AlignmentFlag.AlignTop)
            
        else:
            # 챗봇
            self.profile.setStyleSheet("""
                image: url('src/assets/chat-ai.png');
                padding: 10px;
                background-color: #E0E0E0; 
                border-radius: 30px; 
                border: 2px solid #25343F;
            """)
            
            self.bubble_frame.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
            
            # 배치
            main_layout.addWidget(self.profile, alignment=Qt.AlignmentFlag.AlignTop)
            main_layout.addWidget(self.bubble_frame)
            main_layout.addStretch()