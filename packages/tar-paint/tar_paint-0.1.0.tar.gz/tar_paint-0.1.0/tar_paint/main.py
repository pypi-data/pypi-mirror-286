import tkinter as tk
from tkinter.colorchooser import askcolor


class PaintApp:
    def __init__(self, root):
        self.lang = "eng"
        self.root = root
        self.lang_menu_text = {}
        self.update_language()
        self.mode = "draw"
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.current_color = "black"
        self.eraser_color = "white"

        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM, fill=tk.X)
        self.init_menu()

    def init_menu(self, delete=False):
        if delete:
            self.menubar.delete(0, tk.END)

        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.lang_menu_text["language"], menu=self.lang_menu)
        self.lang_menu.add_command(label="English", command=self.set_english)
        self.lang_menu.add_command(label="ไทย", command=self.set_thai)

        color_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.lang_menu_text["colors"], menu=color_menu)
        color_menu.add_command(label=self.lang_menu_text["choose_color"], command=self.choose_color)

        tool_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.lang_menu_text["tools"], menu=tool_menu)
        tool_menu.add_command(label=self.lang_menu_text["eraser"], command=self.use_eraser)
        tool_menu.add_command(label=self.lang_menu_text["brush"], command=self.use_brush)

        if hasattr(self, 'clear_button'):
            self.clear_button.config(text=self.lang_buttons["clear"])
        else:
            self.clear_button = tk.Button(self.root, text=self.lang_buttons["clear"], command=self.clear_canvas)
            self.clear_button.pack(side=tk.BOTTOM, fill=tk.X)

    def set_english(self):
        self.lang = "eng"
        self.update_language()
        self.init_menu(delete=True)

    def set_thai(self):
        self.lang = "th"
        self.update_language()
        self.init_menu(delete=True)

    def update_language(self):
        if self.lang == "eng":
            self.lang_menu_text = {
                "colors": "Colors",
                "choose_color": "Choose Color",
                "tools": "Tools",
                "eraser": "Eraser",
                "brush": "Brush",
                "language": "Language"
            }
            self.lang_buttons = {
                "clear": "Clear"
            }
            self.root.title("Tar Paint")
        else:
            self.lang_menu_text = {
                "colors": "สี",
                "choose_color": "เลือกสี",
                "tools": "เครื่องมือ",
                "eraser": "ยางลบ",
                "brush": "แปรง",
                "language": "ภาษา"
            }
            self.lang_buttons = {
                "clear": "ล้าง"
            }
            self.root.title("ต้าร์ วาดรูป")
            # self.update_language_menu()

    def on_click(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        x, y = event.x, event.y
        if self.mode == "draw":
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.current_color, width=2)
        elif self.mode == "erase":
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.eraser_color, width=10)
        self.last_x, self.last_y = x, y

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.current_color = color

    def use_eraser(self):
        self.mode = "erase"

    def use_brush(self):
        self.mode = "draw"

    def clear_canvas(self):
        self.canvas.delete("all")


def main():
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
