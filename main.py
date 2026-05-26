import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import customtkinter as ctk
from questions import questions

# ---------------- PRE-SET CUSTOM CORE CONFIGS ---------------- #
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

# ---------------- MATRIX DATABASE GATEWAY ---------------- #
conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")
conn.commit()

# ---------------- MASTER APPLICATION NODE ---------------- #
root = ctk.CTk()
root.title("🧠 IntelliQuiz Pro Suite v2.0")
root.geometry("1150x760") # Optimized Height to prevent screen cutting down
root.configure(fg_color="#0F172A")  # Slate 900 Deep Space Background
root.resizable(False, False)

# System Runtime State Engines
score = 0
current = 0
quiz = []
current_user = "Guest"
selected_ans_string = ""  
timer_running = False
time_left = 15
lifeline_used = False  
option_card_widgets = []  
user_session_logs = []  # Cache array tracking exact selection mistakes

def clear():
    global timer_running
    timer_running = False  
    for widget in root.winfo_children():
        widget.destroy()

# System Audio Feedback Triggers
def play_sound(state_type):
    try:
        if state_type == "success":
            root.bell()  
        elif state_type == "error":
            root.after(0, root.bell)
            root.after(100, root.bell)  
    except:
        pass

# ---------------- LAYER 1: AUTHENTICATION MODULE ---------------- #
def login_page():
    clear()
    global lifeline_used, user_session_logs
    lifeline_used = False
    user_session_logs = []

    ctk.CTkLabel(
        root, text="🧠 IntelliQuiz Pro",
        font=("Helvetica", 42, "bold"), text_color="#22D3EE"
    ).pack(pady=(45, 5))

    ctk.CTkLabel(
        root, text="Enterprise-Level Knowledge Assessment Terminal Engine",
        font=("Arial", 14, "italic"), text_color="#64748B"
    ).pack(pady=(0, 25))

    card = ctk.CTkFrame(root, fg_color="#1E293B", corner_radius=20, border_width=1, border_color="#334155")
    card.pack(pady=10, ipadx=45, ipady=25)

    ctk.CTkLabel(
        card, text="Authorization Vault Gate 👋",
        font=("Arial", 20, "bold"), text_color="#FFFFFF"
    ).pack(pady=(15, 15))

    username_entry = ctk.CTkEntry(
        card, width=350, height=45, placeholder_text="Enter Username ID",
        font=("Arial", 14), fg_color="#0F172A", border_color="#475569", text_color="white", corner_radius=10
    )
    username_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(
        card, width=350, height=45, placeholder_text="Enter Secure Password Code", show="*",
        font=("Arial", 14), fg_color="#0F172A", border_color="#475569", text_color="white", corner_radius=10
    )
    password_entry.pack(pady=10)

    def login_trigger():
        global current_user
        u, p = username_entry.get().strip(), password_entry.get().strip()
        if not u or not p or u == "Enter Username ID" or p == "Enter Secure Password Code":
            messagebox.showwarning("Execution Aborted", "Both authorization input strings are required.")
            return
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if cur.fetchone():
            current_user = u
            dashboard(u)
        else:
            messagebox.showerror("Access Void", "The credential encryption layout did not match parameters.")

    def register_trigger():
        u, p = username_entry.get().strip(), password_entry.get().strip()
        if not u or not p or u == "Enter Username ID" or p == "Enter Secure Password Code":
            messagebox.showwarning("Execution Aborted", "Registration requires dual parameter initialization strings.")
            return
        cur.execute("SELECT * FROM users WHERE username=?", (u,))
        if cur.fetchone():
            messagebox.showwarning("Duplicate Identity", "This entity profile configuration is already active inside database arrays.")
            return
        cur.execute("INSERT INTO users VALUES (?,?)", (u, p))
        conn.commit()
        messagebox.showinfo("Success", "Security Node Securely Registered To Internal Database Array! 🎉")

    ctk.CTkButton(
        card, text="Authenticate Account Session", width=350, height=45, font=("Arial", 14, "bold"),
        fg_color="#06B6D4", hover_color="#0891B2", corner_radius=10, command=login_trigger
    ).pack(pady=(20, 10))

    ctk.CTkButton(
        card, text="Provision New Pipeline Channel", width=350, height=45, font=("Arial", 14, "bold"),
        fg_color="#10B981", hover_color="#059669", corner_radius=10, command=register_trigger
    ).pack(pady=5)


# ---------------- LAYER 2: SYSTEM MANAGEMENT DASHBOARD ---------------- #
def dashboard(name):
    clear()

    avatar_frame = ctk.CTkFrame(root, fg_color="transparent")
    avatar_frame.pack(pady=(45, 5))
    
    ctk.CTkLabel(avatar_frame, text="⚡", font=("Arial", 38), text_color="#EAB308").pack(side="left", padx=10)
    
    title_box = ctk.CTkFrame(avatar_frame, fg_color="transparent")
    title_box.pack(side="left")
    ctk.CTkLabel(title_box, text=f"Welcome Commander, {name}", font=("Arial", 32, "bold"), text_color="#FFFFFF").pack(anchor="w")
    ctk.CTkLabel(title_box, text="Security clearance status: Authorized Senior Developer 🎖️", font=("Arial", 13), text_color="#22D3EE").pack(anchor="w")

    panel_box = ctk.CTkFrame(root, fg_color="#1E293B", corner_radius=20, border_width=1, border_color="#334155")
    panel_box.pack(pady=25, ipadx=55, ipady=30)

    ctk.CTkButton(
        panel_box, text="⚡ Execute High-Performance Assessment", width=350, height=52,
        font=("Arial", 15, "bold"), fg_color="#06B6D4", hover_color="#0891B2", corner_radius=12, command=category_page
    ).pack(pady=12)

    ctk.CTkButton(
        panel_box, text="⚙️ Structural Quiz Builder Workspace", width=350, height=52,
        font=("Arial", 15, "bold"), fg_color="#10B981", hover_color="#059669", corner_radius=12, command=create_quiz
    ).pack(pady=12)
    
    ctk.CTkButton(
        panel_box, text="🛑 Destroy Active Session Token", width=350, height=42,
        font=("Arial", 14, "bold"), fg_color="#EF4444", hover_color="#DC2626", corner_radius=10, command=login_page
    ).pack(pady=(25, 5))


# ---------------- LAYER 3: DOMAIN SPECIFICATION TRACKS ---------------- #
def category_page():
    clear()

    ctk.CTkLabel(
        root, text="Assessment Array Domain Framework",
        font=("Arial", 32, "bold"), text_color="#FFFFFF"
    ).pack(pady=(60, 5))

    ctk.CTkLabel(
        root, text="Allocate resources to localized technology modules compiled inside tracking systems.",
        font=("Arial", 14), text_color="#94A3B8"
    ).pack(pady=(0, 35))

    container_frame = ctk.CTkFrame(root, fg_color="#1E293B", corner_radius=20, border_width=1, border_color="#334155")
    container_frame.pack(pady=10, ipadx=45, ipady=30)

    for cat_key in questions.keys():
        ctk.CTkButton(
            container_frame, text=f"⚡ Initialize Core Variant: {cat_key} ", width=320, height=50,
            font=("Arial", 14, "bold"), fg_color="#06B6D4", hover_color="#0891B2", corner_radius=12,
            command=lambda selected_cat=cat_key: start_quiz(selected_cat)
        ).pack(pady=10)


# ---------------- LAYER 4: CUSTOM QUIZ BUILDER ---------------- #
def create_quiz():
    clear()

    ctk.CTkLabel(
        root, text="Custom Knowledge Injector Core",
        font=("Arial", 30, "bold"), text_color="#FFFFFF"
    ).pack(pady=(25, 5))
    
    ctk.CTkLabel(
        root, text="Direct data entry pipelines mapping new dictionaries into active process environments.",
        font=("Arial", 13), text_color="#94A3B8"
    ).pack(pady=(0, 20))

    form = ctk.CTkFrame(root, fg_color="#1E293B", corner_radius=20, border_width=1, border_color="#334155")
    form.pack(pady=5, padx=80, fill="both", expand=True)

    q_in = ctk.CTkEntry(form, width=720, height=42, placeholder_text="Formulate Core Question Anchor Stem Prompt Array...", corner_radius=10)
    q_in.pack(pady=(20, 10))

    a_in = ctk.CTkEntry(form, width=580, height=35, placeholder_text="Option State Vector Alpha", corner_radius=8)
    a_in.pack(pady=5)
    b_in = ctk.CTkEntry(form, width=580, height=35, placeholder_text="Option State Vector Beta", corner_radius=8)
    b_in.pack(pady=5)
    c_in = ctk.CTkEntry(form, width=580, height=35, placeholder_text="Option State Vector Gamma", corner_radius=8)
    c_in.pack(pady=5)
    d_in = ctk.CTkEntry(form, width=580, height=35, placeholder_text="Option State Vector Delta", corner_radius=8)
    d_in.pack(pady=5)

    ans_in = ctk.CTkEntry(form, width=580, height=40, placeholder_text="Exact Explicit Target Matching Solution Value String", border_color="#10B981", corner_radius=8)
    ans_in.pack(pady=(12, 10))

    def commit_database_array():
        q, o1, o2, o3, o4, ans = q_in.get().strip(), a_in.get().strip(), b_in.get().strip(), c_in.get().strip(), d_in.get().strip(), ans_in.get().strip()
        if not all([q, o1, o2, o3, o4, ans]):
            messagebox.showwarning("Validation Conflict", "All procedural injection arrays need structured values.")
            return

        new_dict = {"question": q, "options": [o1, o2, o3, o4], "answer": ans}
        if "Python" not in questions: questions["Python"] = []
        questions["Python"].append(new_dict)
        
        messagebox.showinfo("Committed", "New Variable Parameters Injected Into Live Module Track Cache! 🎉")
        dashboard(current_user)

    box = ctk.CTkFrame(form, fg_color="transparent")
    box.pack(pady=(10, 15))
    ctk.CTkButton(box, text="Commit Memory Structure", width=200, height=42, font=("Arial", 13, "bold"), fg_color="#10B981", hover_color="#059669", corner_radius=10, command=commit_database_array).grid(row=0, column=0, padx=15)
    ctk.CTkButton(box, text="Abort Operation Pipeline", width=200, height=42, font=("Arial", 13, "bold"), fg_color="#64748B", hover_color="#475569", corner_radius=10, command=lambda: dashboard(current_user)).grid(row=0, column=1, padx=15)


# ---------------- SETUP LOADER CONTROLLER ---------------- #
def start_quiz(category):
    global quiz, current, score, lifeline_used, user_session_logs
    current, score = 0, 0
    lifeline_used = False
    user_session_logs = []
    quiz = list(questions[category])
    random.shuffle(quiz)
    quiz_screen()


# -------- LAYER 5: LIVE QUIZ TERMINAL CORE -------- #
def quiz_screen():
    global selected_ans_string, timer_running, time_left, option_card_widgets
    clear()
    
    selected_ans_string = "" 
    q = quiz[current]
    option_card_widgets = [] 

    header = ctk.CTkFrame(root, fg_color="transparent")
    header.pack(pady=(20, 5), fill="x", padx=120)

    ctk.CTkLabel(header, text=f"LIVE EVALUATION: {current + 1} OF {len(quiz)}", font=("Helvetica", 14, "bold"), text_color="#EAB308").pack(side="left")
    
    timer_label = ctk.CTkLabel(header, text="⏱️ Time Left: 15s", font=("Helvetica", 15, "bold"), text_color="#EF4444")
    timer_label.pack(side="left", padx=180)

    ctk.CTkLabel(header, text=f"ACCUMULATION INDICES: {score}", font=("Helvetica", 14, "bold"), text_color="#10B981").pack(side="right")

    progress_bar = ctk.CTkProgressBar(root, width=910, height=8, corner_radius=4, fg_color="#1E293B", progress_color="#22D3EE")
    progress_bar.pack(pady=(0, 10))
    progress_bar.set(current / len(quiz))

    stem_card = ctk.CTkFrame(root, fg_color="#1E293B", corner_radius=16, border_width=1, border_color="#334155")
    stem_card.pack(pady=8, fill="x", padx=120, ipady=10)

    ctk.CTkLabel(stem_card, text=q["question"], wraplength=850, font=("Arial", 20, "bold"), text_color="#FFFFFF").pack(pady=15, padx=25)

    options_wrapper = ctk.CTkFrame(root, fg_color="transparent")
    options_wrapper.pack(pady=5)

    def select_card_trigger(chosen_text, active_frame_node):
        global selected_ans_string
        selected_ans_string = chosen_text  

        for frame_widget, inner_dot, label_node, opt_val in option_card_widgets:
            if frame_widget.winfo_viewable():  
                frame_widget.configure(fg_color="#1E293B", border_color="#334155", border_width=1)
                inner_dot.configure(fg_color="transparent", border_color="#64748B")
                label_node.configure(text_color="#CBD5E1")

        active_frame_node.configure(fg_color="#0F172A", border_color="#22D3EE", border_width=2) 
        inner_dot_target = active_frame_node.winfo_children()[0]
        inner_dot_target.configure(fg_color="#22D3EE", border_color="#22D3EE") 
        
        label_target = active_frame_node.winfo_children()[1]
        label_target.configure(text_color="#22D3EE")

    for opt_txt in q["options"]:
        card_capsule = ctk.CTkFrame(options_wrapper, width=640, height=48, fg_color="#1E293B", border_width=1, border_color="#334155", corner_radius=12, cursor="hand2")
        card_capsule.pack(pady=5, fill="x")
        card_capsule.pack_propagate(False)

        micro_dot = ctk.CTkFrame(card_capsule, width=14, height=14, corner_radius=7, fg_color="transparent", border_width=2, border_color="#64748B")
        micro_dot.pack(side="left", padx=(20, 15))

        txt_lbl = ctk.CTkLabel(card_capsule, text=opt_txt, font=("Arial", 14, "bold"), text_color="#CBD5E1")
        txt_lbl.pack(side="left", anchor="w")

        option_card_widgets.append((card_capsule, micro_dot, txt_lbl, opt_txt))

        def make_hover_enter(f=card_capsule, lbl=txt_lbl):
            return lambda e: f.configure(border_color="#06B6D4") if selected_ans_string != lbl.cget("text") else None
        def make_hover_leave(f=card_capsule, lbl=txt_lbl):
            return lambda e: f.configure(border_color="#334155") if selected_ans_string != lbl.cget("text") else None

        card_capsule.bind("<Enter>", make_hover_enter())
        card_capsule.bind("<Leave>", make_hover_leave())
        
        card_capsule.bind("<Button-1>", lambda event, fs=opt_txt, en=card_capsule: select_card_trigger(fs, en))
        micro_dot.bind("<Button-1>", lambda event, fs=opt_txt, en=card_capsule: select_card_trigger(fs, en))
        txt_lbl.bind("<Button-1>", lambda event, fs=opt_txt, en=card_capsule: select_trigger(fs, en))
        txt_lbl.bind("<Button-1>", lambda event, fs=opt_txt, en=card_capsule: select_card_trigger(fs, en))

    def trigger_50_50():
        global lifeline_used
        if lifeline_used:
            return
        lifeline_used = True
        lifeline_btn.configure(state="disabled", text="❌ Lifeline Expired", fg_color="#475569")
        
        correct_ans = q["answer"]
        wrong_options = [item for item in option_card_widgets if item[3] != correct_ans]
        options_to_remove = random.sample(wrong_options, 2)
        
        for frame_w, _, _, _ in options_to_remove:
            frame_w.pack_forget()  

    action_panel = ctk.CTkFrame(root, fg_color="transparent")
    action_panel.pack(pady=15)

    lifeline_btn = ctk.CTkButton(
        action_panel, text="💡 Trigger AI 50:50 Lifeline", width=220, height=45,
        font=("Arial", 13, "bold"), fg_color="#6366F1", hover_color="#4F46E5", corner_radius=10,
        command=trigger_50_50
    )
    lifeline_btn.grid(row=0, column=0, padx=15)
    if lifeline_used:
        lifeline_btn.configure(state="disabled", text="❌ Lifeline Expired", fg_color="#475569")

    def process_vector_advance():
        global current, score, timer_running, user_session_logs
        timer_running = False  
        if not selected_ans_string:
            messagebox.showwarning("Selection Void", "Operational sequence tracking locked. Select an option parameter.")
            timer_running = True
            countdown_loop(timer_label)
            return

        is_correct = (selected_ans_string == q["answer"])
        if is_correct:
            score += 1
            play_sound("success")
        else:
            play_sound("error")
        
        user_session_logs.append({
            "question": q["question"],
            "user_ans": selected_ans_string,
            "correct_ans": q["answer"],
            "status": "CORRECT" if is_correct else "WRONG"
        })

        current += 1
        if current >= len(quiz):
            render_evaluation_metrics()
        else:
            quiz_screen()

    ctk.CTkButton(
        action_panel, text="Advance Processing Vector ➜", width=260, height=45,
        font=("Arial", 14, "bold"), fg_color="#06B6D4", hover_color="#0891B2", corner_radius=10,
        command=process_vector_advance
    ).grid(row=0, column=1, padx=15)

    time_left = 15
    timer_running = True
    countdown_loop(timer_label)

def countdown_loop(label_node):
    global time_left, current, timer_running, user_session_logs
    if not timer_running:
        return
    if time_left > 0:
        label_node.configure(text=f"⏱️ Time Left: {time_left}s")
        time_left -= 1
        root.after(1000, lambda: countdown_loop(label_node))
    else:
        play_sound("error")
        user_session_logs.append({
            "question": quiz[current]["question"],
            "user_ans": "TIMEOUT (No Selection Made)",
            "correct_ans": quiz[current]["answer"],
            "status": "TIMEOUT"
        })
        messagebox.showinfo("Timeout Node Triggered", "Time vector exhausted! System shifting to upcoming module slot.")
        current += 1
        if current >= len(quiz):
            render_evaluation_metrics()
        else:
            quiz_screen()


# -------- LAYER 6: ADVANCED METRICS GRAPHICAL PANEL & SCROLLABLE LOG REPORT -------- #
def render_evaluation_metrics():
    clear()
    percentage_score = (score / len(quiz)) * 100 if len(quiz) > 0 else 0

    ctk.CTkLabel(root, text="🎉 ASSESSMENT PIPELINE TERMINATED 🎉", font=("Helvetica", 28, "bold"), text_color="#F59E0B").pack(pady=(20, 10))

    report = ctk.CTkFrame(root, fg_color="#1E293B", corner_radius=20, border_width=1, border_color="#334155")
    report.pack(pady=5, ipadx=45, ipady=10, fill="x", padx=100)

    if percentage_score >= 80:
        rank, insight, rank_color = "Elite Cyber Architect 🏆", "Exceptional competency. Logic parameters aligned perfectly.", "#10B981"
    elif percentage_score >= 50:
        rank, insight, rank_color = "System Analyst Associate ⚙️", "Moderate yield. Core constructs require localized patches.", "#EAB308"
    else:
        rank, insight, rank_color = "Junior Runtime Debugger 🛠️", "Sub-optimal metrics output. Re-initialize baseline studies.", "#EF4444"

    ctk.CTkLabel(report, text=f"Classification Rank: {rank}", font=("Arial", 18, "bold"), text_color=rank_color).pack(pady=(8, 2))
    ctk.CTkLabel(report, text=f"AI Analytics Insight: \"{insight}\"", font=("Arial", 12, "italic"), text_color="#94A3B8").pack(pady=(0, 5))
    ctk.CTkLabel(report, text=f"Score Summary: {score} / {len(quiz)}  |  Efficiency Vector: {percentage_score:.0f}%", font=("Arial", 14, "bold"), text_color="#22D3EE").pack(pady=4)

    ctk.CTkLabel(root, text="📜 Real-time Module Logs & Review Terminal Structure:", font=("Arial", 13, "bold"), text_color="#94A3B8").pack(pady=(10, 5), anchor="w", padx=105)
    
    # Adjusted Height here to perfectly secure the bottom layout button area
    scroll_box = ctk.CTkScrollableFrame(root, width=910, height=200, fg_color="#0F172A", border_width=1, border_color="#334155", corner_radius=12)
    scroll_box.pack(pady=5)

    for i, item in enumerate(user_session_logs):
        log_card = ctk.CTkFrame(scroll_box, fg_color="#1E293B", corner_radius=8, border_width=1, border_color="#475569")
        log_card.pack(pady=4, fill="x", padx=5)
        
        status_color = "#10B981" if item["status"] == "CORRECT" else "#EF4444"
        
        ctk.CTkLabel(log_card, text=f"Item {i+1}: {item['question']}", font=("Arial", 13, "bold"), text_color="white", wraplength=850).pack(anchor="w", padx=15, pady=(6, 2))
        ctk.CTkLabel(log_card, text=f"Your Selected Value: {item['user_ans']}  |  Target Registry Match: {item['correct_ans']}", font=("Arial", 12), text_color="#94A3B8").pack(anchor="w", padx=15, pady=(0, 2))
        ctk.CTkLabel(log_card, text=f"Verification Vector: {item['status']}", font=("Arial", 11, "bold"), text_color=status_color).pack(anchor="w", padx=15, pady=(0, 6))

    ctk.CTkButton(
        root, text="Re-Initialize Terminal System Loop Instance", width=320, height=45,
        font=("Arial", 14, "bold"), fg_color="#10B981", hover_color="#059669", corner_radius=12,
        command=lambda: dashboard(current_user)
    ).pack(pady=15)


# ---------------- SYSTEM ENGINE ENTRY TRIGGER INITIALIZER ---------------- #
login_page()
root.mainloop()