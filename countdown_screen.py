import os
import sys
import tkinter as tk
from tkvideo import tkvideo  

class OasisCountdownOnly(tk.Tk):
    def __init__(self, target_minutes):
        super().__init__()
        self.title("OASIS - Active Focus Session")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        self.total_seconds_left = target_minutes * 60
        
        # 1. Full-Screen Video Background Label Container
        self.video_label = tk.Label(self, bg="#0F1219")
        self.video_label.place(x=0, y=0, width=980, height=680)
        
        video_asset = "tenor4.mov"
        if not os.path.exists(video_asset):
            if os.path.exists("tenor4.MOV"):
                video_asset = "tenor4.MOV"
                
        if os.path.exists(video_asset):
            self.player = tkvideo(video_asset, self.video_label, loop=1, size=(980, 680))
            self.player.play()
        else:
            print("Warning: tenor4.mov not found.")

        # 2. FIXED: UI Overlay Canvas Layer (Removed invalid bg="" to stop the TclError crash)
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0)
        self.main_canvas.place(x=0, y=0)
        
        # Draw Top Header Strip Layout Banner
        self.main_canvas.create_rectangle(0, 0, 980, 65, fill="#141821", outline="")
        self.main_canvas.create_line(0, 65, 980, 65, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(30, 32, text="⚡ Focus Session Progress:", font=("Arial", 11, "bold"), fill="#FF69B4", anchor="w")
        self.clock_id = self.main_canvas.create_text(250, 32, text=self.format_time(self.total_seconds_left), font=("Courier New", 20, "bold"), fill="white", anchor="w")
        self.main_canvas.create_text(420, 32, text="Status: Focus window active.", font=("Arial", 11), fill="#A0AAB5", anchor="w")
        
        # Close Button widget structure
        btn = tk.Button(self, text="Close App 🛑", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.exit_app)
        self.main_canvas.create_window(890, 32, window=btn, width=120, height=28)
        
        self.run_timer()

    def run_timer(self):
        if self.total_seconds_left > 0:
            self.total_seconds_left -= 1
            self.main_canvas.itemconfig(self.clock_id, text=self.format_time(self.total_seconds_left))
            self.after(1000, self.run_timer)
        else:
            self.main_canvas.itemconfig(self.clock_id, text="00:00:00")

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
