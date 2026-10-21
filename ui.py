import os
import tkinter as tk
from PIL import Image, ImageTk

class OasisDiagnosticApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window Settings
        self.title("OASIS - System Diagnostics Portal")
        self.geometry("980x680")
        self.configure(bg="#0F1219")  
        self.resizable(False, False)
        
        # State Trackers
        self.current_screen = "login"
        self.entered_name = ""
        self.cursor_visible = True
        self.blink_job = None  
        self.assets = {}  
        
        # Base Canvas
        self.main_canvas = tk.Canvas(self, width=980, height=680, bd=0, highlightthickness=0, bg="#0F1219")
        self.main_canvas.pack(fill="both", expand=True)
        
        # Load Background File
        login_asset = "login.jpg"
        if not os.path.exists(login_asset):
            for ext in [".jpeg", ".png", ".PNG", ".jpg"]:
                if os.path.exists(f"login{ext}"):
                    login_asset = f"login{ext}"
                    break
                    
        if os.path.exists(login_asset):
            try:
                raw_image = Image.open(login_asset)
                resized_image = raw_image.resize((980, 680), Image.Resampling.LANCZOS)
                self.assets["bg_img"] = ImageTk.PhotoImage(resized_image)
                self.bg_image_id = self.main_canvas.create_image(0, 0, image=self.assets["bg_img"], anchor="nw")
                print(f"👉 SYSTEM LOG: Found and loaded background image: {login_asset}")
            except Exception as e:
                print(f"❌ SYSTEM ERROR Loading Image: {e}")
        else:
            self.bg_image_id = None
            print("⚠️ SYSTEM LOG: No 'login.jpg' image found. Using default dark background.")

        self.render_login_screen()

    def render_login_screen(self):
        self.current_screen = "login"
        
        # Draw Interface Box
        overlay_pixel = Image.new("RGBA", (1, 1), (30, 34, 43, 140)) 
        self.assets["login_card"] = ImageTk.PhotoImage(overlay_pixel.resize((380, 300)))
        card_x, card_y = 490, 238
        
        self.main_canvas.create_image(card_x, card_y, image=self.assets["login_card"], anchor="center")
        self.main_canvas.create_rectangle(card_x-190, card_y-150, card_x+190, card_y+150, outline="#2C323F", width=1)
        
        self.main_canvas.create_text(card_x, card_y-95, text="OASIS", font=("Georgia", 32, "italic", "bold"), fill="#FF69B4", anchor="center")
        self.main_canvas.create_text(card_x, card_y-45, text="Enter your name", font=("Arial", 12), fill="#A0AAB5", anchor="center")
        
        # Input Text Properties
        self.main_canvas.create_rectangle(card_x-130, card_y-3, card_x+130, card_y+33, fill="#0F1219", outline="#2C323F", width=1)
        self.display_text_id = self.main_canvas.create_text(card_x, card_y+15, text=self.entered_name, font=("Arial", 13), fill="white", anchor="center")
        self.cursor_id = self.main_canvas.create_line(card_x, card_y+4, card_x, card_y+26, fill="white", width=2)
        
        # Login Button UI
        self.login_btn_bg = self.main_canvas.create_rectangle(card_x-110, card_y+56, card_x+110, card_y+94, fill="#FF69B4", outline="", width=0)
        self.login_btn_txt = self.main_canvas.create_text(card_x, card_y+75, text="Enter Workspace →", font=("Arial", 12, "bold"), fill="white", anchor="center")
        
        # Event Listeners
        self.bind("<Key>", self.handle_login_keypress)
        self.bind("<BackSpace>", self.handle_login_backspace)
        
        # Action Triggers wrapped inside safe validation routes
        self.main_canvas.tag_bind(self.login_btn_bg, "<Button-1>", self.safe_switch_trigger)
        self.main_canvas.tag_bind(self.login_btn_txt, "<Button-1>", self.safe_switch_trigger)
        
        self.update_login_input_ui()
        self.start_cursor_blink()

    def handle_login_keypress(self, event):
        if len(event.char) == 1 and ord(event.char) >= 32:
            if len(self.entered_name) < 24:
                self.entered_name += event.char
                self.update_login_input_ui()

    def handle_login_backspace(self, event):
        self.entered_name = self.entered_name[:-1]
        self.update_login_input_ui()

    def update_login_input_ui(self):
        self.main_canvas.itemconfig(self.display_text_id, text=self.entered_name)
        bbox = self.main_canvas.bbox(self.display_text_id)
        if bbox and self.entered_name:
            text_width = bbox - bbox
            cursor_x = 490 + (text_width // 2) + 4
        else:
            cursor_x = 490
        self.main_canvas.coords(self.cursor_id, cursor_x, 238+4, cursor_x, 238+26)

    def start_cursor_blink(self):
        if self.current_screen == "login":
            self.cursor_visible = not self.cursor_visible
            state = "normal" if self.cursor_visible else "hidden"
            try:
                self.main_canvas.itemconfig(self.cursor_id, state=state)
            except:
                return
            self.blink_job = self.after(500, self.start_cursor_blink)

    def safe_switch_trigger(self, event=None):
        """CRITICAL WATCHDOG: Captures hidden runtime bugs preventing transitions."""
        print("👉 SYSTEM LOG: Enter Workspace button clicked! Attempting transition...")
        try:
            self.switch_to_workspace()
        except Exception as crash_error:
            print("\n❌ ❌ CRITICAL WORKSPACE CRASH DETECTED ❌ ❌")
            print(f"Error Type: {type(crash_error).__name__}")
            print(f"Error Message Details: {crash_error}\n")

    def switch_to_workspace(self):
        self.current_screen = "workspace"
        
        # Stop typing blinker
        if self.blink_job:
            self.after_cancel(self.blink_job)
            self.blink_job = None
            
        # Clean up login box widgets safely
        for item in self.main_canvas.find_all():
            if item != self.bg_image_id:
                self.main_canvas.delete(item)
        self.unbind("<Key>")
        self.unbind("<BackSpace>")
        
        # Keep background at base
        if self.bg_image_id:
            self.main_canvas.tag_lower(self.bg_image_id)
            
        # Draw Side Navbar
        sidebar_pixel = Image.new("RGBA", (1, 1), (20, 24, 33, 215)) 
        self.assets["sidebar_bg"] = ImageTk.PhotoImage(sidebar_pixel.resize((220, 680)))
        self.main_canvas.create_image(0, 0, image=self.assets["sidebar_bg"], anchor="nw")
        self.main_canvas.create_line(220, 0, 220, 680, fill="#2C323F", width=1)
        
        self.main_canvas.create_text(110, 45, text="OASIS", font=("Georgia", 24, "italic", "bold"), fill="#FF69B4", anchor="center")
        self.main_canvas.create_text(35, 130, text="🏠 Home", font=("Arial", 12, "bold"), fill="white", anchor="nw")
        self.main_canvas.create_text(35, 185, text="📋 To-Do List", font=("Arial", 12), fill="#A0AAB5", anchor="nw")
        
        # Draw Top Timer Strip Bar
        top_strip_pixel = Image.new("RGBA", (1, 1), (30, 34, 43, 160))
        self.assets["top_bar_bg"] = ImageTk.PhotoImage(top_strip_pixel.resize((760, 65)))
        self.main_canvas.create_image(220, 0, image=self.assets["top_bar_bg"], anchor="nw")
        self.main_canvas.create_line(220, 65, 980, 65, fill="#2C323F", width=1)
        
        start_x = 250
        y_center = 32
        
        self.main_canvas.create_text(start_x, y_center, text="Focus Timer:", font=("Arial", 12, "bold"), fill="white", anchor="w")
        
        # Draw Native OS Selection Dropdowns
        self.hours_var = tk.StringVar(self)
        self.hours_var.set("00")
        self.mins_var = tk.StringVar(self)
        self.mins_var.set("25")
        
        hours_menu = tk.OptionMenu(self, self.hours_var, *[f"{i:02d}" for i in range(13)])
        mins_menu = tk.OptionMenu(self, self.mins_var, *[f"{i:02d}" for i in range(0, 60, 5)])
        
        for menu in (hours_menu, mins_menu):
            menu.config(bg="#0F1219", fg="white", activebackground="#2C323F", activeforeground="white", highlightthickness=1, highlightbackground="#2C323F", bd=0, indicatoron=0)
            menu["menu"].config(bg="#0F1219", fg="white", selectcolor="#FF69B4", activebackground="#2C323F")
            
        self.main_canvas.create_window(start_x + 115, y_center, window=hours_menu, width=50, height=28, anchor="w")
        self.main_canvas.create_window(start_x + 195, y_center, window=mins_menu, width=50, height=28, anchor="w")
        
        # Top Small Rectangular Start Button
        btn_start_x = start_x + 290
        self.main_canvas.create_rectangle(btn_start_x, y_center-14, btn_start_x+110, y_center+14, fill="#FF69B4", outline="", width=0)
        self.main_canvas.create_text(btn_start_x+55, y_center, text="Start ⚡", font=("Arial", 11, "bold"), fill="white", anchor="center")
        
        print("👉 SYSTEM LOG: Successfully switched to workspace hub view window frame layout!")

if __name__ == "__main__":
    app = OasisDiagnosticApp()
    app.mainloop()
