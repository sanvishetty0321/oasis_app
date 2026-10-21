import customtkinter as ctk

# Set up clean dark-mode base layers
ctk.set_appearance_mode("dark")

class OasisInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OASIS - Premium Desktop Interface Engine")
        self.geometry("980x680")
        self.configure(fg_color="#0F1219")  # Luxurious midnight black canvas
        
        # Grid layout for elegant proportions
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ---------------------------------------------------------
        # 1. LUXURIOUS PINK SIDEBAR NAV PANEL
        # ---------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#141923")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        # Premium Styled Custom Pink Logo Header Block
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Oasis", 
            font=("Georgia", 36, "italic"), 
            text_color="#FF69B4"  # Vibrant Premium Pink Accent Brand Color
        )
        self.logo_label.pack(pady=(35, 25), padx=20)
        
        # Premium High-Contrast Sidebar Menu Action Items
        self.btn_home = ctk.CTkButton(
            self.sidebar_frame, text="📊 Home Dashboard", font=("Arial", 14, "bold"),
            fg_color="#FF69B4", text_color="white", hover_color="#FF1493",
            anchor="w", height=42, corner_radius=8, command=self.show_home
        )
        self.btn_home.pack(fill="x", padx=15, pady=6)
        
        self.btn_tasks = ctk.CTkButton(
            self.sidebar_frame, text="📋 To-Do List Task Board", font=("Arial", 14),
            fg_color="transparent", text_color="#A0AAB5", hover_color="#202836",
            anchor="w", height=42, corner_radius=8, command=self.show_tasks
        )
        self.btn_tasks.pack(fill="x", padx=15, pady=6)
        
        self.btn_settings = ctk.CTkButton(
            self.sidebar_frame, text="⚙️ Settings & Alerts", font=("Arial", 14),
            fg_color="transparent", text_color="#A0AAB5", hover_color="#202836",
            anchor="w", height=42, corner_radius=8, command=self.show_settings
        )
        self.btn_settings.pack(fill="x", padx=15, pady=6)
        
        # Real-time Hardware Analytics Monitor Dock
        self.status_box = ctk.CTkFrame(self.sidebar_frame, fg_color="#1B2230", corner_radius=10)
        self.status_box.pack(side="bottom", fill="x", padx=15, pady=30)
        
        ctk.CTkLabel(self.status_box, text="LIVE CAM HARDWARE METRICS", font=("Arial", 11, "bold"), text_color="#627280").pack(pady=(12,6))
        self.posture_lbl = ctk.CTkLabel(self.status_box, text="Posture: ✅ Good Position", font=("Arial", 13), text_color="#2ECC71")
        self.posture_lbl.pack(anchor="w", padx=15, pady=2)
        self.focus_lbl = ctk.CTkLabel(self.status_box, text="Status: 🎯 High Focus", font=("Arial", 13), text_color="#FF69B4")
        self.focus_lbl.pack(anchor="w", padx=15, pady=(2,12))

        # ---------------------------------------------------------
        # MAIN MULTI-VIEW WORKSPACE STAGE
        # ---------------------------------------------------------
        self.stage_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stage_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        
        self.init_home_view()
        self.init_tasks_view()
        self.init_settings_view()
        
        self.show_home()

    # ---------------------------------------------------------
    # LAYOUT 1: RE-ENGINEERED LUSH HOME DASHBOARD
    # ---------------------------------------------------------
    def init_home_view(self):
        self.home_frame = ctk.CTkFrame(self.stage_frame, fg_color="transparent")
        
        # Custom Welcoming Header Block
        self.greeting = ctk.CTkLabel(self.home_frame, text="Welcome Back, Sanvi", font=("Georgia", 28, "bold"), text_color="#FF69B4")
        self.greeting.pack(anchor="w", pady=(5,2))
        
        self.sub_g = ctk.CTkLabel(self.home_frame, text="Your active tracking session is active.", font=("Arial", 13), text_color="#627280")
        self.sub_g.pack(anchor="w", pady=(0,15))
        
        # Premium Performance Metrics Row
        stats_row = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        stats_row.pack(fill="x", pady=5)
        
        c1 = ctk.CTkFrame(stats_row, height=85, fg_color="#141923", corner_radius=12); c1.pack(side="left", expand=True, fill="both", padx=(0,12))
        ctk.CTkLabel(c1, text="Total Active Focus Time", font=("Arial", 12, "bold"), text_color="#627280").pack(pady=(12,2))
        ctk.CTkLabel(c1, text="2.5 Hours", font=("Arial", 22, "bold"), text_color="white").pack()
        
        c2 = ctk.CTkFrame(stats_row, height=85, fg_color="#141923", corner_radius=12); c2.pack(side="left", expand=True, fill="both", padx=12)
        ctk.CTkLabel(c2, text="Completed Milestone Goals", font=("Arial", 12, "bold"), text_color="#627280").pack(pady=(12,2))
        ctk.CTkLabel(c2, text="4 Tasks", font=("Arial", 22, "bold"), text_color="#FF69B4").pack()

        # 🪐 MASSIVE IMMERSIVE PLANT ECOSYSTEM BOX
        self.garden_box = ctk.CTkFrame(self.home_frame, fg_color="#141923", corner_radius=16, border_width=1, border_color="#202836")
        self.garden_box.pack(fill="both", expand=True, pady=15)
        
        # Animated Emojis Cluster representing your rich garden mix
        self.plant_render = ctk.CTkLabel(
            self.garden_box, 
            text="🌹 🌻 🌿 🪵 🌸 🌿 🌹\n\n[ DIGITAL TERRARIUM ECOSYSTEM ACTIVE ]\n\nYour Exotic Roses, Sunflowers, and Lavender are blooming beautifully.", 
            font=("Georgia", 16, "italic"), 
            text_color="#BDC3C7"
        )
        self.plant_render.pack(expand=True)
        
        # Active Trigger simulation item
        ctk.CTkButton(self.home_frame, text="Simulate Camera Slouch Detection Alert", fg_color="#C0392B", hover_color="#A93226", height=38, corner_radius=8, command=self.trigger_frosted_modal).pack(pady=5)

    # ---------------------------------------------------------
    # LAYOUT 2: TO-DO LIST TASK BOARD SYSTEM
    # ---------------------------------------------------------
    def init_tasks_view(self):
        self.tasks_frame = ctk.CTkFrame(self.stage_frame, fg_color="transparent")
        ctk.CTkLabel(self.tasks_frame, text="📋 To-Do List Task Board", font=("Arial", 24, "bold"), text_color="white").pack(anchor="w", pady=(10,15))
        
        input_row = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        input_row.pack(fill="x", pady=5)
        
        self.task_entry = ctk.CTkEntry(input_row, placeholder_text="Type a new focus milestone...", fg_color="#141923", border_color="#202836", height=38)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0,12))
        
        ctk.CTkButton(input_row, text="Add Goal", width=110, height=38, fg_color="#FF69B4", hover_color="#FF1493", font=("Arial", 13, "bold"), command=self.append_new_task).pack(side="right")
        
        self.task_scrollbox = ctk.CTkScrollableFrame(self.tasks_frame, fg_color="#141923", corner_radius=12, border_width=1, border_color="#202836")
        self.task_scrollbox.pack(fill="both", expand=True, pady=15)

    def append_new_task(self):
        val = self.task_entry.get()
        if val:
            row = ctk.CTkFrame(self.task_scrollbox, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkCheckBox(row, text=val, font=("Arial", 14), text_color="white", fg_color="#FF69B4", hover_color="#FF1493").pack(side="left", padx=5)
            self.task_entry.delete(0, 'end')

    # ---------------------------------------------------------
    # LAYOUT 3: SYSTEM HARDWARE PREFERENCES
    # ---------------------------------------------------------
    def init_settings_view(self):
        self.settings_frame = ctk.CTkFrame(self.stage_frame, fg_color="transparent")
        ctk.CTkLabel(self.settings_frame, text="⚙️ Settings & Alerts", font=("Arial", 24, "bold"), text_color="white").pack(anchor="w", pady=(10, 15))
        
        # Hardware Integration Preferences Card
        config_box = ctk.CTkFrame(self.settings_frame, fg_color="#141923", corner_radius=12, border_width=1, border_color="#202836")
        config_box.pack(fill="x", pady=10, padx=2)
        
        ctk.CTkLabel(config_box, text="HARDWARE & CAMERA MONITORING", font=("Arial", 14, "bold"), text_color="#FF69B4").pack(anchor="w", padx=20, pady=(15, 10))
        
        cam_switch = ctk.CTkSwitch(config_box, text="Enable Camera AI Posture Tracking", font=("Arial", 13), fg_color="#202836", progress_color="#FF69B4")
        cam_switch.pack(anchor="w", padx=20, pady=8)
        cam_switch.select()
        
        alert_switch = ctk.CTkSwitch(config_box, text="Send Real-Time Slouch Haptic Alerts", font=("Arial", 13), fg_color="#202836", progress_color="#FF69B4")
        alert_switch.pack(anchor="w", padx=20, pady=(8, 20))
        alert_switch.select()

    # ---------------------------------------------------------
    # NAVIGATION AND MODAL VIEW CONTROLLERS
    # ---------------------------------------------------------
    def clean_workspace(self):
        self.home_frame.pack_forget()
        self.tasks_frame.pack_forget()
        self.settings_frame.pack_forget()
        
        # Reset Nav Button Highlights to Unselected Slate Style
        for btn in [self.btn_home, self.btn_tasks, self.btn_settings]:
            btn.configure(fg_color="transparent", text_color="#A0AAB5", font=("Arial", 14))

    def show_home(self):
        self.clean_workspace()
        self.btn_home.configure(fg_color="#FF69B4", text_color="white", font=("Arial", 14, "bold"))
        self.home_frame.pack(fill="both", expand=True)


