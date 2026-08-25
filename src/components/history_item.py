from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

class HistoryItem(QPushButton):
    # 클릭 시 자신의 session_id를 바깥으로 방출하는 커스텀 신호
    session_clicked = pyqtSignal(str) 

    def __init__(self, session_id, title):
        super().__init__(title)
        
        # 고유 ID 저장
        self.session_id = session_id 
        
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

        # 버튼이 클릭되면 자체 함수를 실행하도록 연결
        self.clicked.connect(self.emit_session)

    # 저장해둔 session_id를 바깥으로 던져주는 함수
    def emit_session(self):
        self.session_clicked.emit(self.session_id)