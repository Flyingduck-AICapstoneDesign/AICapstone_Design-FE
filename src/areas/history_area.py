from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

from components.history_card import HistoryCard

class HistoryArea(QWidget):
    # 특정 카드가 클릭되었을 때 메인 창으로 보낼 신호
    session_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: #EAEFEF;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # 상단 제목
        title_label = QLabel("과거 대화 기록")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        main_layout.addWidget(title_label)

        # 스크롤 영역 생성
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # 스크롤바 디자인 변경
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: transparent;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0;
                min-height: 40px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #999999;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # 스크롤 안에 들어갈 도화지 위젯
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        
        # 도화지에 카드들을 쌓아줄 레이아웃
        self.card_layout = QVBoxLayout(self.content_widget)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(15)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # 위에서부터 차곡차곡

        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)

    # 외부에서 목록을 받아 카드를 추가해주는 함수
    def add_history(self, session_id, title, date):
        card = HistoryCard(session_id, title, date)
        # 카드에서 클릭 신호가 오면, 그걸 그대로 메인 창으로 전달
        card.session_clicked.connect(self.session_selected.emit)
        self.card_layout.insertWidget(0, card)

    # 카드를 싹 비우는 함수 (새로고침 용도)
    def clear_history(self):
        while self.card_layout.count() > 0:
            item = self.card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()