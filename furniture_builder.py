import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk


# ── Flyweight: Color ──────────────────────────────────────────────────────────

class Color:
    def __init__(self, color_name, color_code):
        self.color_name = color_name
        self.color_code = color_code

    def __str__(self):
        return f"{self.color_name} (Color Code: {self.color_code})"


class FlyweightFactory:
    _colors = {}

    @staticmethod
    def get_color(color_name):
        color_codes = {
            'White':    (255, 255, 255),
            'Black':    (0, 0, 0),
            'Green':    (0, 255, 0),
            'Wood':     (139, 69, 19),
            'Grey':     (128, 128, 128),
            'Darkgrey': (47, 79, 79),
            'Walnut':   (192, 180, 171),
        }
        if color_name not in FlyweightFactory._colors:
            FlyweightFactory._colors[color_name] = Color(color_name, color_codes[color_name])
        return FlyweightFactory._colors[color_name]


# ── Core: Furniture ───────────────────────────────────────────────────────────

class Furniture:
    def __init__(self, furniture_type):
        self.furniture_type = furniture_type
        self.features = []
        self.color = None

    def add_feature(self, feature):
        self.features.append(feature)

    def set_material(self, material):
        self.material = material

    def set_color(self, color):
        self.color = color

    def __str__(self):
        furniture = self.furniture_type
        features_str = ", ".join(self.features) if self.features else "No additional features"
        color_str = str(self.color) if self.color else "None"
        return f"Furniture: {furniture}\nOptions: {features_str}\nColor: {color_str}\n"


# ── Builder ───────────────────────────────────────────────────────────────────

class FurnitureBuilder:
    def __init__(self, furniture_type):
        self.furniture = Furniture(furniture_type)

    def add_feature(self, feature):
        self.furniture.add_feature(feature)
        return self

    def set_color(self, color):
        self.furniture.set_color(color)
        return self

    def build(self):
        return self.furniture


# ── Decorator ─────────────────────────────────────────────────────────────────

class FeatureDecorator(Furniture):
    def __init__(self, furniture):
        super().__init__(furniture.furniture_type)
        self._furniture = furniture
        self.features = furniture.features.copy()
        self.color = furniture.color

    def __str__(self):
        return f"{str(self._furniture)}"

    def add_feature(self, feature):
        self._furniture.add_feature(feature)


class WheelDecorator(FeatureDecorator):
    def __init__(self, furniture, color):
        super().__init__(furniture)
        self.add_feature(f'Wheel ({color})')


class ArmrestDecorator(FeatureDecorator):
    def __init__(self, furniture, color):
        super().__init__(furniture)
        self.add_feature(f'Armrest ({color})')


class MirrorDecorator(FeatureDecorator):
    def __init__(self, furniture):
        super().__init__(furniture)
        self.add_feature('Mirror Door')


class AdjustableHeightDecorator(FeatureDecorator):
    def __init__(self, furniture):
        super().__init__(furniture)
        self.add_feature('Adjustable Height')


# ── Memento ───────────────────────────────────────────────────────────────────

class Memento:
    def __init__(self, state):
        self._state = state

    def get_saved_state(self):
        return self._state


class Caretaker:
    def __init__(self):
        self._mementos = []

    def save(self, memento):
        self._mementos.append(memento)

    def undo(self):
        if self._mementos:
            return self._mementos.pop()
        return None


caretaker = Caretaker()


# ── Custom MessageBox ─────────────────────────────────────────────────────────

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.configure(bg='#f0e6f7')
        self.geometry("300x150")
        self.resizable(False, False)

        tk.Label(self, text=message, bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).pack(pady=20)

        button_frame = tk.Frame(self, bg='#f0e6f7')
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="OK",
                   command=self.destroy, style='TButton').pack()


# ── Main Application ──────────────────────────────────────────────────────────

class FurnitureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Furniture Builder")
        self.root.configure(bg='#f0e6f7')

        self.style = ttk.Style()
        self.style.configure('TMenubutton', background='#ffe4e1',
                              foreground='black', font=('Comic Sans MS', 12), padding=5)
        self.style.map('TMenubutton',
                       background=[('active', '#ffd3b6')],
                       relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        self.style.configure('TButton', background='#ffe4e1',
                              foreground='black', font=('Comic Sans MS', 12),
                              relief='raised')
        self.style.map('TButton',
                       background=[('active', '#ffd3b6'), ('!active', '#ffe4e1')])

        self.leg_color_var = tk.StringVar(value="Black")
        self.leg_color_menu = None

        self.frame = tk.Frame(self.root, bg='#f0e6f7', padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="NSEW")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Furniture Type:", bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).grid(row=0, column=0, pady=5, sticky='w')
        tk.Label(self.frame, text="Color:", bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).grid(row=1, column=0, pady=5, sticky='w')
        tk.Label(self.frame, text="Options:", bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).grid(row=3, column=0, pady=5, sticky='w')

        self.create_labels()
        self.create_options()
        self.create_checkbuttons()
        self.create_buttons()
        self.create_result_box()
        self.create_image_box()

    def create_labels(self):
        tk.Label(self.frame, text="Furniture Type:", bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).grid(row=0, column=0, pady=5, sticky='w')
        tk.Label(self.frame, text="Color:", bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).grid(row=1, column=0, pady=5, sticky='w')
        tk.Label(self.frame, text="Options:", bg='#f0e6f7',
                 font=('Comic Sans MS', 12)).grid(row=3, column=0, pady=5, sticky='w')

    def create_options(self):
        self.furniture_var = tk.StringVar(value="Chair")
        self.furniture_menu = tk.OptionMenu(
            self.frame, self.furniture_var,
            "Chair", "Wardrobe", "Desk",
            command=self.update_color_options
        )
        self.furniture_menu.config(bg='#ffe4e1', fg='black', font=('Comic Sans MS', 12))
        self.furniture_menu["menu"].config(bg='#ffe4e1', fg='black', font=('Comic Sans MS', 12))
        self.furniture_menu.grid(row=0, column=1, pady=5)

        self.color_var = tk.StringVar(value="White")
        self.color_menu = tk.OptionMenu(self.frame, self.color_var,
                                        "White", "Grey", "Green")
        self.color_menu.config(bg='#ffe4e1', fg='black', font=('Comic Sans MS', 12))
        self.color_menu["menu"].config(bg='#ffe4e1', fg='black', font=('Comic Sans MS', 12))
        self.color_menu.grid(row=1, column=1, pady=5)

        self.leg_color_var = tk.StringVar(value="Black")

    def update_color_options(self, *args):
        furniture = self.furniture_var.get()
        self.color_menu["menu"].delete(0, "end")

        self.option_var.set(False)
        self.toggle_options()

        if furniture == 'Chair':
            colors = ["White", "Grey", "Green"]
        elif furniture == 'Desk':
            colors = ["Black", "White", "Wood", "Walnut"]
            self.create_leg_color_menu()
        elif furniture == 'Wardrobe':
            colors = ["Darkgrey", "Grey", "White", "Wood"]

        for color in colors:
            self.color_menu["menu"].add_command(
                label=color, command=tk._setit(self.color_var, color)
            )

        if furniture != 'Desk':
            if hasattr(self, 'leg_color_label'):
                self.leg_color_label.grid_remove()
            if self.leg_color_menu is not None:
                self.leg_color_menu.grid_remove()
        else:
            if hasattr(self, 'leg_color_label'):
                self.leg_color_label.grid()
            if self.leg_color_menu is not None:
                self.leg_color_menu.grid()

    def create_leg_color_menu(self):
        if self.leg_color_menu is None:
            self.leg_color_label = tk.Label(self.frame, text="Leg Color:",
                                            bg='#f0e6f7', font=('Comic Sans MS', 12))
            self.leg_color_label.grid(row=2, column=0, pady=5, sticky='w')
            self.leg_color_menu = tk.OptionMenu(self.frame, self.leg_color_var,
                                                "Black", "White")
            self.leg_color_menu.config(bg='#ffe4e1', fg='black', font=('Comic Sans MS', 12))
            self.leg_color_menu["menu"].config(bg='#ffe4e1', fg='black',
                                               font=('Comic Sans MS', 12))
            self.leg_color_menu.grid(row=2, column=1, pady=5)
        else:
            self.leg_color_menu["menu"].delete(0, "end")
            for color in ["Black", "White"]:
                self.leg_color_menu["menu"].add_command(
                    label=color, command=tk._setit(self.leg_color_var, color)
                )

    def create_checkbuttons(self):
        self.option_var = tk.BooleanVar()
        tk.Checkbutton(
            self.frame, text="Add Options", variable=self.option_var,
            command=self.toggle_options, bg='#f0e6f7',
            font=('Comic Sans MS', 12), selectcolor="#ffd3b6"
        ).grid(row=3, column=1, pady=5, sticky='w')

        self.option_frame = tk.Frame(self.frame, bg='#f0e6f7')
        self.option_frame.grid(row=4, columnspan=2, pady=5, sticky='ew')

    def create_buttons(self):
        self.button_frame = tk.Frame(self.frame, bg='white',
                                     relief='raised', borderwidth=1)
        self.button_frame.grid(row=5, columnspan=2, pady=10, sticky='ew')

        create_button = ttk.Button(self.button_frame, text="🪑 Create Furniture",
                                   command=self.create_furniture, style='TButton')
        create_button.pack(side='left', padx=5)

        undo_button = ttk.Button(self.button_frame, text="← Undo",
                                 command=self.undo_furniture, style='TButton')
        undo_button.pack(side='left', padx=5)

        show_button = ttk.Button(self.button_frame, text="🔍 Show Furniture",
                                 command=self.show_furniture, style='TButton')
        show_button.pack(side='left', padx=5)

    def create_result_box(self):
        self.result_text = tk.Text(self.frame, height=5, width=50, wrap="word",
                                   bg="#f0e6f7", fg="black", font=("Comic Sans MS", 12))
        self.result_text.grid(row=6, column=0, columnspan=2, pady=5, sticky='ew')

    def create_image_box(self):
        self.image_label = ttk.Label(self.frame)
        self.image_label.grid(row=7, column=0, columnspan=2,
                               sticky="nsew", padx=20, pady=0)
        self.frame.grid_columnconfigure(0, weight=1)

    def toggle_options(self):
        for widget in self.option_frame.winfo_children():
            widget.destroy()

        if self.option_var.get():
            furniture = self.furniture_var.get()
            if furniture == 'Chair':
                options = ["Wheel", "Armrest"]
                self.option_vars = []
                for option in options:
                    frame = tk.Frame(self.option_frame, bg='#f0e6f7')
                    frame.pack(anchor='w', fill='x')
                    var = tk.BooleanVar()
                    self.option_vars.append((option, var))
                    check = tk.Checkbutton(frame, text=option, variable=var,
                                           bg='#f0e6f7', font=('Comic Sans MS', 12))
                    check.pack(side='left')
                    color_var = tk.StringVar(value="Black")
                    color_menu = tk.OptionMenu(frame, color_var, "Black", "White")
                    color_menu.config(bg='#ffe4e1', fg='black', font=('Comic Sans MS', 12))
                    color_menu["menu"].config(bg='#ffe4e1', fg='black',
                                              font=('Comic Sans MS', 12))
                    color_menu.pack(side='left')
                    self.option_vars.append((f"{option}_color", color_var))

            elif furniture == 'Wardrobe':
                options = ["Mirror"]
                self.option_vars = []
                for option in options:
                    var = tk.BooleanVar()
                    self.option_vars.append((option, var))
                    tk.Checkbutton(self.option_frame, text=option, variable=var,
                                   bg='#f0e6f7', font=('Comic Sans MS', 12)).pack(anchor='w')

            elif furniture == 'Desk':
                options = ["Adjustable Height"]
                self.option_vars = []
                for option in options:
                    var = tk.BooleanVar()
                    self.option_vars.append((option, var))
                    tk.Checkbutton(self.option_frame, text=option, variable=var,
                                   bg='#f0e6f7', font=('Comic Sans MS', 12)).pack(anchor='w')

    def create_furniture(self):
        furniture_type = self.furniture_var.get()
        color = self.color_var.get()

        builder = FurnitureBuilder(furniture_type)
        builder.set_color(FlyweightFactory.get_color(color))

        base_furniture = builder.build()
        decorated_furniture = base_furniture

        if self.option_var.get():
            for option, var in self.option_vars:
                if var.get():
                    if option == "Wheel":
                        decorated_furniture = WheelDecorator(
                            decorated_furniture, self.leg_color_var.get()
                        )
                    elif option == "Armrest":
                        decorated_furniture = ArmrestDecorator(
                            decorated_furniture, color
                        )
                    elif option == "Mirror":
                        decorated_furniture = MirrorDecorator(decorated_furniture)
                    elif option == "Adjustable Height":
                        decorated_furniture = AdjustableHeightDecorator(decorated_furniture)

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(decorated_furniture))
        state = self.result_text.get("1.0", tk.END)
        caretaker.save(Memento(state))

    def undo_furniture(self):
        memento = caretaker.undo()
        if memento:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, memento.get_saved_state())
        else:
            self.show_custom_messagebox("Undo", "Nothing to undo.")

    def show_custom_messagebox(self, title, message):
        CustomMessageBox(self.root, title, message)

    def show_furniture(self):
        furniture_type = self.furniture_var.get()
        color = self.color_var.get()

        if furniture_type == 'Chair':
            armrest_color = "none"
            wheel_color = "none"
            if self.option_var.get():
                for i in range(0, len(self.option_vars), 2):
                    option, var = self.option_vars[i]
                    _, color_var = self.option_vars[i + 1]
                    if var.get():
                        if option == "Wheel":
                            wheel_color = color_var.get()
                        elif option == "Armrest":
                            armrest_color = color_var.get()
            filename = f"chair_{color.lower()}_{armrest_color.lower()}_{wheel_color.lower()}.png"

        elif furniture_type == 'Desk':
            leg_color = self.leg_color_var.get()
            height_option = "none"
            if self.option_var.get():
                for option, var in self.option_vars:
                    if option == "Adjustable Height" and var.get():
                        height_option = "opt"
            filename = f"desk_{color.lower()}_{leg_color.lower()}_{height_option.lower()}.png"

        elif furniture_type == 'Wardrobe':
            mirror_option = "none"
            if self.option_var.get():
                for option, var in self.option_vars:
                    if option == "Mirror" and var.get():
                        mirror_option = "mirror"
            filename = f"wardrobe_{color.lower()}_{mirror_option.lower()}.png"

        # 이미지 폴더 경로 지정 (코드 파일 기준 상대경로)
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, "이미지", "설패", filename)

        try:
            image = Image.open(filepath)
            new_width = 480
            new_height = 360
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file not found: {filepath}")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = FurnitureApp(root)
    root.mainloop()
