from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class HistoryCard(QFrame):
    session_clicked = pyqtSignal(str)

    def __init__(self, session_id, title, date):
        super().__init__()
        self.session_id = session_id

        self.setStyleSheet("""
            HistoryCard {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 10px;
            }
            HistoryCard:hover {
                border: 2px solid #6A8C6A;
                background-color: #F8F9F9;
            }
        """)
        self.setFixedHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; border: none; background: transparent; color: #333333;")
        
        date_label = QLabel(f"상담 일자: {date}")
        date_label.setStyleSheet("font-size: 12px; color: #888888; border: none; background: transparent;")

        layout.addWidget(title_label)
        layout.addWidget(date_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.session_clicked.emit(self.session_id)
        super().mousePressEvent(event)