import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QTextEdit

class BasicWindow(QMainWindow):
    """
    메인 윈도우 창을 생성하는 기본 클래스
    """
    def __init__(self):
        """
        생성자. 부모 클래스의 생성자를 호출하고 UI 초기화를 진행합니다.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        사용자 인터페이스(UI)의 기본 속성을 설정합니다.
        """
        # 윈도우 제목 설정
        self.setWindowTitle('계산기')
        
        # 윈도우 위치와 크기 설정 (x, y, 너비, 높이)
        self.setGeometry(300, 300, 400, 300)

        # 중앙 위젯과 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 텍스트 에디터 생성
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True) # 읽기 전용으로 설정 (선택 사항)

        # 버튼 생성
        button = QPushButton('메시지 보기', self)
        
        # 레이아웃에 버튼 추가
        # 레이아웃에 위젯 추가 (텍스트 에디터, 버튼 순)
        layout.addWidget(self.text_edit)
        layout.addWidget(button)
        
        # 버튼 클릭 시그널을 슬롯(메서드)에 연결
        button.clicked.connect(self.show_message)
        
        # 윈도우를 화면에 표시
        self.show()

    def show_message(self):
        """
        버튼 클릭 시 메시지 박스를 표시하는 슬롯
        버튼 클릭 시 텍스트 에디터에 메시지를 추가하는 슬롯
        """
        QMessageBox.information(self, '알림', 'Button Clicked')
        self.text_edit.append("Btton Clicked")

if __name__ == '__main__':
    # QApplication 인스턴스 생성: GUI 애플리케이션을 관리하는 핵심 객체입니다.
    app = QApplication(sys.argv)
    
    # BasicWindow 클래스의 인스턴스 생성
    window = BasicWindow()
    
    # 이벤트 루프 시작: 프로그램이 종료되지 않고 사용자 입력을 기다리게 합니다.
    # 윈도우가 닫힐 때 종료 코드를 시스템에 반환합니다.
    sys.exit(app.exec())
