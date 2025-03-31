import tkinter as tk
from tkinter import messagebox
import random
import time


class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SLOT MACHINE")
        self.root.geometry("600x500")
        self.root.configure(bg="#162447")
       # self.root.resizable(False, False)  # Prevent resizing

        # Splash Screen
        self.splash_canvas = tk.Canvas(self.root, width=600, height=500, bg="yellow")
        self.splash_canvas.pack()
        self.splash_canvas.create_text(300, 350, text="Loading...", font=("Arial", 16, "bold"), tags="loading_text")

        self.loading_arc = self.splash_canvas.create_arc(270, 250, 330, 310, start=0, extent=30, outline="black",
                                                         width=3, tags="arc")
        self.angle = 0
        self.animate_loading()

        self.root.after(2000, self.show_main_screen)  # Show main screen after 2 seconds

        self.root.bind('<Return>', self.spin)

    def animate_loading(self):
        try:
            self.angle = (self.angle + 10) % 360
            self.splash_canvas.itemconfig(self.loading_arc, extent=self.angle)
            self.root.after(50, self.animate_loading)
        except tk.TclError:
            pass  # Ignore errors if the canvas is deleted

    def show_main_screen(self):
        self.splash_canvas.destroy()

        # Title
        header = tk.Label(self.root, text="SLOT MACHINE", font=("Arial", 20, "bold"), bg="yellow", fg="black")
        header.pack(fill=tk.X)

        # Balance
        self.balance = 100
        self.balance_label = tk.Label(self.root, text=f"Balance: ${self.balance}", font=("Arial", 14), bg="#162447",
                                      fg="white")
        self.balance_label.pack(pady=10)

        # Slot Box Frame
        self.slot_frame = tk.Frame(self.root, bg="#1f4068", relief=tk.RIDGE, bd=3, width = 240, height = 80, padx=10, pady=10)
        self.slot_frame.pack(pady=10)
        self.slot_frame.pack_propagate(False)

        # Slot Symbols
        self.symbols = ["🍒", "🔔", "🍋", "🍉", "⭐", "🍇"]
        self.current_slots = random.choices(self.symbols, k=3)

        # Separate labels for symbols and separators
        self.slot_labels = []
        self.separator_labels = []

        for i in range(3):
            lbl = tk.Label(self.slot_frame, text=self.current_slots[i], font=("Arial", 28), bg="#1f4068", fg="white",  width=2, height=2)
            lbl.pack(side=tk.LEFT, padx=5)
            self.slot_labels.append(lbl)

            if i < 2:  # Add '|' separator only between symbols
                sep = tk.Label(self.slot_frame, text="|", font=("Arial", 28), bg="#1f4068", fg="white")
                sep.pack(side=tk.LEFT)
                self.separator_labels.append(sep)

        # Bet Entry
        self.bet_label = tk.Label(self.root, text="Enter Bet Amount:", font=("Arial", 12), bg="#162447", fg="white")
        self.bet_label.pack(pady=5)

        self.bet_entry = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.bet_entry.pack(pady=5)

        # Spin Button
        self.spin_button = tk.Button(self.root, text="SPIN", font=("Arial", 10, "bold"), command=self.spin, bg="white",
                                     fg="black", width=15)
        self.spin_button.pack(pady=10)

        # Footer
        footer = tk.Label(self.root, text=f"@ {time.strftime('%Y')}, All rights reserved", font=("Arial", 10),
                          bg="#162447", fg="white")
        footer.pack(side=tk.BOTTOM, pady=5)

    def spin(self, event=None):
        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.balance:
                messagebox.showerror("Error", "Invalid bet amount")
                return
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
            return

        self.balance -= bet
        self.balance_label.config(text=f"Balance: ${self.balance}")

        for _ in range(15):  # Spin animation
            new_symbols = random.choices(self.symbols, k=3)
            for i in range(3):
                self.slot_labels[i].config(text=new_symbols[i], fg="white")  # Keep symbols white while spinning
            self.root.update()
            time.sleep(0.1)

        result = [lbl.cget("text") for lbl in self.slot_labels]

        if len(set(result)) == 1:  # Win condition
            self.balance += bet * 2
            for lbl in self.slot_labels:
                lbl.config(fg="lightgreen")  # Change only symbols' fg
            self.spin_button.config(bg="lightgreen")
            messagebox.showinfo("You Win!", "Congratulations! You won!")
        else:  # Loss condition
            for lbl in self.slot_labels:
                lbl.config(fg="red")  # Change only symbols' fg
            self.spin_button.config(bg="red")
            messagebox.showinfo("You Lost", "Better luck next time!")

        # Reset colors after message box
        for lbl in self.slot_labels:
            lbl.config(fg="white")  # Reset symbols to white
        for sep in self.separator_labels:
            sep.config(fg="white")  # Keep separators permanently white
        self.spin_button.config(bg="white")  # Reset button

        self.balance_label.config(text=f"Balance: ${self.balance}")

        if self.balance == 0:
            messagebox.showwarning("Game Over", "Insufficient Balance! Reload to play again.")
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
