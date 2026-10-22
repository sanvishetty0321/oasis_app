import os
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class OasisDrowsyAlert(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 1. Main Window Setup
        self.title("OASIS - ALERT SYSTEM")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        # Force window straight to the front to catch user attention
        self.lift()
        self.attributes('-topmost', True)
        
        self.gif_frames = []
        self.current_frame = 0
        
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # 2. Load Full Screen DND.gif
        gif_asset = None
        for name in ["DND.gif", "dnd.gif", "DND.GIF"]:
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
        else:
            self.main_canvas.create_text(490, 200, text="⚠️ ALERT SCREEN Active ⚠️", font=("Arial", 24, "bold"), fill="red")
            self.main_canvas.create_text(490, 300, text="[ Place DND.gif inside the OasisTest folder ]", font=("Arial", 14), fill="#A0AAB5")

        # 3. Top Banner Warning Strip Overlay
        self.top_pixel = Image.new("RGBA", (1, 1), (15, 18, 25, 230))
        self.top_photo = ImageTk.PhotoImage(self.top_pixel.resize((980, 75)))
        self.main_canvas.create_image(0, 0, image=self.top_photo, anchor="nw")
        self.main_canvas.create_line(0, 75, 980, 75, fill="red", width=2)
        
        # Centered bold wake up warning text
        self.main_canvas.create_text(490, 38, text="🚨 DROWSINESS/SLOUCHING DETECTED! WAKE UP & RESET POSTURE 🚨", font=("Arial", 14, "bold"), fill="red")

        # 4. Action Dismiss Button to go back to work
        btn = tk.Button(self, text="Dismiss & Resume Work ⚡", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.resume_work)
        self.main_canvas.create_window(490, 620, window=btn, width=240, height=35)

    def animate_gif(self):
        if self.gif_frames:
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.main_canvas.itemconfig(self.bg_id, image=self.gif_frames[self.current_frame])
            self.main_canvas.tag_lower(self.bg_id)
            self.after(60, self.animate_gif)

    def resume_work(self):
        self.destroy() # Closes alert screen safely
        os.system("python workspace_screen.py") # Returns user straight to home base workspace

if __name__ == "__main__":
    app = OasisDrowsyAlert()
    app.mainloop()
