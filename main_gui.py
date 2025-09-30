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


def choose_distance_popup():
    popup = tk.Toplevel(root)
    popup.title("Choose Distance")
    popup.geometry("250x350")
    selected_dist = tk.IntVar(value=500)

    tk.Label(popup, text="Select moving distance (um):").pack(pady=10)

    distances = [100, 200, 500, 1000, 2000, 5000]
    for d in distances:
        tk.Radiobutton(popup, text=f"{d} um", variable=selected_dist, value=d).pack(anchor=tk.W)

    custom_var = tk.StringVar()
    tk.Label(popup, text="Or enter custom distance:").pack(pady=5)
    tk.Entry(popup, textvariable=custom_var).pack()

    def confirm():
        if custom_var.get():
            try:
                selected_dist.set(int(custom_var.get()))
            except ValueError:
                messagebox.showwarning("Invalid", "Enter a valid number")
                return
        popup.destroy()

    tk.Button(popup, text="OK", command=confirm).pack(pady=10)
    popup.grab_set()
    root.wait_window(popup)

    return selected_dist.get()


def move_z(direction):
    dist = choose_distance_popup()
    if dist is not None:
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
        messagebox.showinfo("Next Point", f"Point {point} saved. Press OK to continue to next point.")
        beep()
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


main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)


# Left frame for buttons and logo
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)


# Right frame for log and power
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)


# Load logo (replace 'logo.png' with your file path)
try:
    logo_img = Image.open("Princetel Logo.png")
    logo_img = logo_img.resize((120, 120))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(left_frame, image=logo_photo)
    logo_label.pack(pady=5)
except Exception as e:
    messagebox.showwarning("Logo", f"Logo not loaded: {e}")


# Buttons with different colors
btn1 = tk.Button(left_frame, text="Initial Alignment", width=20, command=laser_beam_align, bg="lightblue")
btn2 = tk.Button(left_frame, text="Z-Move Forward", width=20, command=lambda: move_z("forward"), bg="lightgreen")
btn3 = tk.Button(left_frame, text="Z-Move Backward", width=20, command=lambda: move_z("backward"), bg="lightyellow")
btn4 = tk.Button(left_frame, text="Fine Alignment", width=20, command=fine_alignment, bg="lightpink")
btn5 = tk.Button(left_frame, text="Find Rotate Center", width=20, command=find_best_center, bg="lightcoral")
btn6 = tk.Button(left_frame, text="Epoxy", width=20, command=epoxy_move, bg="lightsalmon")
btn7 = tk.Button(left_frame, text="Exit", width=20, command=exit_system, bg="lightgray")
btn_monitor = tk.Button(left_frame, text="Start Monitoring", width=20, command=toggle_monitoring, bg="lightcyan")


btn1.pack(pady=5)
btn2.pack(pady=5)
btn3.pack(pady=5)
btn4.pack(pady=5)
btn5.pack(pady=5)
btn6.pack(pady=5)
btn7.pack(pady=5)
btn_monitor.pack(pady=5)


# Right frame: power label and log
lbl_power = tk.Label(right_frame, text="-- dBm", font=("Arial", 32, "bold"), fg="blue")
lbl_power.pack(pady=10)


log_box = scrolledtext.ScrolledText(right_frame, width=60, height=30)
log_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


root.mainloop()