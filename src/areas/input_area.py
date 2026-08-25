from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QLabel, QProgressBar, QGraphicsOpacityEffect, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt, QEvent

class InputArea(QFrame): 
    # 메시지가 전송 신호
    clicked_send = pyqtSignal(str) 

    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: #EAEFEF;")
        self.setFixedHeight(180)

        # 전체 수직 레이아웃
        main_vbox = QVBoxLayout()
        main_vbox.setContentsMargins(40, 0, 40, 60) 
        main_vbox.setSpacing(0)

        # 상태 메시지 영역
        self.loading_container = QFrame()
        loading_layout = QHBoxLayout(self.loading_container)
        loading_layout.setContentsMargins(0, 0, 0, 0)
        loading_layout.setSpacing(10)

        loading_layout.addStretch()

        self.loading_label = QLabel("AI가 답변을 생성 중입니다...")
        self.loading_label.setStyleSheet("color: #4A4A4A; font-size: 12px; font-weight: bold;")
        
        # 로딩바 설정
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8) 
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setRange(0, 0) 
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar { border: 1px solid #CCCCCC; border-radius: 4px; background-color: white; }
            QProgressBar::chunk { background-color: #4A4A4A; }
        """)

        loading_layout.addWidget(self.loading_label)
        loading_layout.addWidget(self.progress_bar)
        loading_layout.addStretch()
        
        # 투명도 설정
        self.opacity_effect = QGraphicsOpacityEffect(self.loading_container)
        self.loading_container.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0) 

        # 가로 레이아웃 생성 (입력창 + 버튼)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10) 
        
        # 인풋 박스
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("여기에 질문을 입력하세요")
        self.text_input.setFixedHeight(80)
        self.text_input.setStyleSheet("background-color: white; border: 2px solid #BFC9D1; border-radius: 10px; padding: 10px; font-size: 14px;")

        self.text_input.installEventFilter(self)

        # 전송 버튼
        self.send_button = QPushButton("전송")
        self.send_button.setFixedSize(80, 60)
        self.send_button.setStyleSheet("background-color: #6A8C6A; color: white; border-radius: 10px; font-weight: bold; font-size: 14px;")
        
        # 버튼 클릭 시 내부 함수 연결
        self.send_button.clicked.connect(self.on_click_send)
        
        layout.addWidget(self.text_input)
        layout.addWidget(self.send_button)

        main_vbox.addWidget(self.loading_container)
        main_vbox.addLayout(layout)
        self.setLayout(main_vbox)

    def eventFilter(self, obj, event):
        if obj is self.text_input and event.type() == QEvent.Type.KeyPress:
            # 눌린 키가 엔터(Enter/Return)키라면
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    return False 
                else:
                    self.on_click_send()
                    return True
        return super().eventFilter(obj, event)
    
    # 버튼 누르면 텍스트 외부로 전달하는 로직
    def on_click_send(self):
        text = self.text_input.toPlainText().strip()
        if text:
            self.clicked_send.emit(text) 
            self.text_input.clear()

    # 투명도 변경 로직
    def set_loading(self, is_loading):
        if is_loading:
            self.opacity_effect.setOpacity(1.0) 
            self.send_button.setEnabled(False)
            self.text_input.setEnabled(False)
        else:
            self.opacity_effect.setOpacity(0.0) 
            self.send_button.setEnabled(True)
            self.text_input.setEnabled(True)
            self.text_input.clear()