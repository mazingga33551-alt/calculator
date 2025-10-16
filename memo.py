import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, messagebox

class NotepadApp:
    """
    간단한 파일 기능을 갖춘 메모장 애플리케이션 클래스
    """
    def __init__(self, root):
        """
        애플리케이션 초기화
        """
        self.root = root
        self.root.geometry("800x600")

        # 텍스트 영역 생성 (스크롤 기능 포함)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill='both')
        
        # 메뉴바 생성
        self.create_menu()

        # 현재 열려있는 파일 경로
        self.current_file = None
        # 제목 없음 상태로 시작
        self.update_title()

        # 창을 닫을 때 저장 여부 확인
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_menu(self):
        """
        메뉴바와 하위 메뉴들을 생성합니다.
        """
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # 파일 메뉴
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="파일(F)", menu=file_menu)
        file_menu.add_command(label="새로 만들기(N)", command=self.new_file)
        file_menu.add_command(label="열기(O)...", command=self.open_file)
        file_menu.add_command(label="저장(S)", command=self.save_file)
        file_menu.add_command(label="다른 이름으로 저장(A)...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="끝내기(X)", command=self.exit_app)

    def new_file(self):
        """
        새 파일을 생성합니다. 변경 사항이 있으면 저장 여부를 묻습니다.
        """
        if self.check_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.update_title()

    def open_file(self):
        """
        파일 열기 대화상자를 통해 파일을 엽니다.
        """
        if not self.check_unsaved_changes():
            return

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.INSERT, file.read())
                self.current_file = file_path
                self.update_title()
            except Exception as e:
                messagebox.showerror("오류", f"파일을 여는 중 오류가 발생했습니다: {e}")

    def save_file(self):
        """
        현재 파일을 저장합니다. 새 파일이면 다른 이름으로 저장합니다.
        """
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                self.update_title() # 저장 후 제목 업데이트
            except Exception as e:
                messagebox.showerror("오류", f"파일을 저장하는 중 오류가 발생했습니다: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """
        다른 이름으로 저장 대화상자를 통해 파일을 저장합니다.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            self.save_file()

    def exit_app(self):
        """
        애플리케이션을 종료합니다. 변경 사항이 있으면 저장 여부를 묻습니다.
        """
        if self.check_unsaved_changes():
            self.root.destroy()

    def check_unsaved_changes(self):
        """
        저장되지 않은 변경 사항이 있는지 확인하고 사용자에게 저장할지 묻습니다.
        사용자가 '취소'를 누르면 False를, 그 외에는 True를 반환합니다.
        """
        content = self.text_area.get(1.0, tk.END).strip()
        if not content: # 내용이 없으면 그냥 진행
            return True

        # 파일이 열려있을 때, 파일 내용과 현재 내용이 다른지 확인
        is_modified = True
        if self.current_file:
            try:
                with open(self.current_file, "r", encoding="utf-8") as f:
                    if f.read() == self.text_area.get(1.0, tk.END):
                        is_modified = False
            except FileNotFoundError:
                pass # 파일이 아직 디스크에 없으면 수정된 것으로 간주
            except Exception as e:
                messagebox.showwarning("경고", f"파일 확인 중 오류: {e}")


        if is_modified:
            response = messagebox.askyesnocancel("메모장", f"변경 내용을 {self.current_file or '제목 없음'}에 저장하시겠습니까?")
            if response is True:  # '예'
                self.save_file()
                return True
            elif response is False:  # '아니요'
                return True
            else:  # '취소' (None)
                return False
        return True

    def update_title(self):
        """창 제목을 현재 파일 상태에 맞게 업데이트합니다."""
        title = "제목 없음"
        if self.current_file:
            # os.path.basename을 사용하면 전체 경로 대신 파일 이름만 가져올 수 있습니다.
            import os
            title = os.path.basename(self.current_file)
        
        self.root.title(f"{title} - 메모장")


if __name__ == "__main__":
    main_window = tk.Tk()
    app = NotepadApp(main_window)
    main_window.mainloop()
