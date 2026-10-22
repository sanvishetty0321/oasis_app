import os
import sys
import tkinter as tk
from tkvideo import tkvideo  # Video loop layer

class OasisDrowsyOverride(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 1. Main Window Settings
        self.title("OASIS - ALERT: Distraction Detected")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        # Force the alert window straight to the front on execution
        self.lift()
        self.attributes('-topmost', True)
        
        # 2. Full-Screen Video Background Label Container (DND.mov)
        self.video_label = tk.Label(self, bg="#0F1219")
        self.video_label.place(x=0, y=0, width=980, height=680)
        
        # Target your drowsy posture movie file formats explicitly
        video_asset = "DND.mov"
        if not os.path.exists(video_asset):
            if os.path.exists("DND.MOV"):
                video_asset = "DND.MOV"
                
        if os.path.exists(video_asset):
            # Stream the movie directly onto the background layer in a continuous loop
            self.player = tkvideo(video_asset, self.video_label, loop=1, size=(980, 680))
            self.player.play()
        else:
            print("⚠️ SYSTEM LOG: 'DND.mov' not found in this directory folder pathway.")

        # 3. Transparent Warning Control Overlay UI Canvas Layer
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="")
        self.main_canvas.place(x=0, y=0)
        
        # Top Header Strip Layout Banner (Slightly darker slate red tint for urgency)
        self.main_canvas.create_rectangle(0, 0, 980, 65, fill="#1D1217", outline="")
        self.main_canvas.create_line(0, 65, 980, 65, fill="#3F232F", width=1)
        
        # Alert Typography
        self.main_canvas.create_text(30, 32, text="⚠️ POSTURE WARNING:", font=("Arial", 11, "bold"), fill="#FF69B4", anchor="w")
        self.main_canvas.create_text(210, 32, text="Slouching or Drowsiness detected! Re-align your position.", font=("Arial", 11), fill="white", anchor="w")
        
        # Action Return Reset Button
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
        self.main_canvas.create_window(880, 32, window=btn, width=150, height=28)

    def return_to_hub(self):
        self.destroy()  # Closes the drowsy screen overlay window immediately
        os.system("python workspace_screen.py")  # Boots the home workspace page back up safely

if __name__ == "__main__":
    app = OasisOverride() if 'OasisOverride' in globals() else OasisDrowsyOverride()
    app.mainloop()
