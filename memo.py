import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, messagebox
import os

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

        # 텍스트 영역 생성 (스크롤 기능 포함, undo/redo 활성화)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True, maxundo=-1)
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
        menu_bar.add_cascade(label="파일(F)", menu=file_menu, underline=3)
        file_menu.add_command(label="새로 만들기(N)", command=self.new_file, accelerator="Ctrl+N", underline=7)
        file_menu.add_command(label="열기(O)...", command=self.open_file, accelerator="Ctrl+O", underline=4)
        file_menu.add_command(label="저장(S)", command=self.save_file, accelerator="Ctrl+S", underline=3)
        file_menu.add_command(label="다른 이름으로 저장(A)...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="끝내기(X)", command=self.exit_app)

        # 편집 메뉴
        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="편집(E)", menu=edit_menu, underline=3)
        edit_menu.add_command(label="실행 취소(U)", command=self.text_area.edit_undo, accelerator="Ctrl+Z", underline=6)
        edit_menu.add_command(label="다시 실행(R)", command=self.text_area.edit_redo, accelerator="Ctrl+Y", underline=6)
        edit_menu.add_separator()
        edit_menu.add_command(label="잘라내기(T)", command=lambda: self.text_area.event_generate("<<Cut>>"), accelerator="Ctrl+X", underline=5)
        edit_menu.add_command(label="복사(C)", command=lambda: self.text_area.event_generate("<<Copy>>"), accelerator="Ctrl+C", underline=3)
        edit_menu.add_command(label="붙여넣기(P)", command=lambda: self.text_area.event_generate("<<Paste>>"), accelerator="Ctrl+V", underline=5)
        edit_menu.add_separator()
        edit_menu.add_command(label="모두 선택(A)", command=self.select_all, accelerator="Ctrl+A", underline=6)

        # 단축키 바인딩
        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<Control-a>", lambda event: self.select_all())
        # Ctrl+X, C, V, Z, Y는 텍스트 위젯에서 기본적으로 지원됩니다.

    def new_file(self):
        """
        새 파일을 생성합니다. 변경 사항이 있으면 저장 여부를 묻습니다.
        """
        if self.check_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.text_area.edit_modified(False)
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
                self.text_area.edit_modified(False)
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
                # tkinter 텍스트 위젯은 항상 마지막에 개행 문자를 추가하므로 제거해줍니다.
                if content.endswith('\n'):
                    content = content[:-1]
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                self.text_area.edit_modified(False) # 저장 후 수정 상태 초기화
                self.update_title()
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
        # text_area.edit_modified()는 내용 변경 여부를 boolean으로 반환합니다.
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("메모장", f"변경 내용을 {os.path.basename(self.current_file) if self.current_file else '제목 없음'}에 저장하시겠습니까?")
            if response is True:  # '예'
                self.save_file()
                # save_file 후에도 여전히 수정된 상태이면 저장 실패로 간주하고 종료 취소
                return not self.text_area.edit_modified()
            elif response is False:  # '아니요'
                return True
            else:  # '취소' (None)
                return False
        return True

    def update_title(self):
        """창 제목을 현재 파일 상태에 맞게 업데이트합니다."""
        modified_marker = "*" if self.text_area.edit_modified() else ""
        title = "제목 없음"
        if self.current_file:
            title = os.path.basename(self.current_file)
        
        self.root.title(f"{modified_marker}{title} - 메모장")

    def select_all(self, event=None):
        """
        텍스트 영역의 모든 텍스트를 선택합니다.
        """
        self.text_area.tag_add('sel', '1.0', 'end')
        return 'break' # 다른 바인딩이 실행되지 않도록 합니다.


if __name__ == "__main__":
    main_window = tk.Tk()
    app = NotepadApp(main_window)
    main_window.mainloop()
