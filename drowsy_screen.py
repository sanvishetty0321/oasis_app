import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

class OasisDrowsyOverride(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 1. Main Window Settings
        self.title("OASIS - ALERT: Drowsiness Detected")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        # Force the alert window straight to the front on execution
        self.lift()
        self.attributes('-topmost', True)
        
        self.assets = {}
        
        # 2. Main Full Screen Canvas Layer
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # --- STATIC IMAGE BACKDROP ENGINE ---
        # Explicitly targets your "new.jpeg" alert background file
        bg_asset = None
        for name in ["new.jpeg", "new.JPEG", "new.jpg", "img.jpeg", "login.png"]:
            if os.path.exists(name):
                bg_asset = name
                break
                
        if bg_asset:
            try:
                raw_image = Image.open(bg_asset)
                resized_image = raw_image.resize((980, 680), Image.Resampling.LANCZOS)
                self.assets["bg_img"] = ImageTk.PhotoImage(resized_image)
                self.main_canvas.create_image(0, 0, image=self.assets["bg_img"], anchor="nw")
                print(f"👉 SYSTEM LOG: Successfully loaded drowsy background asset: {bg_asset}")
            except Exception as e:
                print(f"❌ SYSTEM ERROR Decoding Image: {e}")
        else:
            print("⚠️ SYSTEM LOG: No static asset found for alert screen. Running on default dark template.")

        # --- 3. COMPACT SINGLE-LINE HORIZONTAL BAR (TOP) ---
        # Dark crimson translucent overlay banner bar for urgency (Width: 980px, Height: 65px)
        top_strip_pixel = Image.new("RGBA", (1, 1), (29, 18, 23, 225)) 
        self.assets["top_bar_bg"] = ImageTk.PhotoImage(top_strip_pixel.resize((980, 65)))
        self.main_canvas.create_image(0, 0, image=self.assets["top_bar_bg"], anchor="nw")
        self.main_canvas.create_line(0, 65, 980, 65, fill="#4D2533", width=1)
        
        # Alignment anchor along the single top-line layout
        y_center = 32
        
        # Warning Typography Label Elements
        self.main_canvas.create_text(30, y_center, text="⚠️ DROWSINESS DETECTED:", font=("Arial", 11, "bold"), fill="#FF69B4", anchor="w")
        self.main_canvas.create_text(230, y_center, text="You look sleepy! Stand up, stretch, and move around!", font=("Arial", 11, "bold"), fill="white", anchor="w")

        # --- 4. COMPACT UPPER RESET WORKSPACE BUTTON ---
        btn_stop_x = 810
        btn = tk.Button(
            self, 
            text="Reset Workspace 🔄", 
            font=("Arial", 11, "bold"), 
            fg="white", 
            bg="#FF69B4", 
            activebackground="#FF1493", 
            bd=0, 
            command=self.return_to_hub
        )
        self.main_canvas.create_window(btn_stop_x + 75, y_center, window=btn, width=150, height=28, anchor="center")

    def return_to_hub(self):
        self.destroy()  # Closes the drowsy alert screen window immediately
        os.system("python workspace_screen.py")  # Safely re-opens your main workspace hub script

if __name__ == "__main__":
    app = OasisDrowsyOverride()
    app.mainloop()
