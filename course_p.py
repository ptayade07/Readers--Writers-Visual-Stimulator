import tkinter as tk
from tkinter import font as tkfont
import threading
import time
import random
import math

# --------------------------
# Globals & sync primitives
# --------------------------
data = 0
read_count = 0
running = False
mutex = threading.Semaphore(1)
rw_mutex = threading.Semaphore(1)

# --------------------------
# Thread-safe UI helpers
# --------------------------
def safe_call(fn, *a, **k):
    root.after(0, lambda: fn(*a, **k))

# --------------------------
# UI colors
# --------------------------
BG = "#0f172a"
PANEL = "#1e293b"
CARD_NORMAL = "#2c3e50"
TEXT = "#e6f0ff"
ACCENT = "#34d399"
ACCENT_DARK = "#065f46"
ACTIVE_READ = "#9be7c4"
ACTIVE_WRITE = "#ff6b81"
GLOW = "#facc15"

# --------------------------
# Tkinter setup
# --------------------------
root = tk.Tk()
root.title("Readers–Writers — Sleek Simulator")
root.geometry("920x620")
root.configure(bg=BG)

title_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
label_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
mono_font = tkfont.Font(family="Courier New", size=10)

# --------------------------
# Header
# --------------------------
header = tk.Frame(root, bg=BG)
header.pack(fill="x", pady=(15, 8))
tk.Label(header, text="Readers–Writers Synchronization Simulator", font=title_font, fg=TEXT, bg=BG).pack(anchor="center")

# --------------------------
# Main container
# --------------------------
main_container = tk.Frame(root, bg=BG)
main_container.pack(fill="both", expand=True, padx=20, pady=10)

panel = tk.Frame(main_container, bg=PANEL)
panel.pack(fill="both", expand=True)

# --------------------------
# Right panel
# --------------------------
ctrl_frame = tk.Frame(panel, bg=PANEL, width=280)
ctrl_frame.pack(side="right", fill="y", padx=(5, 10), pady=10)

info_header = tk.Frame(ctrl_frame, bg=CARD_NORMAL, pady=8, padx=10)
info_header.pack(fill="x", pady=(0, 8))
shared_label = tk.Label(info_header, text="Shared Data: 0", font=label_font, fg=ACCENT, bg=CARD_NORMAL)
shared_label.pack(pady=(0, 4))
status_var = tk.StringVar(value="Status: Ready")
status_lbl = tk.Label(info_header, textvariable=status_var, font=("Segoe UI", 10, "italic"), fg="#a9c2d8", bg=CARD_NORMAL)
status_lbl.pack()

# --------------------------
# Buttons
# --------------------------
def disable_buttons():
    start_btn.config(state="disabled", bg="#10b981", fg="#a7f3d0")
    stop_btn.config(state="normal", bg="#ef4444", fg="#fee2e2")

def enable_buttons():
    start_btn.config(state="normal", bg="#059669", fg="#FFFFFF")
    stop_btn.config(state="disabled", bg="#a9a9a9", fg="#FFFFFF")

def reset_ui():
    """Reset visuals and logs for a new run."""
    for i in range(len(reader_blocks)):
        safe_call(set_reader_active, i, False)
    for i in range(len(writer_blocks)):
        safe_call(set_writer_active, i, False)
    safe_call(set_data, 0, False)
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.insert(tk.END, "System ready for next run...\n")
    log_box.configure(state="disabled")
    safe_call(status_var.set, "Status: Ready")

def start_sim():
    global running, data, read_count
    if running:
        return
    running = True
    data = 0
    read_count = 0
    reset_ui()

    safe_call(log, "🚀 Simulation started...")
    disable_buttons()

    readers = [threading.Thread(target=reader_thread, args=(i,)) for i in range(1, 4)]
    writers = [threading.Thread(target=writer_thread, args=(i,)) for i in range(1, 3)]
    for t in readers + writers:
        t.daemon = True
        t.start()

    # auto-stop after approx duration
    root.after(11000, stop_sim)

def stop_sim():
    global running
    if not running:
        return
    running = False
    safe_call(log, "\n🎯 Simulation complete! All readers and writers have finished.")
    safe_call(status_var.set, "Status: Complete — Ready for new run")
    safe_call(enable_buttons)

# Buttons layout
btn_frame = tk.Frame(ctrl_frame, bg=PANEL, pady=10)
btn_frame.pack(fill="x", side="bottom")

start_btn = tk.Button(btn_frame, text="▶ Start Simulation", command=start_sim,
                      bg="#059669", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                      bd=0, padx=15, pady=8)
start_btn.pack(side="left", expand=True, padx=6)
stop_btn = tk.Button(btn_frame, text="■ Stop", command=stop_sim,
                     bg="#a9a9a9", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                     bd=0, padx=15, pady=8, state="disabled")
stop_btn.pack(side="left", expand=True, padx=6)

# --------------------------
# Log Box
# --------------------------
log_label = tk.Label(ctrl_frame, text="Activity Log", font=label_font, fg=TEXT, bg=PANEL)
log_label.pack(anchor="w", padx=6, pady=(4, 2))
log_box = tk.Text(ctrl_frame, height=18, width=35, bg="#071328", fg="#d1e0ff", font=mono_font, bd=0, padx=8, pady=8)
log_box.pack(padx=6, pady=(0, 6), fill="both", expand=True)
log_box.insert(tk.END, "System ready...\n")
log_box.configure(state="disabled")

def log(msg):
    log_box.configure(state="normal")
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.configure(state="disabled")

# --------------------------
# Left: Visualization
# --------------------------
vis_frame = tk.Frame(panel, bg=PANEL)
vis_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
canvas_bg = tk.Frame(vis_frame, bg=CARD_NORMAL, bd=2, relief="groove")
canvas_bg.pack(fill="both", expand=True, padx=5, pady=5)
canvas = tk.Canvas(canvas_bg, width=640, height=420, bg=CARD_NORMAL, highlightthickness=0)
canvas.pack(fill="both", expand=True, padx=10, pady=10)

reader_blocks, writer_blocks, reader_texts, writer_texts = [], [], [], []

CANVAS_W, CANVAS_H = 640, 420
r_y = 90
w_y = 330
BLOCK_W, BLOCK_H = 120, 50
CIRCLE_RADIUS = 60
center_x, center_y = CANVAS_W * 0.40, CANVAS_H * 0.5
r_x = [center_x - 180, center_x, center_x + 180]
w_x = [center_x - 90, center_x + 90]

circle = canvas.create_oval(center_x - CIRCLE_RADIUS, center_y - CIRCLE_RADIUS,
                            center_x + CIRCLE_RADIUS, center_y + CIRCLE_RADIUS,
                            fill=ACCENT_DARK, outline=ACCENT, width=4)
data_text = canvas.create_text(center_x, center_y, text="Data: 0", fill=TEXT, font=("Segoe UI", 16, "bold"))

for i, x in enumerate(r_x):
    rect = canvas.create_rectangle(x - 60, r_y - 25, x + 60, r_y + 25, fill=CARD_NORMAL, outline="#4a637a", width=2)
    text = canvas.create_text(x, r_y, text=f"Reader {i + 1}", fill=TEXT, font=("Segoe UI", 11, "bold"))
    reader_blocks.append(rect)
    reader_texts.append(text)

for i, x in enumerate(w_x):
    rect = canvas.create_rectangle(x - 60, w_y - 25, x + 60, w_y + 25, fill=CARD_NORMAL, outline="#4a637a", width=2)
    text = canvas.create_text(x, w_y, text=f"Writer {i + 1}", fill=TEXT, font=("Segoe UI", 11, "bold"))
    writer_blocks.append(rect)
    writer_texts.append(text)

# --- Draw connecting lines (RE-ADDED LOGIC) ---
# Readers to Data
for x_reader in r_x:
    # Line starts at reader's bottom center
    line_start_x = x_reader
    line_start_y = r_y + BLOCK_H/2 

    # Vector from reader block to circle center
    dx = center_x - line_start_x
    dy = center_y - line_start_y
    distance = math.sqrt(dx**2 + dy**2)

    # Calculate the intersection point on the circle's circumference (line end)
    if distance > 0:
        x_end = line_start_x + (dx / distance) * (distance - CIRCLE_RADIUS)
        y_end = line_start_y + (dy / distance) * (distance - CIRCLE_RADIUS)
    else: 
        x_end = center_x
        y_end = center_y - CIRCLE_RADIUS
        
    canvas.create_line(line_start_x, line_start_y, x_end, y_end, fill="#4a637a", width=2, arrow=tk.LAST)

# Data to Writers
for x_writer in w_x:
    # Line ends at writer's top center
    line_end_x = x_writer
    line_end_y = w_y - BLOCK_H/2

    # Vector from circle center to writer block
    dx = line_end_x - center_x
    dy = line_end_y - center_y
    distance = math.sqrt(dx**2 + dy**2)

    # Calculate the intersection point on the circle's circumference (line start)
    if distance > 0:
        x_start = center_x + (dx / distance) * CIRCLE_RADIUS
        y_start = center_y + (dy / distance) * CIRCLE_RADIUS
    else: 
        x_start = center_x
        y_start = center_y + CIRCLE_RADIUS
        
    canvas.create_line(x_start, y_start, line_end_x, line_end_y, fill="#4a637a", width=2, arrow=tk.LAST)
# --------------------------
# UI helpers
# --------------------------
def set_reader_active(i, active=True):
    color = ACTIVE_READ if active else CARD_NORMAL
    text_color = ACCENT_DARK if active else TEXT
    canvas.itemconfig(reader_blocks[i], fill=color, outline=ACCENT if active else "#4a637a")
    canvas.itemconfig(reader_texts[i], fill=text_color)

def set_writer_active(i, active=True):
    color = ACTIVE_WRITE if active else CARD_NORMAL
    text_color = "#330000" if active else TEXT
    canvas.itemconfig(writer_blocks[i], fill=color, outline="#dc2626" if active else "#4a637a")
    canvas.itemconfig(writer_texts[i], fill=text_color)

def set_data(value, glow=False):
    global data
    data = value
    canvas.itemconfig(data_text, text=f"Data: {value}")
    shared_label.config(text=f"Shared Data: {value}")
    outline = ACCENT if not glow else GLOW
    canvas.itemconfig(circle, outline=outline, width=4 if not glow else 6)
    if glow:
        canvas.itemconfig(data_text, fill=GLOW)
        root.after(800, lambda: canvas.itemconfig(data_text, fill=TEXT) or canvas.itemconfig(circle, outline=ACCENT, width=4))

# --------------------------
# Reader/Writer Threads
# --------------------------
def reader_thread(id):
    global read_count
    loops = 3
    for _ in range(loops):
        if not running:
            break
        time.sleep(random.uniform(0.8, 2.2))
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            rw_mutex.acquire()
        mutex.release()

        safe_call(set_reader_active, id - 1, True)
        safe_call(log, f"📗 Reader {id} is reading data...")
        safe_call(status_var.set, f"Status: Reader {id} reading")
        time.sleep(random.uniform(0.8, 1.5))
        safe_call(log, f"✅ Reader {id} finished reading data = {data}")
        safe_call(set_reader_active, id - 1, False)

        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            rw_mutex.release()
        mutex.release()

def writer_thread(id):
    global data
    loops = 2
    for _ in range(loops):
        if not running:
            break
        time.sleep(random.uniform(1.6, 3.5))
        rw_mutex.acquire()

        safe_call(set_writer_active, id - 1, True)
        safe_call(log, f"✏️ Writer {id} is writing...")
        safe_call(status_var.set, f"Status: Writer {id} writing")
        new_data = random.randint(1, 99)
        safe_call(set_data, new_data, True)
        data = new_data # Update global data value
        time.sleep(random.uniform(0.9, 1.6))
        safe_call(log, f"✅ Writer {id} finished writing, data = {data}")
        safe_call(set_writer_active, id - 1, False)
        rw_mutex.release()

# --------------------------
# Run
# --------------------------
enable_buttons()
root.mainloop()