from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

class HeaderArea(QFrame):
    go_to_chat = pyqtSignal()
    go_to_history = pyqtSignal()
    go_to_info = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # 헤더 배경색과 글자색, 높이 고정
        self.setStyleSheet("background-color: #525F6C; color: white;")
        self.setFixedHeight(80)

        # 가로 레이아웃
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 20)

        # 메인 타이틀
        title_label = QLabel("민사 소송 AI 상담봇")
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        # 새 채팅 메뉴
        self.nav_chat = QPushButton("새 채팅")
        self.nav_chat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nav_chat.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: white; 
                font-weight: bold; 
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                color: #BFC9D1; 
            }
        """)
        self.nav_chat.clicked.connect(self.go_to_chat.emit)
        
        # 과거 기록 메뉴
        self.nav_history = QPushButton("과거 기록")
        self.nav_history.setCursor(Qt.CursorShape.PointingHandCursor)  
        self.nav_history.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: white; 
                font-weight: bold; 
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                color: #BFC9D1; 
            }
        """)
        self.nav_history.clicked.connect(self.go_to_history.emit)

        # 추가 정보 메뉴
        self.nav_info = QPushButton("추가 정보")
        self.nav_info.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nav_info.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: white; 
                font-weight: bold; 
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                color: #BFC9D1;
            }
        """)
        self.nav_info.clicked.connect(self.go_to_info.emit)

        # 레이아웃 조립
        layout.addWidget(title_label)
        layout.addStretch() 
        
        layout.addWidget(self.nav_chat)  
        layout.addSpacing(30)
        
        layout.addWidget(self.nav_history)
        layout.addSpacing(30) 
        
        layout.addWidget(self.nav_info)