import os
import subprocess
import sys
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from blink_timer1 import (
    SessionDatabase,
    BlinkDetector,
    FocusTimer,
    format_time,
    draw_text,
    play_alert,
    DATABASE_FILE,
)

class OasisWorkspaceOnly(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OASIS - Workspace Central Hub")
        self.geometry("980x680")
        self.configure( bg="#0F1219")  
        self.resizable(False, False)
        
        # 1. Main Canvas Layer
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # Load your login.png file directly to keep the background the same
        
        self.bg_img = None
        image_path = os.path.join("assets", "login.jpeg")

        if os.path.exists(image_path):
            raw_img = Image.open(image_path)
            self.bg_img = ImageTk.PhotoImage(
                raw_img.resize((980, 680), Image.Resampling.LANCZOS)
            )
            self.main_canvas.create_image(
                0, 0, image=self.bg_img, anchor="nw"
            )
        else:
            print(f"Warning: Background image not found at {image_path}")

        
        # Left Sidebar Panel Overlay
        self.sidebar_pixel = Image.new("RGBA", (1, 1), (20, 24, 33, 215))
        self.sidebar_photo = ImageTk.PhotoImage(self.sidebar_pixel.resize((220, 680)))
        self.main_canvas.create_image(0, 0, image=self.sidebar_photo, anchor="nw")
        self.main_canvas.create_line(220, 0, 220, 680, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(110, 45, text="OASIS", font=("Georgia", 24, "italic", "bold"), fill="#FF69B4")
        self.main_canvas.create_text(35, 130, text="🏠 Home", font=("Arial", 12, "bold"), fill="white", anchor="nw")
        self.main_canvas.create_text(35, 185, text="📋 To-Do List", font=("Arial", 12), fill="#A0AAB5", anchor="nw")
        
        # Top Strip Focus Bar Panel Controls
        self.top_pixel = Image.new("RGBA", (1, 1), (30, 34, 43, 160))
        self.top_photo = ImageTk.PhotoImage(self.top_pixel.resize((760, 65)))
        self.main_canvas.create_image(220, 0, image=self.top_photo, anchor="nw")
        self.main_canvas.create_line(220, 65, 980, 65, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(250, 32, text="Focus Minutes:", font=("Arial", 12, "bold"), fill="white", anchor="w")
        
        # Timer Entry Input field
        self.mins_entry = tk.Entry(self, font=("Arial", 12, "bold"), fg="white", bg="#0F1219", bd=1, relief="solid", justify="center", insertbackground="white")
        self.mins_entry.insert(0, "25")
        self.main_canvas.create_window(420, 32, window=self.mins_entry, width=60, height=28)
        
        # Start button
        btn = tk.Button(self, text="Start ⚡", font=("Arial", 11, "bold"), fg="white", bg="#FF69B4", activebackground="#FF1493", bd=0, command=self.go_to_timer)
        self.main_canvas.create_window(545, 32, window=btn, width=110, height=28)
        
        monitor_btn = tk.Button(
            self,
            text="Open Monitoring",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#496B50",
            bd=0,
            command=self.open_monitoring
        )

        self.main_canvas.create_window(
            735, 32,
            window=monitor_btn,
            width=140,
            height=28
        )
                # Webcam display area inside OASIS workspace
        self.camera_label = tk.Label(
            self,
            text="Webcam feed will appear here",
            bg="#0F1219",
            fg="white",
            font=("Arial", 12)
        )

        self.main_canvas.create_window(
            600, 360,
            window=self.camera_label,
            width=600,
            height=400
        )
        
        # Monitoring variables
        self.camera = None
        self.detector = None
        self.timer = None
        self.database = None

        self.saved_for_this_run = False
        self.session_completed = False
        self.last_closure_alerted = False

        self.camera_image = None

        self.protocol("WM_DELETE_WINDOW", self.close_workspace)
        
        # Monitoring controls
        self.start_btn = tk.Button(
            self, text="Start / Resume",
            command=self.start_focus,
            bg="#496B50", fg="white"
        )
        self.main_canvas.create_window(
            350, 590, window=self.start_btn, width=120, height=32
        )

        self.pause_btn = tk.Button(
            self, text="Pause",
            command=self.pause_focus,
            bg="#555B70", fg="white"
        )
        self.main_canvas.create_window(
            490, 590, window=self.pause_btn, width=80, height=32
        )

        self.break_btn = tk.Button(
            self, text="Take Break",
            command=self.begin_focus_break,
            bg="#496B50", fg="white"
        )
        self.main_canvas.create_window(
            590, 590, window=self.break_btn, width=100, height=32
        )

        self.reset_btn = tk.Button(
            self, text="Reset",
            command=self.reset_focus,
            bg="#555B70", fg="white"
        )
        self.main_canvas.create_window(
            700, 590, window=self.reset_btn, width=80, height=32
        )

        self.stop_btn = tk.Button(
            self, text="Stop Monitoring",
            command=self.stop_monitoring,
            bg="#9B4141", fg="white"
        )
        self.main_canvas.create_window(
            830, 590, window=self.stop_btn, width=130, height=32
        )

    
    def go_to_timer(self):
        try:
            mins = int(self.mins_entry.get())
            if mins <= 0:
                print("Please enter a positive number of minutes.")
                return
        except ValueError:
            print("Please enter a valid number of minutes.")
            return

        self.start_focus()

        if self.timer is None:
            return

        self.timer.session_seconds = mins * 60
        self.withdraw()

        countdown_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "countdown_screen.py"
        )

        try:
            self.countdown_process = subprocess.Popen(
                [sys.executable, countdown_path, str(mins)]
            )
            self.check_countdown_process()
        except Exception as e:
            self.deiconify()
            print("Could not open focus screen:", e)

    def check_countdown_process(self):
        if self.countdown_process.poll() is None:
            self.after(250, self.check_countdown_process)
        else:
            self.countdown_process = None
            self.deiconify()




        
    
    def open_monitoring(self):
        if self.camera is not None:
            return

        try:
            self.database = SessionDatabase()
            self.detector = BlinkDetector()
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not self.camera.isOpened():
                self.camera.release()
                self.camera = None
                self.detector.close()
                self.detector = None
                self.camera_label.config(
                    text="Cannot access webcam. Check camera permissions."
                )
                return

            self.timer = FocusTimer()
            self.saved_for_this_run = False
            self.session_completed = False
            self.last_closure_alerted = False

            self.camera_label.config(text="")
            self.update_camera()

        except Exception as e:
            print("Monitoring error:", e)
            self.stop_monitoring()

    def update_camera(self):
        if self.camera is None or not self.camera.isOpened():
            return

        success, frame = self.camera.read()

        if not success:
            self.camera_label.config(text="Cannot read from webcam.")
            self.after(100, self.update_camera)
            return

        self.detector.detect(frame)
        elapsed = self.timer.elapsed()

        if self.detector.prolonged_closure and not self.last_closure_alerted:
            play_alert()
            self.last_closure_alerted = True
        elif not self.detector.prolonged_closure:
            self.last_closure_alerted = False

        if (
            self.timer.running
            and self.timer.is_session_complete()
            and not self.timer.break_alerted
        ):
            self.timer.pause()
            self.timer.break_alerted = True
            self.session_completed = True
            play_alert()

        draw_text(frame, f"Blinks: {self.detector.blink_count}", (20, 35), (0, 255, 0))
        draw_text(
            frame,
            f"Recent blinks/min: {self.detector.get_recent_blink_rate()}",
            (20, 65),
        )
        draw_text(frame, f"Focus time: {format_time(elapsed)}", (20, 95))
        draw_text(
            frame,
            f"Session goal: {format_time(self.timer.session_seconds)}",
            (20, 125),
        )

        if not self.detector.face_detected:
            message, color = "Face not detected - adjust camera", (0, 165, 255)
        elif self.detector.prolonged_closure:
            message, color = "Possible fatigue cue - consider a break", (0, 0, 255)
        elif self.timer.on_break:
            message, color = "Break time - press Resume", (255, 200, 0)
        elif self.session_completed:
            message, color = "Session goal reached - take a break", (0, 200, 255)
        elif self.timer.running:
            message, color = "Focus session running", (0, 255, 0)
        else:
            message, color = "Paused - press Start / Resume", (0, 200, 255)

        draw_text(frame, message, (20, 165), color, 0.58)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (600, 400))
        self.camera_image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.camera_label.config(image=self.camera_image, text="")

        self.after(15, self.update_camera)

    def start_focus(self):
        if self.timer is None:
            self.open_monitoring()

        if self.timer is None:
            return

        if self.timer.on_break:
            self.timer.resume_after_break()
        else:
            self.timer.start()

        self.session_completed = False

    def pause_focus(self):
        if self.timer is not None:
            self.timer.pause()

    def reset_focus(self):
        if self.timer is not None:
            self.timer.reset()
            self.detector.blink_count = 0
            self.detector.prolonged_closure_events = 0
            self.detector.blink_timestamps.clear()
            self.last_closure_alerted = False
            self.session_completed = False
            self.saved_for_this_run = False

    def begin_focus_break(self):
        if self.timer is not None:
            self.timer.begin_break()
            play_alert()

    def stop_monitoring(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

        if (
            self.timer is not None
            and self.timer.started_at_text is not None
            and not self.saved_for_this_run
        ):
            self.database.save_session(
                self.timer.started_at_text,
                self.timer.elapsed(),
                self.detector.blink_count,
                self.detector.prolonged_closure_events,
                self.session_completed,
            )
            self.saved_for_this_run = True
            print(f"Session summary saved to {DATABASE_FILE}")

        if self.detector is not None:
            self.detector.close()
            self.detector = None

        self.timer = None
        self.camera_label.config(image="", text="Monitoring stopped")
        self.camera_image = None

    def close_workspace(self):
        self.stop_monitoring()
        self.destroy()



if __name__ == "__main__":
    app = OasisWorkspaceOnly()
    app.mainloop()

