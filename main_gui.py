import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import time
import winsound
import threading
from PIL import Image, ImageTk

from connect import MotionSystem
from stagecontrol import AlignmentController

# --- Setup motion system ---
ms = MotionSystem("5.153.34.236.1.1")
ms.connect()
controller = AlignmentController(ms, 1310)

# --- GUI helpers ---
def log(msg):
    log_box.insert(tk.END, f"{msg}\n")
    log_box.see(tk.END)

def beep():
    winsound.Beep(2500, 500)

# --- Core Functions ---
def laser_beam_align():
    try:
        controller.find_beam()
        CachePower = [-60, -60, -60]
        CachePower_mean = sum(CachePower) / len(CachePower)
        while CachePower_mean < -15:
            last_CachePower_mean = CachePower_mean
            while CachePower_mean <= -40:
                for i in range(3):
                    CachePower[i] = controller.read_power()
                    log(f"{i}: {CachePower[i]}")
                    time.sleep(2)
                last_CachePower_mean = CachePower_mean
                CachePower_mean = sum(CachePower) / len(CachePower)
                time.sleep(3)
                log(f"Mean: {CachePower_mean}")

            if abs(last_CachePower_mean - CachePower_mean) < 2:
                if controller.read_power() > -20:
                    log("Great, first search is done!")
                    log(controller.read_power())
                    break

                while controller.read_power() < -10.0:
                    log("Oops, hit local minimum…")
                    controller.skip_local_min_ytx()

                    if controller.read_power() < -15.0:
                        controller.skip_local_min_xty()

                log("Finally, get rid of local minimum")
                break

        log("Final: four axis alignment")
        repeatTimes = 3
        while repeatTimes > 0:
            try:
                log(f"Try: {repeatTimes}")
                controller.four_axis_alignment()
                repeatTimes -= 1
            except Exception as e:
                log(f"Alignment error: {e}")
                continue
        log("First Alignment Done!")
        beep()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def move_z(direction):
    dist = simpledialog.askinteger("Move Distance", "Enter moving distance (um):", minvalue=1)
    if dist:
        if direction == "forward":
            ms.ZMove(-dist)
        else:
            ms.ZMove(dist)
        log(f"Z moved {direction} by {dist} um")
        beep()
        time.sleep(1)


def fine_alignment():
    controller.four_axis_fineAlignment()
    log("Fine alignment complete")
    beep()


def find_best_center():
    points = 4
    for point in range(points):
        controller.four_axis_fineAlignment()
        ms.show_positions()
        log(f"Saved position {point}")
        ms.save_current_positions(point)
    best_position = ms.center_position()
    ms.restore_position(best_position)
    ms.show_positions()
    log("Restored best center position")
    beep()


def epoxy_move():
    ms.ZMove(10000)
    messagebox.showinfo("Epoxy", "Add epoxy, then press OK to move back.")
    ms.ZMove(-10000)
    ms.stop()
    log("Epoxy process done")
    beep()


def exit_system():
    ms.stop()
    ms.disconnect()
    root.destroy()

# --- Real-Time Power Monitoring ---
monitoring = False

def toggle_monitoring():
    global monitoring
    monitoring = not monitoring
    if monitoring:
        log("Started power monitoring…")
        btn_monitor.config(text="Stop Monitoring")
        threading.Thread(target=update_power, daemon=True).start()
    else:
        log("Stopped power monitoring")
        btn_monitor.config(text="Start Monitoring")

def update_power():
    while monitoring:
        try:
            power = controller.read_power()
            lbl_power.config(text=f"Current Power: {power:.2f} dBm")
        except Exception as e:
            lbl_power.config(text=f"Error: {e}")
        time.sleep(1)

# --- GUI Layout ---
root = tk.Tk()
root.title("Laser Beam Alignment GUI")

# Load logo (replace 'logo.png' with your file path)
try:
    logo_img = Image.open("Princetel Logo.png")
    logo_img = logo_img.resize((120, 120))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.pack(pady=5)
except Exception as e:
    log_box = None
    messagebox.showwarning("Logo", f"Logo not loaded: {e}")

frame = tk.Frame(root)
frame.pack(pady=10)

btn1 = tk.Button(frame, text="Initial Alignment", width=20, command=laser_beam_align)
btn2 = tk.Button(frame, text="Z-Move Forward", width=20, command=lambda: move_z("forward"))
btn3 = tk.Button(frame, text="Z-Move Backward", width=20, command=lambda: move_z("backward"))
btn4 = tk.Button(frame, text="Fine Alignment", width=20, command=fine_alignment)
btn5 = tk.Button(frame, text="Find Best Center", width=20, command=find_best_center)
btn6 = tk.Button(frame, text="Epoxy Move", width=20, command=epoxy_move)
btn7 = tk.Button(frame, text="Exit", width=20, command=exit_system)

btn1.grid(row=0, column=0, padx=5, pady=5)
btn2.grid(row=1, column=0, padx=5, pady=5)
btn3.grid(row=2, column=0, padx=5, pady=5)
btn4.grid(row=3, column=0, padx=5, pady=5)
btn5.grid(row=4, column=0, padx=5, pady=5)
btn6.grid(row=5, column=0, padx=5, pady=5)
btn7.grid(row=6, column=0, padx=5, pady=5)

# Real-time monitoring button
btn_monitor = tk.Button(frame, text="Start Monitoring", width=20, command=toggle_monitoring)
btn_monitor.grid(row=7, column=0, padx=5, pady=5)

# Power label
lbl_power = tk.Label(root, text="Current Power: --", font=("Arial", 12))
lbl_power.pack(pady=5)

# Log output box
log_box = scrolledtext.ScrolledText(root, width=60, height=20)
log_box.pack(padx=10, pady=10)

root.mainloop()
