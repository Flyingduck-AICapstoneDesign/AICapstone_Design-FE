import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    # PyQt 어플리케이션 객체 생성
    app = QApplication(sys.argv)
    
    # 메인 화면 컴포넌트 생성 및 표시
    window = MainWindow()
    window.show()
    
    # 이벤트 루프 실행
    sys.exit(app.exec())

if __name__ == "__main__":
    main()