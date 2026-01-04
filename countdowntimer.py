import tkinter as tk
from tkinter import messagebox, ttk
import platform

# Windows sound support
if platform.system() == "Windows":
    import winsound


class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("420x380")
        self.root.resizable(False, False)

        self.time_left = 0
        self.running = False
        self.dark_mode = False

        # ttk style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Input frame
        input_frame = ttk.Frame(root, padding=10)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Minutes:").grid(row=0, column=0, padx=5)
        self.min_entry = ttk.Entry(input_frame, width=5, justify="center")
        self.min_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Seconds:").grid(row=0, column=2, padx=5)
        self.sec_entry = ttk.Entry(input_frame, width=5, justify="center")
        self.sec_entry.grid(row=0, column=3, padx=5)

        # Timer label
        self.timer_label = tk.Label(
            root, text="00:00", font=("Helvetica", 48, "bold"), fg="red"
        )
        self.timer_label.pack(pady=20)

        # Buttons
        button_frame = ttk.Frame(root, padding=5)
        button_frame.pack(pady=5)

        self.start_btn = ttk.Button(
            button_frame, text="Start", command=self.start_timer, width=10
        )
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = ttk.Button(
            button_frame, text="Pause", command=self.pause_timer,
            width=10, state="disabled"
        )
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = ttk.Button(
            button_frame, text="Reset", command=self.reset_timer,
            width=10, state="disabled"
        )
        self.reset_btn.grid(row=0, column=2, padx=5)

        # Presets
        preset_frame = ttk.LabelFrame(root, text="Quick Presets", padding=10)
        preset_frame.pack(pady=10)

        ttk.Button(preset_frame, text="1 Min",
                   command=lambda: self.set_preset(1)).grid(row=0, column=0, padx=8)
        ttk.Button(preset_frame, text="5 Min",
                   command=lambda: self.set_preset(5)).grid(row=0, column=1, padx=8)
        ttk.Button(preset_frame, text="10 Min",
                   command=lambda: self.set_preset(10)).grid(row=0, column=2, padx=8)

        # Theme toggle
        self.theme_btn = ttk.Button(
            root, text="🌙 Toggle Dark Mode", command=self.toggle_theme
        )
        self.theme_btn.pack(pady=10)

    # ---------- Functions ----------

    def set_preset(self, minutes):
        self.min_entry.delete(0, tk.END)
        self.sec_entry.delete(0, tk.END)
        self.min_entry.insert(0, str(minutes))
        self.sec_entry.insert(0, "0")

    def start_timer(self):
        if not self.running:
            try:
                minutes = int(self.min_entry.get()) if self.min_entry.get() else 0
                seconds = int(self.sec_entry.get()) if self.sec_entry.get() else 0
                self.time_left = minutes * 60 + seconds

                if self.time_left <= 0:
                    messagebox.showerror("Invalid Input", "Enter a positive time!")
                    return

                self.running = True
                self.update_timer()

                self.start_btn.config(state="disabled")
                self.pause_btn.config(state="normal")
                self.reset_btn.config(state="normal")

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter numbers only!")

    def update_timer(self):
        if self.running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)

        elif self.time_left == 0:
            self.timer_label.config(text="00:00")
            self.play_sound()
            messagebox.showinfo("Time's up!", "⏰ Countdown finished!")
            self.running = False
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")

    def play_sound(self):
        if platform.system() == "Windows":
            winsound.Beep(1000, 500)
        else:
            self.root.bell()

    def pause_timer(self):
        if self.running:
            self.running = False
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")

    def reset_timer(self):
        self.running = False
        self.time_left = 0
        self.timer_label.config(text="00:00")
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")

    def toggle_theme(self):
        if not self.dark_mode:
            self.root.configure(bg="#1e1e1e")
            self.timer_label.config(bg="#1e1e1e", fg="lime")
            self.style.configure("TFrame", background="#1e1e1e")
            self.style.configure("TLabel", background="#1e1e1e", foreground="white")
            self.style.configure("TButton", background="#333333", foreground="white")
            self.dark_mode = True
        else:
            self.root.configure(bg="SystemButtonFace")
            self.timer_label.config(bg="SystemButtonFace", fg="red")
            self.style.configure("TFrame", background="SystemButtonFace")
            self.style.configure("TLabel", background="SystemButtonFace", foreground="black")
            self.style.configure("TButton", background="SystemButtonFace", foreground="black")
            self.dark_mode = False


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
