import tkinter as tk

def create_basic_window():
    """
    "메모장" 제목과 중앙에 라벨이 있는 기본 창을 생성하고 실행합니다.
    """
    # 1. 메인 윈도우를 생성합니다.
    root = tk.Tk()

    # 2. 창의 제목을 "메모장"으로 설정합니다.
    root.title("메모장")

    # 3. 창의 초기 크기를 설정합니다.
    root.geometry("600x400")

    # 4. 창 가운데에 표시될 라벨(텍스트) 위젯을 생성합니다.
    label = tk.Label(root, text="메모장을 만들어봐요", font=("Malgun Gothic", 16))

    # 5. 라벨을 화면 중앙에 배치합니다. (expand=True가 중앙 정렬의 핵심입니다.)
    label.pack(expand=True)

    # 6. 윈도우가 닫히기 전까지 계속 실행되도록 합니다.
    root.mainloop()

# 이 스크립트 파일이 직접 실행될 때 create_basic_window 함수를 호출합니다.
if __name__ == "__main__":
    create_basic_window()
