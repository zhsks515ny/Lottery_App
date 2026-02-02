import random
import tkinter as tk
from tkinter import ttk
import winsound
import threading

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lottery Number Generator")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Title.TLabel",
                        font=("Segoe UI", 20, "bold"),
                        foreground="#eee",
                        background="#1a1a2e")

        style.configure("Rule.TLabel",
                        font=("Segoe UI", 10),
                        foreground="#888",
                        background="#1a1a2e")

    def play_generate_sound(self):
        """Play a slot machine style sound effect."""
        def sound_thread():
            frequencies = [400, 500, 600, 700, 800, 1000, 1200]
            for freq in frequencies:
                winsound.Beep(freq, 50)
            winsound.Beep(1500, 150)
            winsound.Beep(1800, 150)
            winsound.Beep(2000, 200)

        threading.Thread(target=sound_thread, daemon=True).start()

    def play_click_sound(self):
        """Play a simple click sound."""
        threading.Thread(target=lambda: winsound.Beep(800, 30), daemon=True).start()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="🎰 Lottery Generator", style="Title.TLabel")
        title.pack(pady=(30, 5))

        # Rule description
        rule = ttk.Label(self.root,
                         text="1st digit: 1-5  |  2nd-7th digits: 0-9",
                         style="Rule.TLabel")
        rule.pack(pady=(0, 20))

        # Count selector frame
        count_frame = tk.Frame(self.root, bg="#1a1a2e")
        count_frame.pack(pady=10)

        count_label = tk.Label(count_frame, text="Numbers to generate:",
                               font=("Segoe UI", 11), fg="#ccc", bg="#1a1a2e")
        count_label.pack(side=tk.LEFT, padx=(0, 10))

        self.count_var = tk.IntVar(value=5)
        count_spin = tk.Spinbox(count_frame, from_=1, to=5,
                                textvariable=self.count_var, width=5,
                                font=("Segoe UI", 12), justify="center",
                                command=self.play_click_sound)
        count_spin.pack(side=tk.LEFT)

        # Generate button
        generate_btn = tk.Button(self.root, text="✨ Generate Numbers ✨",
                                 font=("Segoe UI", 13, "bold"),
                                 bg="#e94560", fg="white",
                                 activebackground="#ff6b6b",
                                 activeforeground="white",
                                 border=0, padx=30, pady=12,
                                 cursor="hand2",
                                 command=self.generate_numbers)
        generate_btn.pack(pady=20)

        # Hover effects for button
        generate_btn.bind("<Enter>", lambda e: generate_btn.configure(bg="#ff6b6b"))
        generate_btn.bind("<Leave>", lambda e: generate_btn.configure(bg="#e94560"))

        # Results frame
        self.results_frame = tk.Frame(self.root, bg="#16213e", padx=20, pady=15)
        self.results_frame.pack(fill=tk.BOTH, padx=30, pady=(10, 30))

        results_title = tk.Label(self.results_frame, text="Generated Numbers",
                                 font=("Segoe UI", 12, "bold"),
                                 fg="#e94560", bg="#16213e")
        results_title.pack(anchor="w")

        # Results container
        self.results_container = tk.Frame(self.results_frame, bg="#16213e")
        self.results_container.pack(fill=tk.BOTH, pady=(10, 0))

        # Generate initial numbers
        self.generate_numbers()

    def generate_lottery_number(self, first_digit):
        remaining_digits = [random.randint(0, 9) for _ in range(6)]
        return str(first_digit) + ''.join(map(str, remaining_digits))

    def generate_numbers(self):
        # Play sound effect
        self.play_generate_sound()

        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        # Generate new numbers with unique first digits (sorted ascending)
        count = self.count_var.get()
        first_digits = sorted(random.sample([1, 2, 3, 4, 5], count))

        for i in range(count):
            number = self.generate_lottery_number(first_digits[i])
            formatted = f"  {number[0]}조  -  {number[1:4]}  -  {number[4:]}"

            row = tk.Frame(self.results_container, bg="#16213e")
            row.pack(fill=tk.X, pady=4)

            num_label = tk.Label(row, text=f"{number[0]}조",
                                 font=("Segoe UI", 14, "bold"),
                                 fg="#e94560", bg="#16213e", width=4)
            num_label.pack(side=tk.LEFT)

            value_label = tk.Label(row, text=f"  {number[1:4]}  -  {number[4:]}",
                                   font=("Consolas", 16, "bold"),
                                   fg="#00d9ff", bg="#0f3460",
                                   padx=20, pady=8)
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Copy button
            copy_btn = tk.Button(row, text="📋",
                                 font=("Segoe UI", 11),
                                 bg="#0f3460", fg="white",
                                 activebackground="#1a5276",
                                 border=0, padx=12, pady=5,
                                 cursor="hand2",
                                 command=lambda n=number: self.copy_to_clipboard(n))
            copy_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Update window size after widgets are created
        self.root.update_idletasks()
        self.resize_window(count)

    def resize_window(self, count):
        """Resize window based on number of lottery numbers."""
        base_height = 350
        row_height = 50
        padding = 70

        total_height = base_height + (count * row_height) + padding
        width = 550

        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - total_height) // 2

        self.root.geometry(f"{width}x{total_height}+{x}+{y}")

    def copy_to_clipboard(self, number):
        self.root.clipboard_clear()
        self.root.clipboard_append(number)
        self.play_click_sound()

def main():
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
