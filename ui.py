import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class OasisInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OASIS - Interactive Desktop Dashboard")
        self.geometry("950x650")
        
        # Grid layout for Sidebar (col 0) and Main Content Space (col 1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ---------------------------------------------------------
        # 1. SIDEBAR NAVIGATION & LIVE DATA DISPLAY
        # ---------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OASIS", font=("Arial", 26, "bold"), text_color="#2ECC71")
        self.logo_label.pack(pady=30, padx=20)
        
        # Menu Buttons
        self.btn_home = ctk.CTkButton(self.sidebar_frame, text="📊 Home Dashboard", fg_color="transparent", text_color="white", anchor="w", command=self.show_home)
        self.btn_home.pack(fill="x", padx=10, pady=5)
        
        self.btn_tasks = ctk.CTkButton(self.sidebar_frame, text="📋 Task Manager", fg_color="transparent", text_color="white", anchor="w", command=self.show_tasks)
        self.btn_tasks.pack(fill="x", padx=10, pady=5)
        
        self.btn_settings = ctk.CTkButton(self.sidebar_frame, text="⚙️ Settings & Alerts", fg_color="transparent", text_color="white", anchor="w", command=self.show_settings)
        self.btn_settings.pack(fill="x", padx=10, pady=5)
        
        # Real-time Hardware Tracking Monitor Box
        self.status_box = ctk.CTkFrame(self.sidebar_frame, fg_color="#1E272C")
        self.status_box.pack(side="bottom", fill="x", padx=15, pady=30)
        
        ctk.CTkLabel(self.status_box, text="LIVE CAM CAMERA METRICS", font=("Arial", 11, "bold"), text_color="#7F8C8D").pack(pady=(10,5))
        self.posture_lbl = ctk.CTkLabel(self.status_box, text="Posture: ✅ Good", font=("Arial", 13))
        self.posture_lbl.pack(anchor="w", padx=15, pady=2)
        self.eye_lbl = ctk.CTkLabel(self.status_box, text="Eye Activity: 👁️ Active", font=("Arial", 13))
        self.eye_lbl.pack(anchor="w", padx=15, pady=2)
        self.focus_lbl = ctk.CTkLabel(self.status_box, text="Status: 🎯 Focused", font=("Arial", 13))
        self.focus_lbl.pack(anchor="w", padx=15, pady=(2,10))

        # ---------------------------------------------------------
        # MAIN MULTI-VIEW ENGINE CONTAINER
        # ---------------------------------------------------------
        self.stage_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stage_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.init_home_view()
        self.init_tasks_view()
        self.init_settings_view()
        
        self.show_home() # Start on home dashboard layout

    # ---------------------------------------------------------
    # LAYOUT 1: HOME DASHBOARD (Session Summaries & Stats)
    # ---------------------------------------------------------
    def init_home_view(self):
        self.home_frame = ctk.CTkFrame(self.stage_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.home_frame, text="Productivity Dashboard", font=("Arial", 26, "bold")).pack(anchor="w", pady=(10,20))
        
        # Stat Display Row
        stats_row = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        stats_row.pack(fill="x", pady=10)
        
        c1 = ctk.CTkFrame(stats_row, height=90); c1.pack(side="left", expand=True, fill="both", padx=(0,10))
        ctk.CTkLabel(c1, text="Total Focus Time", font=("Arial", 12), text_color="#95A5A6").pack(pady=(10,2))
        ctk.CTkLabel(c1, text="2.5 Hours", font=("Arial", 20, "bold")).pack()
        
        c2 = ctk.CTkFrame(stats_row, height=90); c2.pack(side="left", expand=True, fill="both", padx=10)
        ctk.CTkLabel(c2, text="Completed Goals", font=("Arial", 12), text_color="#95A5A6").pack(pady=(10,2))
        ctk.CTkLabel(c2, text="4 Tasks", font=("Arial", 20, "bold"), text_color="#2ECC71").pack()

        # The Ecosystem Core Display box
        self.garden_box = ctk.CTkFrame(self.home_frame, fg_color="#1E272C")
        self.garden_box.pack(fill="both", expand=True, pady=20)
        ctk.CTkLabel(self.garden_box, text="🌱\nYour Digital Terrarium Ecosystem is Blooming", font=("Arial", 18)).pack(expand=True)
        
        # Prototype Interactive Testing trigger
        ctk.CTkButton(self.home_frame, text="Simulate Slouch Detection Event", fg_color="#C0392B", hover_color="#962D22", command=self.trigger_frosted_modal).pack(pady=5)

    # ---------------------------------------------------------
    # LAYOUT 2: TASK MANAGEMENT SYSTEM
    # ---------------------------------------------------------
    def init_tasks_view(self):
        self.tasks_frame = ctk.CTkFrame(self.stage_frame, fg_color="transparent")
        ctk.CTkLabel(self.tasks_frame, text="Focus Session Task Board", font=("Arial", 24, "bold")).pack(anchor="w", pady=(10,20))
        
        input_row = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        input_row.pack(fill="x", pady=5)
        
        self.task_entry = ctk.CTkEntry(input_row, placeholder_text="Add a new milestone goal...")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(input_row, text="Create Task", width=100, command=self.append_new_task).pack(side="right")
        
        self.task_scrollbox = ctk.CTkScrollableFrame(self.tasks_frame, fg_color="#1E272C")
        self.task_scrollbox.pack(fill="both", expand=True, pady=15)

    def append_new_task(self):
        val = self.task_entry.get()
        if val:
            row = ctk.CTkFrame(self.task_scrollbox, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkCheckBox(row, text=val, font=("Arial", 14)).pack(side="left", padx=5)
            self.task_entry.delete(0, 'end')

    # ---------------------------------------------------------
    # LAYOUT 3: CONFIGURATION SETTNGS & NOTIFICATIONS
    # ---------------------------------------------------------
    def init_settings_view(self):
        self.settings_frame = ctk.CTkFrame(self.stage_frame, fg_color="transparent")
        ctk.CTkLabel(self.settings_frame, text="App Preferences & Calibration", font=("Arial", 24, "bold")).pack(anchor="w", pady=(10,20))
        
        s1 = ctk.CTkSwitch(self.settings_frame, text="Play background environmental audio loops automatically"); s1.pack(anchor="w", pady=12); s1.select()
        s2 = ctk.CTkSwitch(self.settings_frame, text="Enable instant OS desktop flash banner alerts"); s2.pack(anchor="w", pady=12)
        
        ctk.CTkLabel(self.settings_frame, text="Computer Vision Sensor Sensitivity Threshold", font=("Arial", 13)).pack(anchor="w", pady=(15,2))
        slider = ctk.CTkSlider(self.settings_frame, from_=0, to=100); slider.pack(fill="x", pady=5)

    # ---------------------------------------------------------
    # NAVIGATION MANAGEMENT MECHANICS
    # ---------------------------------------------------------
    def clear_stage_views(self):
        self.home_frame.pack_forget()
        self.tasks_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.btn_home.configure(fg_color="transparent")
        self.btn_tasks.configure(fg_color="transparent")
        self.btn_settings.configure(fg_color="transparent")

    def show_home(self): self.clear_stage_views(); self.btn_home.configure(fg_color="#2E4053"); self.home_frame.pack(fill="both", expand=True)
    def show_tasks(self): self.clear_stage_views(); self.btn_tasks.configure(fg_color="#2E4053"); self.tasks_frame.pack(fill="both", expand=True)
    def show_settings(self): self.clear_stage_views(); self.btn_settings.configure(fg_color="#2E4053"); self.settings_frame.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # MODALS & INTERACTIVE OVERLAYS (Stress Mode Implementation)
    # ---------------------------------------------------------
    def trigger_frosted_modal(self):
        """Generates a full-screen application layout intercept overlay"""
        self.posture_lbl.configure(text="Posture: ⚠️ Slouching", text_color="#E74C3C")
        self.focus_lbl.configure(text="Status: 🌫️ Fatigued", text_color="#E74C3C")
        
        # Full-window blocking pane simulating a frosted pane overlay
        self.modal_overlay = ctk.CTkFrame(self, fg_color="#11171A")
        self.modal_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        ctk.CTkLabel(self.modal_overlay, text="🌫️ Screen Temporarily Locked for Mental Reset", font=("Arial", 24, "bold"), text_color="#E74C3C").pack(pady=(160, 10))
        ctk.CTkLabel(self.modal_overlay, text="⭕", font=("Arial", 110)).pack(pady=15)
        ctk.CTkLabel(self.modal_overlay, text="Follow the breathing ring guide. Relax your eyes.", font=("Arial", 15), text_color="#BDC3C7").pack(pady=5)
        
        ctk.CTkButton(self.modal_overlay, text="Sit Straight (Dismiss Reset Mode)", command=self.dismiss_frosted_modal).pack(pady=40)

    def dismiss_frosted_modal(self):
        self.posture_lbl.configure(text="Posture: ✅ Good", text_color="white")
        self.focus_lbl.configure(text="Status: 🎯 Focused", text_color="white")
        self.modal_overlay.place_forget()

if __name__ == "__main__":
    app = OasisInterface()
    app.mainloop()
