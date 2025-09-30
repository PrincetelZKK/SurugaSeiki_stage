# A GUI for SURUGA SEIKI stage, collimator <-> collimator
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow is needed for JPG or large PNGs
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import sys

# Dummy programs
def program_1(stop_event, update_plot):
    x = []
    y = []
    for i in range(100):
        if stop_event.is_set():
            break
        x.append(i)
        y.append(i * i)
        update_plot(x, y)
        time.sleep(0.1)

def program_2(stop_event, update_plot):
    x = []
    y = []
    for i in range(100):
        if stop_event.is_set():
            break
        x.append(i)
        y.append(i ** 0.5)
        update_plot(x, y)
        time.sleep(0.1)

programs = {
    "Quick Align": program_1,
    "Square Root": program_2
}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SURUGA SEIKI Collimator Alignment")

        self.stop_event = threading.Event()
        self.thread = None

        # Load and display image (change path to your own image file)
        image = Image.open("Princetel Logo.png")  # ← Replace with your image file path
        image = image.resize((200, 100))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(root, image=self.photo)
        self.image_label.pack(pady=10)

        # Dropdown menu
        self.program_var = tk.StringVar(value="Quick Align")
        self.program_menu = ttk.Combobox(root, textvariable=self.program_var, values=list(programs.keys()))
        self.program_menu.pack(pady=5)

        # Buttons
        self.run_button = ttk.Button(root, text="Run", command=self.run_program)
        self.run_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_program)
        self.stop_button.pack(pady=5)

        # Matplotlib plot
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label="Insertion Loss")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Insertion Loss")
        self.ax.grid(True)
        self.ax.legend()
        # self.canvas.draw()

        # Store data
        self.x_data = []
        self.y_data = []
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Coordinate display frame
        coord_frame = ttk.LabelFrame(root, text="Coordinates", padding=10)
        coord_frame.pack(padx=10, pady=10, fill="x")

        # Labels and Entry boxes for coordinates
        self.coord_vars = {}
        coord_labels = [("X (µm)", "x"), ("Y (µm)", "y"), ("Z (µm)", "z"),
                        ("Tx (°)", "tx"), ("Ty (°)", "ty"), ("Tz (°)", "tz")]

        for i, (label_text, key) in enumerate(coord_labels):
            ttk.Label(coord_frame, text=label_text).grid(row=0, column=i, padx=5)
            var = tk.StringVar(value="0.0")
            entry = ttk.Entry(coord_frame, textvariable=var, width=10, justify='center')
            entry.grid(row=1, column=i, padx=5)
            self.coord_vars[key] = var

        self.save_button = ttk.Button(root, text="Save Coordinates", command=self.save_coordinates)
        self.save_button.pack(pady=5)

    def update_plot(self, x, y):
        # self.ax.set_xlabel("Time")
        # self.ax.set_ylabel("Insertion Loss")
        self.ax.grid(True)
        self.x_data = x
        self.y_data = y
        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()              # Adjust axes limits
        self.ax.autoscale_view()     # Autoscale to new data
        self.canvas.draw()

    def run_program(self):
        self.stop_event.clear()
        selected_program = programs[self.program_var.get()]
        self.thread = threading.Thread(target=selected_program, args=(self.stop_event, self.update_plot))
        self.thread.start()

    def stop_program(self):
        self.stop_event.set()

    def save_coordinates(self):
        # Get current timestamp for filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"coordinates_{timestamp}.txt"

        # Read current coordinate values
        coords = {k: v.get() for k, v in self.coord_vars.items()}

        # Save to text file
        with open(filename, "w") as f:
            f.write("Coordinates Snapshot\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("-------------------------\n")
            f.write(f"X (µm):  {coords['x']}\n")
            f.write(f"Y (µm):  {coords['y']}\n")
            f.write(f"Z (µm):  {coords['z']}\n")
            f.write(f"Tx (°):  {coords['tx']}\n")
            f.write(f"Ty (°):  {coords['ty']}\n")
            f.write(f"Tz (°):  {coords['tz']}\n")

        print(f"Saved coordinates to {filename}")

root = tk.Tk()
app = App(root)
root.mainloop()
