import os
import customtkinter as ctk
from PIL import Image, ImageTk

# Set up clean dark-mode base layers
ctk.set_appearance_mode("dark")

class OasisEngine(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OASIS - Premium Desktop Interface Engine")
        self.geometry("980x680")
        self.configure(fg_color="#0F1219")  # Midnight canvas
        
        # Base application grid layout matching master proportions
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Core data tracking metrics states
        self.user_name = "Sanvi"
        self.gif_frames = []
        self.current_frame = 0
        self.playlist_index = 0
        
        # Timer tracking state engines
        self.total_seconds_left = 0
        self.timer_running = False
        
        # Thread loop ID managers to safely clear loops when switching screens
        self.animation_loop_id = None
        self.playlist_loop_id = None
        self.countdown_loop_id = None
        
        # Start directly on Screen 1: Login Canvas View
        self.init_login_screen()

    # ---------------------------------------------------------
    # UTILITY: BACKEND VISION TEAM INTEGRATION GATEWAY
    # ---------------------------------------------------------
    def trigger_vision_drowsy_alert(self):
        """
        GATEWAY FOR YOUR TEAMMATE: 
        Your vision processing team can call this exact function from their code 
        when their camera scripts detect closed eyes or heavy slouching!
        """
        if self.playlist_loop_id:
            self.after_cancel(self.playlist_loop_id)
            self.playlist_loop_id = None
        self.timer_running = False
        if self.countdown_loop_id:
            self.after_cancel(self.countdown_loop_id)
            self.countdown_loop_id = None
            
        self.kill_active_animation_loops()
        
        try: self.home_view.pack_forget()
        except Exception: pass
        try: self.todo_view.pack_forget()
        except Exception: pass
        try: self.focus_fullscreen_frame.destroy()
        except Exception: pass
        
        self.sidebar.grid_forget()
        self.stage.grid_forget()
        
        self.alert_frame = ctk.CTkFrame(self, fg_color="#0F1219")
        self.alert_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.alert_media_render = ctk.CTkLabel(self.alert_frame, text="")
        self.alert_media_render.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.load_and_play_gif("tenor23.gif", self.alert_media_render, (980, 680))
        self.after(3500, self.engage_storm_alert_phase)

    def engage_storm_alert_phase(self):
        if hasattr(self, 'alert_media_render') and self.alert_frame.winfo_exists():
            self.load_and_play_gif("tenor6.gif", self.alert_media_render, (980, 680))
            
            # Frosted glass pop-up card box
            popup_card = ctk.CTkFrame(self.alert_frame, width=440, height=240, fg_color="rgba(30, 15, 25, 0.55)", corner_radius=16, border_width=1, border_color="rgba(231, 76, 60, 0.4)")
            popup_card.place(relx=0.5, rely=0.5, anchor="center")
            popup_card.pack_propagate(False)
            
            ctk.CTkLabel(popup_card, text="🚨 Fatigue Detected!", font=("Arial", 22, "bold"), text_color="#E74C3C").pack(pady=(25, 10))
            ctk.CTkLabel(popup_card, text="You look a little sleepy! Stand up, stretch, move around a bit, and let's get your focus mode back.", font=("Arial", 14), text_color="#ECF0F1", justify="center", wraplength=380).pack(pady=10)
            
            ctk.CTkButton(popup_card, text="Acknowledge & Clear", font=("Arial", 13, "bold"), fg_color="#C0392B", hover_color="#A93226", width=200, height=38, corner_radius=8, command=self.clear_vision_alert_system).pack(side="bottom", pady=20)

    def clear_vision_alert_system(self):
        self.kill_active_animation_loops()
        self.alert_frame.destroy()
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.stage.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.show_home_view()

    # ---------------------------------------------------------
    # SCREEN 1: LOGIN FRAMEWORK
    # ---------------------------------------------------------
    def init_login_screen(self):
        self.login_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
        self.bg_label = ctk.CTkLabel(self.login_frame, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        login_asset = None
        for ext in [".gif", ".png", ".jpg", ".jpeg"]:
            if os.path.exists(f"login{ext}"):
                login_asset = f"login{ext}"
                break
                
        if login_asset:
            try:
                raw_bg = Image.open(login_asset)
                self.bg_img = ImageTk.PhotoImage(raw_bg.resize((980, 680), Image.Resampling.LANCZOS))
                self.bg_label.configure(image=self.bg_img)
            except Exception:
                self.login_frame.configure(fg_color="#141923")
        else:
            self.login_frame.configure(fg_color="#141923")
            
        # Relocated slightly upward (rely=0.42 instead of 0.5) and applied a frosted glass style (0.45 opacity)
        login_card = ctk.CTkFrame(self.login_frame, width=380, height=300, fg_color="rgba(20, 25, 35, 0.45)", corner_radius=16, border_width=1, border_color="rgba(255, 255, 255, 0.15)")
        login_card.place(relx=0.5, rely=0.42, anchor="center")
        login_card.pack_propagate(False)
        
        ctk.CTkLabel(login_card, text="OASIS", font=("Georgia", 34, "italic", "bold"), text_color="#FF69B4").pack(pady=(35, 10))
        ctk.CTkLabel(login_card, text="Enter your name to unlock alignment", font=("Arial", 12), text_color="#A0AAB5").pack(pady=(0, 20))
        
        self.name_entry = ctk.CTkEntry(login_card, placeholder_text="Your Name...", width=260, height=40, fg_color="#0F1219", border_color="#202836", text_color="white")
        self.name_entry.pack(pady=10)
        self.name_entry.bind("<Return>", lambda e: self.process_login())
        
        ctk.CTkButton(login_card, text="Enter Workspace →", font=("Arial", 13, "bold"), fg_color="#FF69B4", hover_color="#FF1493", width=260, height=40, corner_radius=8, command=self.process_login).pack(pady=15)

    def process_login(self):
        input_val = self.name_entry.get().strip()
        if input_val:
            self.user_name = input_val
        self.login_frame.destroy()
        self.init_main_app_workspace()

    # ---------------------------------------------------------
    # MAIN WORKSPACE BASE STRUCTURE (SIDEBAR AND WINDOW CONTROLLER)
    # ---------------------------------------------------------
    def init_main_app_workspace(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Premium Sidebar Navigation Bar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#141923")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame = self.sidebar
        self.sidebar.grid_propagate(False)
        
        ctk.CTkLabel(self.sidebar, text="Oasis", font=("Georgia", 36, "italic"), text_color="#FF69B4").pack(pady=(35, 25), padx=20)
        
        self.btn_home = ctk.CTkButton(self.sidebar, text="📊 Home Dashboard", font=("Arial", 14, "bold"), fg_color="#FF69B4", text_color="white", hover_color="#FF1493", anchor="w", height=42, corner_radius=8, command=self.show_home_view)
        self.btn_home.pack(fill="x", padx=15, pady=6)
        
        self.btn_todo = ctk.CTkButton(self.sidebar, text="📋 To-Do List Board", font=("Arial", 14), fg_color="transparent", text_color="#A0AAB5", hover_color="#202836", anchor="w", height=42, corner_radius=8, command=self.show_todo_view)
        self.btn_todo.pack(fill="x", padx=15, pady=6)
        
        simulation_box = ctk.CTkFrame(self.sidebar, fg_color="#1C2330", corner_radius=10, height=90)
        simulation_box.pack(side="bottom", fill="x", padx=15, pady=25)
        simulation_box.pack_propagate(False)
        ctk.CTkButton(simulation_box, text="Simulate Drowsiness Alert", font=("Arial", 11, "bold"), fg_color="#C0392B", hover_color="#A93226", height=32, command=self.trigger_vision_drowsy_alert).pack(expand=True, padx=10)
        
        self.stage = ctk.CTkFrame(self, fg_color="transparent")
        self.stage.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        self.build_home_view()
        self.build_todo_view()
        self.show_home_view()

    # ---------------------------------------------------------
    # SCREEN 2: HOME DASHBOARD (WITH CAT GIF & TIMER CONFIG)
    # ---------------------------------------------------------
    def build_home_view(self):
        self.home_view = ctk.CTkFrame(self.stage, fg_color="transparent")
        
        self.lbl_welcome = ctk.CTkLabel(self.home_view, text=f"Welcome Back, {self.user_name}", font=("Georgia", 28, "bold"), text_color="#FF69B4")
        self.lbl_welcome.pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(self.home_view, text="Select your core target hours and sink into alignment.", font=("Arial", 13), text_color="#627280").pack(anchor="w", pady=(0, 15))
        
        row_content = ctk.CTkFrame(self.home_view, fg_color="transparent")
        row_content.pack(fill="both", expand=True, pady=10)
        
        # Translucent frosted design matching your blueprint
        picker_card = ctk.CTkFrame(row_content, fg_color="rgba(20, 25, 35, 0.45)", corner_radius=16, border_width=1, border_color="rgba(255, 255, 255, 0.12)")
        picker_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        


