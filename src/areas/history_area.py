from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

# 컴포넌트 불러오기
from components.history_item import HistoryItem 

class HistoryArea(QFrame):
    def __init__(self):
        super().__init__()
        
        # 기록 구역 기본 스타일 및 크기 설정
        self.setStyleSheet("background-color: #525F6C;")
        self.setContentsMargins(20, 60, 20, 60)
        self.setFixedWidth(250) # 너비 고정
        
        # 레이아웃 생성
        self.history_layout = QVBoxLayout(self)
        
        # 제목 라벨
        title_label = QLabel("쉽게 알아보는\n소송 걸기")
        title_label.setStyleSheet("color: #FAF9F6; font-weight: bold; font-size: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.history_layout.addWidget(title_label)
        
        self.history_layout.addSpacing(60)

        # 서브 제목 라벨
        subtitle_label = QLabel("과거 대화 기록")
        subtitle_label.setStyleSheet("color: #EAEFEF; font-weight: bold; font-size: 13px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.history_layout.addWidget(subtitle_label)

        self.history_layout.addSpacing(10)
        
        # 아래쪽을 밀어주는 빈 공간 추가 
        self.history_layout.addStretch()

        # 확인용 테스트 데이터
        self.add_history("전세금 반환 소송 절차")
        self.add_history("근로계약서 미작성 신고")
        self.add_history("빌려준 돈을 받지 못할 때")

    def add_history(self, title):
        """
        새로운 과거 기록 컴포넌트를 사이드바에 추가하는 함수
        """
        # 낱개 컴포넌트 생성
        item = HistoryItem(title)
        
        # 빈 공간이 항상 맨 밑에 유지되도록, 전체 개수에서 -1 한 위치에 삽입
        self.history_layout.insertWidget(self.history_layout.count() - 1, item)