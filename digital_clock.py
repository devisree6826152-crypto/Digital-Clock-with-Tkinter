import tkinter as tk
from tkinter import ttk
import time
import math

# ---------------- STARTUP SPLASH WITH PROGRESS BAR ----------------
def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x200+500+250")
    splash.configure(bg="#1e1e1e")

    title = tk.Label(splash, text="Digital Clock Loading...", font=("Arial", 16, "bold"), fg="white", bg="#1e1e1e")
    title.pack(pady=20)

    pb = ttk.Progressbar(splash, mode='determinate', length=300)
    pb.pack(pady=20)

    for i in range(100):
        pb['value'] = i
        splash.update_idletasks()
        time.sleep(0.02)

    splash.destroy()


# ---------------- MAIN CLOCK ----------------
root = tk.Tk()
root.title("Digital Clock")
root.geometry("500x400")
root.resizable(False, False)

show_splash()   # show splash screen first


# ---------------- THEME COLORS ----------------
dark_mode = True
is_24hr = False

def apply_theme():
    if dark_mode:
        root.configure(bg="#000000")
        clock_frame.configure(bg="#000000")
        time_label.configure(bg="#000000", fg="#00FFAA")
        date_label.configure(bg="#000000", fg="#00FFAA")
        toggle_btn.configure(bg="#111111", fg="white")
        mode_btn.configure(bg="#111111", fg="white")
    else:
        root.configure(bg="#e3f2fd")
        clock_frame.configure(bg="#e3f2fd")
        time_label.configure(bg="#e3f2fd", fg="#003366")
        date_label.configure(bg="#e3f2fd", fg="#003366")
        toggle_btn.configure(bg="#0288d1", fg="white")
        mode_btn.configure(bg="#0288d1", fg="white")


# ---------------- TIME UPDATE ----------------
def update_time():
    global is_24hr

    current_time = time.strftime("%H:%M:%S") if is_24hr else time.strftime("%I:%M:%S %p")
    time_label.config(text=current_time)

    current_date = time.strftime("%A, %d %B %Y")
    date_label.config(text=current_date)

    draw_analog_clock()

    root.after(1000, update_time)


# ---------------- TOGGLE 12/24 ----------------
def toggle_format():
    global is_24hr
    is_24hr = not is_24hr
    toggle_btn.config(text="24-Hour" if is_24hr else "12-Hour")


# ---------------- TOGGLE DARK/LIGHT ----------------
def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    mode_btn.config(text="Dark Mode" if dark_mode else "Light Mode")
    apply_theme()


# ---------------- ANALOG CLOCK ----------------
def draw_analog_clock():
    canvas.delete("all")

    cx, cy = 60, 60
    r = 50

    # Clock border
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="#00ffaa" if dark_mode else "#003366", width=3)

    # Time
    h = int(time.strftime("%I"))
    m = int(time.strftime("%M"))
    s = int(time.strftime("%S"))

    # Angles
    s_angle = math.radians(s * 6 - 90)
    m_angle = math.radians(m * 6 - 90)
    h_angle = math.radians((h % 12) * 30 + m * 0.5 - 90)

    # Hands
    canvas.create_line(cx, cy, cx + 45 * math.cos(s_angle), cy + 45 * math.sin(s_angle), fill="red", width=2)
    canvas.create_line(cx, cy, cx + 35 * math.cos(m_angle), cy + 35 * math.sin(m_angle), fill="#00aaff", width=3)
    canvas.create_line(cx, cy, cx + 25 * math.cos(h_angle), cy + 25 * math.sin(h_angle), fill="#ffaa00", width=4)


# ---------------- UI LAYOUT ----------------
clock_frame = tk.Frame(root, bg="#000000")
clock_frame.pack(expand=True)

time_label = tk.Label(clock_frame, font=("Orbitron", 38, "bold"), bg="#000000", fg="#00FFAA")
time_label.pack(pady=10)

date_label = tk.Label(clock_frame, font=("Arial", 14), bg="#000000", fg="#00FFAA")
date_label.pack()

canvas = tk.Canvas(root, width=120, height=120, bg="black", highlightthickness=0)
canvas.pack(pady=5)

# Buttons
toggle_btn = tk.Button(root, text="12-Hour", font=("Arial", 12, "bold"), command=toggle_format)
toggle_btn.pack(pady=5)

mode_btn = tk.Button(root, text="Dark Mode", font=("Arial", 12, "bold"), command=toggle_mode)
mode_btn.pack(pady=5)


# Button Hover Effect
def on_enter(e): e.widget.config(bg="#444444")
def on_leave(e): apply_theme()

toggle_btn.bind("<Enter>", on_enter)
toggle_btn.bind("<Leave>", on_leave)
mode_btn.bind("<Enter>", on_enter)
mode_btn.bind("<Leave>", on_leave)


apply_theme()
update_time()

root.mainloop()
