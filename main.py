import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TelemetryData:
    def __init__(self, acc_x, acc_y, servo_x, servo_y, temperature, pressure, altitude):
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.servo_x = servo_x
        self.servo_y = servo_y
        self.temperature = temperature
        self.pressure = pressure
        self.altitude = altitude

    def __str__(self):
        return f"AccX: {self.acc_x} g, AccY: {self.acc_y} g, Servo X: {self.servo_x}, Servo Y: {self.servo_y}, Temperature: {self.temperature} *C, Pressure: {self.pressure} hPa, Altitude: {self.altitude} m"

class TelemetryProcessor:
    def __init__(self):
        self.data = []

    def read_telemetry_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "MPU6050" in line:
                        acc_x, acc_y, servo_x, servo_y = self.parse_mpu6050_data(line)
                    elif "Temperature" in line:
                        temperature, pressure, altitude = self.parse_temperature_data(line)
                        self.data.append(TelemetryData(acc_x, acc_y, servo_x, servo_y, temperature, pressure, altitude))
        except Exception as e:
            print(f"Error reading file: {e}")

    def parse_mpu6050_data(self, line):
        data = line.split(", ")
        acc_x = float(data[0].split(": ")[1].strip(" g"))
        acc_y = float(data[1].split(": ")[1].strip(" g"))
        servo_x = int(data[2].split(": ")[1])
        servo_y = int(data[3].split(": ")[1])
        return acc_x, acc_y, servo_x, servo_y

    def parse_temperature_data(self, line):
        data = line.strip().split(", ")
        temperature = float(data[0].split(": ")[1].strip(" *C"))
        pressure = float(data[1].split(": ")[1].strip(" hPa"))
        altitude = float(data[2].split(": ")[1].strip(" m"))
        return temperature, pressure, altitude

class TelemetryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Telemetry Data Processor")

        self.open_button = tk.Button(self, text="Open File", command=self.open_file)
        self.open_button.pack()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.telemetry_processor = TelemetryProcessor()
            self.telemetry_processor.read_telemetry_data(file_path)
            self.display_data()

    def display_data(self):
        x = range(len(self.telemetry_processor.data))
        acc_x = [data.acc_x for data in self.telemetry_processor.data]
        acc_y = [data.acc_y for data in self.telemetry_processor.data]
        servo_x = [data.servo_x for data in self.telemetry_processor.data]
        servo_y = [data.servo_y for data in self.telemetry_processor.data]
        temperature = [data.temperature for data in self.telemetry_processor.data]
        pressure = [data.pressure for data in self.telemetry_processor.data]
        altitude = [data.altitude for data in self.telemetry_processor.data]

        self.ax.plot(x, acc_x, label="AccX")
        self.ax.plot(x, acc_y, label="AccY")
        self.ax.plot(x, servo_x, label="ServoX")
        self.ax.plot(x, servo_y, label="ServoY")
        self.ax.plot(x, temperature, label="Temperature")
        self.ax.plot(x, pressure, label="Pressure")
        self.ax.plot(x, altitude, label="Altitude")
        self.ax.legend()

        self.canvas.draw()

def main():
    # Create GUI
    app = TelemetryGUI()
    telemetry_processor = TelemetryProcessor()
    telemetry_processor.read_telemetry_data("sample_telemetry_data.txt")
    for data in telemetry_processor.data:
        print(data)
    app.mainloop()

if __name__ == "__main__":
    main()