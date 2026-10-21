import os
import sys
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class OasisCountdownOnly(tk.Tk):
    def __init__(self, target_minutes):
        super().__init__()
        self.title("OASIS - Active Focus Session")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        self.total_seconds_left = target_minutes * 60
        self.gif_frames = []
        self.current_frame = 0
        
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # Load and set up background GIF loop sequence array safely
        gif_asset = None
        for name in ["tenor4.gif", "tenor4.GIF", "tenor410.gif", "4dry.gif"]:
            if os.path.exists(name):
                gif_asset = name
                break
                
        if gif_asset:
            raw_gif = Image.open(gif_asset)
            for frame in ImageSequence.Iterator(raw_gif):
                resized = frame.convert("RGBA").resize((980, 680), Image.Resampling.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(resized))
            
            if self.gif_frames:
                self.bg_id = self.main_canvas.create_image(0, 0, image=self.gif_frames[0], anchor="nw")
                self.animate_gif()

        # Top Overlay Banner Design layout components
        self.top_pixel = Image.new("RGBA", (1, 1), (20, 24, 33, 225))
        self.top_photo = ImageTk.PhotoImage(self.top_pixel.resize((980, 65)))
        self.main_canvas.create_image(0, 0, image=self.top_photo, anchor="nw")
        self.main_canvas.create_line(0, 65, 980, 65, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(30, 32, text="⚡ Focus Session Progress:", font=("Arial", 11, "bold"), fill="#FF69B4", anchor="w")
        
        self.clock_id = self.main_canvas.create_text(250, 32, text=self.format_time(self.total_seconds_left), font=("Courier New", 20, "bold"), fill="white", anchor="w")
        self.main_canvas.create_text(420, 32, text="Status: Focus window active.", font=("Arial", 11), fill="#A0AAB5", anchor="w")
        
        # Emergency exit button structure mapping
        btn = tk.Button(self, text="Close App 🛑", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.exit_app)
        self.main_canvas.create_window(890, 32, window=btn, width=120, height=28)
        
        self.run_timer()

    def animate_gif(self):
        if self.gif_frames:
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.main_canvas.itemconfig(self.bg_id, image=self.gif_frames[self.current_frame])
            self.main_canvas.tag_lower(self.bg_id)
            self.after(50, self.animate_gif)

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
    # Pull selected duration values from the command-line argument array context safely
    try:
        chosen_mins = int(sys.argv[1])
    except:
        chosen_mins = 25
        
    app = OasisCountdownOnly(chosen_mins)
    app.mainloop()
