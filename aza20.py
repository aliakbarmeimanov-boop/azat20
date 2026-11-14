
import tkinter as tk
import math

class ProCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PRO CALCULATOR")
        self.root.geometry("440x700")
        self.root.minsize(360, 600)
        self.root.configure(bg="#10131c")

        self.expression = ""
        self.dark = True

        self.colors = {
            "bg": "#10131c",
            "screen": "#1a2030",
            "button": "#252d40",
            "operator": "#354b70",
            "accent": "#687cff",
            "text": "#ffffff",
            "special": "#a83e50"
        }

        self.create_ui()

    def create_ui(self):
        self.header = tk.Label(
            self.root,
            text="PRO CALCULATOR",
            font=("Arial", 20, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["accent"]
        )
        self.header.pack(pady=15)

        self.display = tk.Entry(
            self.root,
            font=("Arial", 27),
            bg=self.colors["screen"],
            fg="white",
            insertbackground="white",
            justify="right",
            bd=0
        )
        self.display.pack(fill="x", padx=15, ipady=22)

        self.result = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 12),
            bg=self.colors["bg"],
            fg="#8c9ab5",
            anchor="e"
        )
        self.result.pack(fill="x", padx=20, pady=8)

        buttons = [
            ["AC", "DEL", "(", ")", "/"],
            ["7", "8", "9", "*", "√"],
            ["4", "5", "6", "-", "x²"],
            ["1", "2", "3", "+", "%"],
            ["0", ".", "π", "^", "="],
            ["sin", "cos", "tan", "log", "ln"],
            ["1/x", "!", "e", "±", "HIST"]
        ]

        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        for r, row in enumerate(buttons):
            frame.rowconfigure(r, weight=1)
            for c, value in enumerate(row):
                frame.columnconfigure(c, weight=1)

                color = self.colors["button"]

                if value in ["+", "-", "*", "/", "^", "="]:
                    color = self.colors["operator"]
                elif value in ["AC", "DEL"]:
                    color = self.colors["special"]
                elif value == "=":
                    color = self.colors["accent"]

                btn = tk.Button(
                    frame,
                    text=value,
                    font=("Arial", 13, "bold"),
                    bg=color,
                    fg="white",
                    activebackground=self.colors["accent"],
                    activeforeground="white",
                    bd=0,
                    cursor="hand2",
                    command=lambda v=value: self.click(v)
                )
                btn.grid(
                    row=r, column=c,
                    sticky="nsew",
                    padx=4, pady=4
                )

        bottom = tk.Frame(self.root, bg=self.colors["bg"])
        bottom.pack(fill="x", padx=15, pady=10)

        tk.Button(
            bottom,
            text="История",
            command=self.history,
            bg="#354b70",
            fg="white",
            bd=0,
            padx=15,
            pady=10
        ).pack(side="left")

        tk.Button(
            bottom,
            text="Сменить тему",
            command=self.toggle_theme,
            bg="#354b70",
            fg="white",
            bd=0,
            padx=15,
            pady=10
        ).pack(side="right")

        self.history_list = []

        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<Escape>", lambda e: self.clear())

    def click(self, value):
        if value == "AC":
            self.clear()

        elif value == "DEL":
            self.expression = self.expression[:-1]
            self.update_display()

        elif value == "=":
            self.calculate()

        elif value == "HIST":
            self.history()

        elif value == "√":
            self.expression += "sqrt("

        elif value == "x²":
            self.expression += "**2"

        elif value == "π":
            self.expression += "pi"

        elif value == "^":
            self.expression += "**"

        elif value == "sin":
            self.expression += "sin("

        elif value == "cos":
            self.expression += "cos("

        elif value == "tan":
            self.expression += "tan("

        elif value == "log":
            self.expression += "log10("

        elif value == "ln":
            self.expression += "log("

        elif value == "1/x":
            self.expression = f"1/({self.expression})"

        elif value == "!":
            self.expression += "!"

        elif value == "e":
            self.expression += "e"

        elif value == "±":
            self.expression = f"-({self.expression})"

        else:
            self.expression += value

        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def clear(self):
        self.expression = ""
        self.update_display()
        self.result.config(text="Ready")

    def calculate(self):
        try:
            expr = self.expression.replace("!", "_fact")

            expr = expr.replace("%", "/100")

            def factorial_replace(s):
                import re
                pattern = r"(\d+(?:\.\d+)?)_fact"
                return re.sub(
                    pattern,
                    lambda m: f"factorial({m.group(1)})",
                    s
                )

            expr = factorial_replace(expr)

            allowed = {
                "sqrt": math.sqrt,
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "log10": math.log10,
                "log": math.log,
                "factorial": math.factorial,
                "pi": math.pi,
                "e": math.e,
                "abs": abs
            }

            result = eval(
                expr,
                {"__builtins__": {}},
                allowed
            )

            self.history_list.append(
                f"{self.expression} = {result}"
            )

            self.result.config(
                text=f"= {result}",
                fg="#55dfaa"
            )

            self.expression = str(result)
            self.update_display()

        except Exception:
            self.result.config(
                text="Ошибка вычисления",
                fg="#ff647c"
            )

    def history(self):
        window = tk.Toplevel(self.root)
        window.title("История вычислений")
        window.geometry("350x400")
        window.configure(bg="#10131c")

        tk.Label(
            window,
            text="ИСТОРИЯ",
            font=("Arial", 17, "bold"),
            bg="#10131c",
            fg="white"
        ).pack(pady=15)

        listbox = tk.Listbox(
            window,
            bg="#1a2030",
            fg="white",
            font=("Arial", 11),
            bd=0
        )
        listbox.pack(fill="both", expand=True, padx=12, pady=10)

        for item in reversed(self.history_list):
            listbox.insert(tk.END, item)

        def use_result(event):
            selection = listbox.curselection()
            if selection:
                item = listbox.get(selection[0])
                self.expression = item.split(" = ")[-1]
                self.update_display()
                window.destroy()

        listbox.bind("<Double-Button-1>", use_result)

    def toggle_theme(self):
        self.dark = not self.dark

        if self.dark:
            bg = "#10131c"
            screen = "#1a2030"
            fg = "white"
        else:
            bg = "#edf1fa"
            screen = "#ffffff"
            fg = "#182033"

        self.root.configure(bg=bg)
        self.header.configure(bg=bg)
        self.display.configure(bg=screen, fg=fg, insertbackground=fg)
        self.result.configure(bg=bg)
        self.header.configure(fg="#687cff")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProCalculator(root)
    root.mainloop()
