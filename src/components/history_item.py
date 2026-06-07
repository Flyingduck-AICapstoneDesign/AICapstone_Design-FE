from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

class HistoryItem(QPushButton):
    def __init__(self, title):
        super().__init__(title)
        
        # 버튼의 기본 크기 및 텍스트 정렬
        self.setMinimumHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor) # 커서 pointer
        
        # Hover 상태 구분
        self.setStyleSheet("""
            QPushButton {
                background-color: #BFC9D1; 
                color: #25343F; 
                border-radius: 4px; 
                padding: 10px;
                text-align: left;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #EAEFEF;
                color: #25343F; 
            }
            QPushButton:pressed {
                background-color: #EAEFEF;
                color: #25343F; 
            }
        """)