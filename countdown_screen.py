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
        
        # 1. Video Background Label Container
        self.video_label = tk.Label(self, bg="#0F1219")
        self.video_label.place(x=0, y=0, width=980, height=680)
        
        # --- FIXED: AUTOMATIC VIDEO FILE LOOKUP ENGINE ---
        video_asset = None
        current_dir_files = os.listdir(".") # Reads every single file inside your folder
        
        # Look for any file that starts with "tenor4" or has "tenor4" in it
        for file in current_dir_files:
            if "tenor4" in file.lower():
                # Check for standard video extensions
                if file.lower().endswith(('.mov', '.mp4', '.avi', '.m4v', '.mkv')):
                    video_asset = file
                    break
                    
        # If it still can't find it, fall back to any video file in the folder as a rescue
        if not video_asset:
            for file in current_dir_files:
                if file.lower().endswith(('.mov', '.mp4')):
                    video_asset = file
                    break

        if video_asset and os.path.exists(video_asset):
            print(f"👉 SYSTEM LOG: Successfully matched and loading video asset: {video_asset}")
            try:
                # Streams your exact .mov format file cleanly at an optimized refresh rate
                self.player = tkvideo(video_asset, self.video_label, loop=1, size=(980, 680), hz=30)
                self.player.play()
            except Exception as e:
                print(f"❌ SYSTEM ERROR: Found {video_asset} but your system codecs cannot play it. Details: {e}")
        else:
            print("⚠️ SYSTEM WARNING: No video file containing the name 'tenor4' could be resolved in this directory.")

        # 2. Transparent Control Overlay UI Canvas Layer
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.place(x=0, y=0)
        
        # Style your top horizontal bar header
        self.main_canvas.create_rectangle(0, 0, 980, 65, fill="#141821", outline="")
        self.main_canvas.create_line(0, 65, 980, 65, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(30, 32, text="⚡ Focus Session Progress:", font=("Arial", 11, "bold"), fill="#FF69B4", anchor="w")
        self.clock_id = self.main_canvas.create_text(250, 32, text=self.format_time(self.total_seconds_left), font=("Courier New", 20, "bold"), fill="white", anchor="w")
        self.main_canvas.create_text(420, 32, text="Status: Focus window active.", font=("Arial", 11), fill="#A0AAB5", anchor="w")
        
        btn = tk.Button(self, text="Close App 🛑", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.exit_app)
        self.main_canvas.create_window(890, 32, window=btn, width=120, height=28)
        
        # Forces the buttons and text straight over the top of your background movie
        self.main_canvas.lift()
        
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
