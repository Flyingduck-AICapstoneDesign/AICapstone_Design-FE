# areas/header_area.py
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

class HeaderArea(QFrame):
    # 각 네비게이션 버튼을 눌렀을 때 메인 창으로 보낼 신호들
    go_to_history = pyqtSignal()
    go_to_info = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # 헤더 배경색과 글자색, 높이 고정
        self.setStyleSheet("background-color: #525F6C; color: white;")
        self.setFixedHeight(80)

        # 가로 레이아웃 (기존 여백 유지)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 20)

        # 왼쪽: 메인 타이틀
        title_label = QLabel("민사 소송 AI 상담봇")
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        # 오른쪽: 네비게이션 메뉴들 생성 (QPushButton 활용)
        
        # 1. 과거 기록 메뉴
        self.nav_history = QPushButton("과거 기록")
        self.nav_history.setCursor(Qt.CursorShape.PointingHandCursor) # 마우스 올리면 손가락 모양 
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

        # 2. 추가 정보 메뉴
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

        # 레이아웃 조립 (제목 -> 빈 공간 쫙 밀기 -> 과거 기록 -> 간격 -> 추가 정보)
        layout.addWidget(title_label)
        layout.addStretch() # 가운데 공간을 띄워주는 역할
        layout.addWidget(self.nav_history)
        layout.addSpacing(30) # 메뉴 사이의 간격
        layout.addWidget(self.nav_info)