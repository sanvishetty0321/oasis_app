import os
import tkinter as tk
from PIL import Image, ImageTk

class OasisWorkspaceOnly(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OASIS - Workspace Central Hub")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        if os.path.exists("login.jpg"):
            raw_img = Image.open("login.jpg")
            self.bg_img = ImageTk.PhotoImage(raw_img.resize((980, 680), Image.Resampling.LANCZOS))
            self.main_canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # Sidebar
        self.sidebar_pixel = Image.new("RGBA", (1, 1), (20, 24, 33, 215))
        self.sidebar_photo = ImageTk.PhotoImage(self.sidebar_pixel.resize((220, 680)))
        self.main_canvas.create_image(0, 0, image=self.sidebar_photo, anchor="nw")
        self.main_canvas.create_line(220, 0, 220, 680, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(110, 45, text="OASIS", font=("Georgia", 24, "italic", "bold"), fill="#FF69B4")
        self.main_canvas.create_text(35, 130, text="🏠 Home", font=("Arial", 12, "bold"), fill="white", anchor="nw")
        self.main_canvas.create_text(35, 185, text="📋 To-Do List", font=("Arial", 12), fill="#A0AAB5", anchor="nw")
        
        # Top Strip Control
        self.top_pixel = Image.new("RGBA", (1, 1), (30, 34, 43, 160))
        self.top_photo = ImageTk.PhotoImage(self.top_pixel.resize((760, 65)))
        self.main_canvas.create_image(220, 0, image=self.top_photo, anchor="nw")
        self.main_canvas.create_line(220, 65, 980, 65, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(250, 32, text="Focus Minutes:", font=("Arial", 12, "bold"), fill="white", anchor="w")
        
        # Entry Input
        self.mins_entry = tk.Entry(self, font=("Arial", 12, "bold"), fg="white", bg="#0F1219", bd=1, relief="solid", justify="center", insertbackground="white")
        self.mins_entry.insert(0, "25")
        self.main_canvas.create_window(420, 32, window=self.mins_entry, width=60, height=28)
        
        # Start button link
        btn = tk.Button(self, text="Start ⚡", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.go_to_timer)
        self.main_canvas.create_window(545, 32, window=btn, width=110, height=28)

    def go_to_timer(self):
        mins = self.mins_entry.get()
        self.destroy()  # Close home screen window safely
        os.system(f"python countdown_screen.py {mins}")  # Launch timer file with chosen minutes

if __name__ == "__main__":
    app = OasisWorkspaceOnly()
    app.mainloop()
