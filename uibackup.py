import tkinter as tk
from tkinter import messagebox

class OasisInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("OASIS - Interactive Desktop Dashboard")
        self.geometry("950x650")
        self.configure(bg="#1A1F2C")  # Dark slate background
        
        # ---------------------------------------------------------
        # SIDEBAR PANEL NAVIGATION
        # ---------------------------------------------------------
        self.sidebar_frame = tk.Frame(self, bg="#11151E", width=220, bd=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        
        self.logo_label = tk.Label(self.sidebar_frame, text="OASIS", font=("Arial", 26, "bold"), fg="#2ECC71", bg="#11151E")
        self.logo_label.pack(pady=30)
        
        # Navigation Buttons
        self.btn_home = tk.Button(self.sidebar_frame, text="📊 Home Dashboard", font=("Arial", 13), fg="white", bg="#2E4053", relief="flat", bd=0, anchor="w", command=self.show_home)
        self.btn_home.pack(fill="x", padx=10, pady=5, ipady=5)
        
        self.btn_tasks = tk.Button(self.sidebar_frame, text="📋 Task Manager", font=("Arial", 13), fg="white", bg="#11151E", relief="flat", bd=0, anchor="w", command=self.show_tasks)
        self.btn_tasks.pack(fill="x", padx=10, pady=5, ipady=5)
        
        self.btn_settings = tk.Button(self.sidebar_frame, text="⚙️ Settings & Alerts", font=("Arial", 13), fg="white", bg="#11151E", relief="flat", bd=0, anchor="w", command=self.show_settings)
        self.btn_settings.pack(fill="x", padx=10, pady=5, ipady=5)
        
        # Real-time Status Box Monitor
        self.status_box = tk.Frame(self.sidebar_frame, bg="#1D2433", padx=10, pady=10)
        self.status_box.pack(side="bottom", fill="x", padx=15, pady=30)
        
        tk.Label(self.status_box, text="LIVE SENSOR FEED METRICS", font=("Arial", 9, "bold"), fg="#7F8C8D", bg="#1D2433").pack(pady=(0,5))
        self.posture_lbl = tk.Label(self.status_box, text="Posture:  Good", font=("Arial", 12), fg="#2ECC71", bg="#1D2433")
        self.posture_lbl.pack(anchor="w", pady=2)
        self.eye_lbl = tk.Label(self.status_box, text="Eye Activity: Active", font=("Arial", 12), fg="white", bg="#1D2433")
        self.eye_lbl.pack(anchor="w", pady=2)
        self.focus_lbl = tk.Label(self.status_box, text="Status: Focused", font=("Arial", 12), fg="white", bg="#1D2433")
        self.focus_lbl.pack(anchor="w", pady=2)

        # ---------------------------------------------------------
        # MAIN MULTI-VIEW STAGE CONTAINER
        # ---------------------------------------------------------
        self.stage_frame = tk.Frame(self, bg="#1A1F2C")
        self.stage_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        self.init_home_view()
        self.init_tasks_view()
        self.init_settings_view()
        
        self.show_home()

    # ---------------------------------------------------------
    # LAYOUT 1: HOME DASHBOARD
    # ---------------------------------------------------------
    def init_home_view(self):
        self.home_frame = tk.Frame(self.stage_frame, bg="#1A1F2C")
        
        tk.Label(self.home_frame, text="Productivity Dashboard", font=("Arial", 24, "bold"), fg="white", bg="#1A1F2C").pack(anchor="w", pady=(10,20))
        
        # Quick Statistics Grid Row
        stats_row = tk.Frame(self.home_frame, bg="#1A1F2C")
        stats_row.pack(fill="x", pady=10)
        
        c1 = tk.Frame(stats_row, bg="#252D3D", padx=20, pady=15); c1.pack(side="left", expand=True, fill="both", padx=(0,10))
        tk.Label(c1, text="Total Focus Time", font=("Arial", 11), fg="#95A5A6", bg="#252D3D").pack()
        tk.Label(c1, text="2.5 Hours", font=("Arial", 18, "bold"), fg="white", bg="#252D3D").pack(pady=5)
        
        c2 = tk.Frame(stats_row, bg="#252D3D", padx=20, pady=15); c2.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(c2, text="Completed Goals", font=("Arial", 11), fg="#95A5A6", bg="#252D3D").pack()
        tk.Label(c2, text="4 Tasks", font=("Arial", 18, "bold"), fg="#2ECC71", bg="#252D3D").pack(pady=5)

        # Main Ecosystem Visual placeholder area box
        self.garden_box = tk.Frame(self.home_frame, bg="#11151E", height=300)
        self.garden_box.pack(fill="both", expand=True, pady=20)
        self.garden_box.pack_propagate(False)
        
        tk.Label(self.garden_box, text="\nYour Digital Terrarium Ecosystem is Blooming", font=("Arial", 16), fg="#BDC3C7", bg="#11151E").pack(expand=True)
        
        # Test Simulation Trigger
        tk.Button(self.home_frame, text="Simulate Slouch Event (Trigger Reset)", font=("Arial", 12, "bold"), fg="white", bg="#C0392B", relief="flat", padx=15, pady=8, command=self.trigger_frosted_modal).pack(pady=5)

    # ---------------------------------------------------------
    # LAYOUT 2: TASK BOARD INTERFACE
    # ---------------------------------------------------------
    def init_tasks_view(self):
        self.tasks_frame = tk.Frame(self.stage_frame, bg="#1A1F2C")
        tk.Label(self.tasks_frame, text="Session Task Board", font=("Arial", 22, "bold"), fg="white", bg="#1A1F2C").pack(anchor="w", pady=(10,20))
        
        input_row = tk.Frame(self.tasks_frame, bg="#1A1F2C")
        input_row.pack(fill="x", pady=5)
        
        self.task_entry = tk.Entry(input_row, font=("Arial", 14), bg="#252D3D", fg="white", insertbackground="white", bd=1, relief="solid")
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0,10), ipady=4)
        
        tk.Button(input_row, text="Create Task", font=("Arial", 12), fg="white", bg="#2ECC71", relief="flat", padx=10, command=self.append_new_task).pack(side="right")
        
        # Task Container box area frame
        self.task_box = tk.Frame(self.tasks_frame, bg="#11151E", padx=10, pady=10)
        self.task_box.pack(fill="both", expand=True, pady=15)

    def append_new_task(self):
        val = self.task_entry.get()
        if val:
            row = tk.Frame(self.task_box, bg="#11151E")
            row.pack(fill="x", pady=4)
            var = tk.IntVar()
            cb = tk.Checkbutton(row, text=val, font=("Arial", 13), variable=var, fg="white", bg="#11151E", selectcolor="#252D3D", activebackground="#11151E", activeforeground="white")
            cb.pack(side="left", padx=5)
            self.task_entry.delete(0, 'end')

    # ---------------------------------------------------------
    # LAYOUT 3: SYSTEM PREFERENCES SETTINGS
    # ---------------------------------------------------------
    def init_settings_view(self):
        self.settings_frame = tk.Frame(self.stage_frame, bg="#1A1F2C")
        tk.Label(self.settings_frame, text="App Preferences & Calibration", font=("Arial", 22, "bold"), fg="white", bg="#1A1F2C").pack(anchor="w", pady=(10,20))
        
        c1 = tk.Checkbutton(self.settings_frame, text="Play background environmental audio loops automatically", font=("Arial", 13), fg="white", bg="#1A1F2C", selectcolor="#252D3D", activebackground="#1A1F2C")
        c1.pack(anchor="w", pady=10); c1.select()
        
        c2 = tk.Checkbutton(self.settings_frame, text="Enable instant OS desktop flash banner alerts", font=("Arial", 13), fg="white", bg="#1A1F2C", selectcolor="#252D3D", activebackground="#1A1F2C")
        c2.pack(anchor="w", pady=10)
        
        tk.Label(self.settings_frame, text="Computer Vision Sensor Sensitivity Threshold", font=("Arial", 13), fg="white", bg="#1A1F2C").pack(anchor="w", pady=(20,5))
        slider = tk.Scale(self.settings_frame, from_=0, to=100, orient="horizontal", bg="#1A1F2C", fg="white", troughcolor="#252D3D", highlightthickness=0)
        slider.pack(fill="x", pady=5)

    # ---------------------------------------------------------
    # NAVIGATION UTILITIES
    # ---------------------------------------------------------
    def clear_stage_views(self):
        self.home_frame.pack_forget()
        self.tasks_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.btn_home.configure(bg="#11151E")
        self.btn_tasks.configure(bg="#11151E")
        self.btn_settings.configure(bg="#11151E")

    def show_home(self):
        self.clear_stage_views()
        self.btn_home.configure(bg="#2E4053")
        self.home_frame.pack(fill="both", expand=True)

    def show_tasks(self):
        self.clear_stage_views()
        self.btn_tasks.configure(bg="#2E4053")
        self.tasks_frame.pack(fill="both", expand=True)

    def show_settings(self):
        self.clear_stage_views()
        self.btn_settings.configure(bg="#2E4053")
        self.settings_frame.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # INTERCEPT MODALS OVERLAYS (Stress Mode Recovery)
    # ---------------------------------------------------------
    def trigger_frosted_modal(self):
        self.posture_lbl.configure(text="Posture:  Slouching", fg="#E74C3C")
        self.focus_lbl.configure(text="Status:  Fatigued", fg="#E74C3C")
        
        self.modal_overlay = tk.Frame(self, bg="#0D1117")
        self.modal_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        tk.Label(self.modal_overlay, text=" Screen Temporarily Locked for Mental Reset", font=("Arial", 22, "bold"), fg="#E74C3C", bg="#0D1117").pack(pady=(180, 10))
        tk.Label(self.modal_overlay, text="⭕", font=("Arial", 90), fg="#3498DB", bg="#0D1117").pack(pady=15)
        tk.Label(self.modal_overlay, text="Follow the breathing ring guide. Relax your eyes.", font=("Arial", 14), fg="#BDC3C7", bg="#0D1117").pack(pady=5)
        
        tk.Button(self.modal_overlay, text="Sit Straight (Dismiss Reset Mode)", font=("Arial", 12), fg="white", bg="#2ECC71", relief="flat", padx=15, pady=8, command=self.dismiss_frosted_modal).pack(pady=40)

    def dismiss_frosted_modal(self):
