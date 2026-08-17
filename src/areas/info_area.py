from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QFrame, QLabel
from PyQt6.QtCore import Qt

class InfoArea(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: #EAEFEF;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # 상단 제목
        title_label = QLabel("유용한 법률 정보 사이트")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")
        main_layout.addWidget(title_label)

        # 스크롤 영역 생성
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea { background-color: transparent; }
            QScrollBar:vertical {
                border: none; background-color: transparent; width: 12px; margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0; min-height: 40px; border-radius: 6px; margin: 2px;
            }
            QScrollBar::handle:vertical:hover { background-color: #999999; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)

        # 스크롤 안에 들어갈 내용물 위젯
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        
        self.card_layout = QGridLayout(self.content_widget)
        self.card_layout.setContentsMargins(0, 0, 15, 0) # 우측 스크롤 여백
        self.card_layout.setSpacing(20)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)

        # 보여줄 사이트 데이터
        websites = [
            {
                "title": "국가법령정보센터",
                "url": "https://www.law.go.kr",
                "desc": "대한민국 법률의 표준이 되는 공식 법전 사이트입니다. 민법, 민사소송법 등 법 조문과 판례를 정확하게 검색할 수 있으며, 어려운 법률 용어 풀이도 제공합니다."
            },
            {
                "title": "찾기쉬운 생활법령정보",
                "url": "https://www.easylaw.go.kr",
                "desc": "법제처에서 운영하며, 임대차, 임금, 금전 문제 등 일상에서 겪는 법률 문제를 카테고리별로 알기 쉽게 정리해 둔 사이트입니다. 법을 잘 모르는 분들께 추천합니다."
            },
            {
                "title": "대한민국 법원 전자소송",
                "url": "https://ecourt.sc.court.go.kr",
                "desc": "혼자서 소장을 접수하고 재판을 진행할 수 있는 공식 사법 포털입니다. 소장, 답변서 등 '나홀로 소송'에 필요한 각종 법적 서식을 무료로 다운로드할 수 있습니다."
            },
            {
                "title": "대한법률구조공단",
                "url": "https://www.klac.or.kr",
                "desc": "국가에서 운영하는 법률구조 기관입니다. 무료 법률 상담을 예약하거나, 다른 사람들의 방대한 법률 상담 사례를 찾아보며 대응 방법을 참고할 수 있습니다."
            }
        ]

        # 데이터 개수만큼 카드 생성
        for index, site in enumerate(websites):
            row = index // 2
            col = index % 2
            self.create_info_card(site["title"], site["url"], site["desc"], row, col)

    def create_info_card(self, title, url, desc, row, col):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        # 사이트 제목
        title_label = QLabel(f'<a href="{url}" style="color: #2C5F2D; text-decoration: none;">{title} 🔗</a>')
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; border: none; background: transparent;")
        
        # 링크 클릭 시 기본 웹 브라우저 열리도록 설정
        title_label.setOpenExternalLinks(True) 
        title_label.setCursor(Qt.CursorShape.PointingHandCursor)

        # 설명 내용
        desc_label = QLabel(desc)
        desc_label.setStyleSheet("font-size: 14px; color: #555555; border: none; background: transparent; line-height: 140%;")
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch() 
        
        # 2x2 그리드에 카드 추가
        self.card_layout.addWidget(card, row, col)