import os
import tkinter as tk
from PIL import Image, ImageTk

class OasisLoginOnly(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OASIS - Secure System Entry Portal")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # FIX: Scan for both lowercase and uppercase variations
        self.bg_img = None
        img_target = None
        for name in ["login.png", "login.PNG", "login.jpg", "login.JPEG", "login.jpeg"]:
            if os.path.exists(name):
                img_target = name
                break
                
        if img_target:
            try:
                raw_img = Image.open(img_target)
                self.bg_img = ImageTk.PhotoImage(raw_img.resize((980, 680), Image.Resampling.LANCZOS))
                self.main_canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
                print(f"👉 Login Screen using: {img_target}")
            except Exception as e:
                print(f"Image load error: {e}")

        # Glass Panel Overlay
        self.card_pixel = Image.new("RGBA", (1, 1), (30, 34, 43, 140))
        self.card_photo = ImageTk.PhotoImage(self.card_pixel.resize((380, 300)))
        self.main_canvas.create_image(490, 238, image=self.card_photo, anchor="center")
        self.main_canvas.create_rectangle(300, 88, 680, 388, outline="#2C323F", width=1)
        
        self.main_canvas.create_text(490, 143, text="OASIS", font=("Georgia", 32, "italic", "bold"), fill="#FF69B4")
        self.main_canvas.create_text(490, 193, text="Enter your name", font=("Arial", 12), fill="#A0AAB5")
        
        self.name_entry = tk.Entry(self, font=("Arial", 13), fg="white", bg="#0F1219", bd=1, relief="solid", insertbackground="white", justify="center")
        self.main_canvas.create_window(490, 253, window=self.name_entry, width=260, height=36)
        self.name_entry.focus_set()
        
        btn = tk.Button(self, text="Enter Workspace →", font=("Arial", 12, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.go_to_workspace)
        self.main_canvas.create_window(490, 313, window=btn, width=220, height=38)

    def go_to_workspace(self):
        self.destroy()  
        os.system("python workspace_screen.py")  

if __name__ == "__main__":
    app = OasisLoginOnly()
    app.mainloop()
