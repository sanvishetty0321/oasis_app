import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

class OasisCountdownOnly(tk.Tk):
    def __init__(self, target_minutes):
        super().__init__()
        
        # 1. Main Stage Window Configurations
        self.title("OASIS - Active Focus Session")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        self.total_seconds_left = target_minutes * 60
        self.assets = {}
        
        # 2. Main Full Screen Canvas Layer
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # --- HIGH-RELIABILITY STATIC IMAGE BACKDROP ENGINE ---
        # Explicitly targets your "img.jpeg" background file
        
        # --- BACKGROUND IMAGE ---
        base_dir = os.path.dirname(os.path.abspath(__file__))

        bg_asset = None
        for name in ["img.jpeg", "img.JPEG", "img.jpg", "login.jpeg", "new.jpeg"]:
            image_path = os.path.join(base_dir, "assets", name)
            if os.path.exists(image_path):
                bg_asset = image_path
                break

        if bg_asset:
            try:
                raw_image = Image.open(bg_asset)
                resized_image = raw_image.resize(
                    (980, 680), Image.Resampling.LANCZOS
                )
                self.assets["bg_img"] = ImageTk.PhotoImage(resized_image)
                self.main_canvas.create_image(
                    0, 0, image=self.assets["bg_img"], anchor="nw"
                )
                print(f"Successfully loaded background: {bg_asset}")
            except Exception as e:
                print(f"Error loading background image: {e}")
        else:
            print("No background image found in the assets folder.")

               
        # --- 3. COMPACT SINGLE-LINE HORIZONTAL BAR (TOP) ---
        top_strip_pixel = Image.new("RGBA", (1, 1), (20, 24, 33, 225)) 
        self.assets["top_bar_bg"] = ImageTk.PhotoImage(top_strip_pixel.resize((980, 65)))
        self.main_canvas.create_image(0, 0, image=self.assets["top_bar_bg"], anchor="nw")
        self.main_canvas.create_line(0, 65, 980, 65, fill="#2C323F", width=1)
        
        # Alignment anchors along the single top-line layout
        y_center = 32
        
        # Left Heading Indicator Label
        self.main_canvas.create_text(30, y_center, text="⚡ Focus Session Progress:", font=("Arial", 11, "bold"), fill="#FF69B4", anchor="w")
        
        # Center Digital Countdown Numbers (HH:MM:SS)
        initial_time_str = self.format_time(self.total_seconds_left)
        self.clock_id = self.main_canvas.create_text(
            250, y_center, 
            text=initial_time_str, 
            font=("Courier New", 20, "bold"), 
            fill="white", 
            anchor="w"
        )
        
        # Status Subtitle text block placement inline
        self.main_canvas.create_text(420, y_center, text="Status: Focus window active.", font=("Arial", 11), fill="#A0AAB5", anchor="w")

        # --- 4. COMPACT UPPER CLOSE APP BUTTON ---
        btn_stop_x = 830
        btn = tk.Button(self, text="Close App 🛑", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.exit_app)
        self.main_canvas.create_window(btn_stop_x + 60, y_center, window=btn, width=120, height=28, anchor="center")

        # Start countdown cycle ticker loops
        self.run_timer()

    def run_timer(self):
        if self.total_seconds_left > 0:
            self.total_seconds_left -= 1
            self.main_canvas.itemconfig(self.clock_id, text=self.format_time(self.total_seconds_left))
            self.after(1000, self.run_timer)
        else:
            self.main_canvas.itemconfig(self.clock_id, text="00:00:00")
            print("Session milestone achieved!")

    def format_time(self, total_secs):
        hours = total_secs // 3600
        minutes = (total_secs % 3600) // 60
        seconds = total_secs % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    chosen_mins = 25
    if len(sys.argv) > 1:
        try:
            chosen_mins = int(sys.argv[1])
        except ValueError:
            pass
        
    app = OasisCountdownOnly(chosen_mins)
    app.mainloop()
