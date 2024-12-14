# Rocket_Code

This repository contains code for a model rocket project. The code is designed to control a gimbaled motor and measure environmental parameters such as temperature, pressure, and altitude. While the data visualization (GUI) is functional, it can be improved with features like axis labels and unit indicators. Feel free to enhance the code to suit your needs!

* Construction of the rocket

You will need to 3D print the gimbal and use the servo motors to control the gimbal. You will need to modify the STL to fit servo motors and diameter of the rocket you choose. You can use a mailing tube as the body. 

There is plenty of videos on youtube where you can find out how to hook up an ESP32 to the compenents I used. I did not use the ESP32 camara.

* Here is a list of the compents I used: 


<img width="470" alt="Screenshot 2024-12-13 at 5 48 48 PM" src="https://github.com/user-attachments/assets/00ad938a-d9aa-489a-a0c1-da45097566e3" />


* I 3D printed the nose code and gimbal. Below are the links to 3D prints:

https://www.thingiverse.com/thing:3657663/files​

https://www.thingiverse.com/thing:4564390

You will need to bend a hanger or something of that nature to connect the gimbal to the body of the rocket motor housing. 


<img width="129" alt="Screenshot 2024-12-13 at 5 48 04 PM" src="https://github.com/user-attachments/assets/57c8f838-21dc-4016-897d-8fefdf7e58e7" />



**Overview of code**

The main.c file will control the motor gimbal keepting the rocket in verticle position throughout flight. The Main.c file logs the position, speed, altitude, atmospheric pressure, and atmospheric temperature to an SD card located on the rocket using a Zittop SD card reader/writer. 

The main.py file visulizes the data from data logged to the SD card. 


**Things to keep in mind**

I advise using Replit.com so you do not have to download Python package on a local IDE. 

You will need to take the SD card out of the rocket after flight and plug it into your computer. After you run the code you will need to click "open file". Ensure your .txt file is named "sample_telemetry_data". If it is not updated to this then you will need to change the def main funcation that opens the "sample_telemetry_data.txt" file. Below is the code you will need to update if you change the name of your .txt file. 

      def main():
          app = TelemetryGUI()
          telemetry_processor = TelemetryProcessor()
          telemetry_processor.read_telemetry_data("sample_telemetry_data.txt") #edit this line
          for data in telemetry_processor.data:
              print(data)
          app.mainloop()



This repository contains two main programs designed for telemetry data processing and collection:

* Note: I have included a unit test file for the Main.py file. I have also included an example of what the data will look like on the SD card. I used Arduino IDE to upload code to ESP32. 

**Python GUI Application (main.py)**

This program provides a graphical user interface (GUI) for processing and visualizing telemetry data. It is built using Python with the tkinter library for the GUI and matplotlib for plotting the data.

* Features:
    * Data Parsing
      * Reads telemetry data from text files that are saved to an onboard SD card.
      * Parses data from MPU6050 accelerometer, servo motors, BMP390 temperature/pressure sensor, and altitude readings.
* Visualization:
  * Displays graphs of accelerometer readings, servo positions, temperature, pressure, and altitude over time.
* GUI Functionality:
  * Users can load telemetry data files using a file dialog.
  * Data is displayed graphically for easy analysis.
* Object-Oriented Design:
  * TelemetryData and TelemetryProcessor classes manage data parsing and organization.
* How to Use:
  * Run main.py to launch the GUI.
  * Use the "Open File" button to load a telemetry data file for visualization.
  * Modify the file paths in the code to test with your telemetry data file.

**Embedded C Data Collection Program (main.c)**

This program is designed for microcontrollers (e.g., ESP32) and is responsible for collecting telemetry data from hardware sensors and saving it to an SD card.

* Features:
  * Sensor Integration:
    * Reads temperature, pressure, and altitude data from the BMP390 sensor.
    * Reads accelerometer data from the MPU6050 sensor.
    * Controls servo motor positions based on accelerometer readings.
  * Data Logging:
    * Logs sensor data to an SD card in real-time.
    * Appends data to separate files (/bmpData.txt and /mpuData.txt).
* Hardware Configuration:
  * Configures I2C communication for MPU6050 and BMP390 sensors.
  * Initializes servos connected to designated pins.
* Dynamic Control:
  * Adjusts servo positions dynamically based on accelerometer readings.
* How to Use:
  * Deploy the code to an ESP32 or compatible microcontroller.
  * Ensure the SD card is correctly connected and configured.
  * Observe telemetry data output via serial monitor and in saved SD card files.

**Combined Usage:**
The embedded C program (main.c) collects telemetry data and saves it to an SD card.
The Python GUI application (main.py) processes and visualizes the logged telemetry data.

Future Improvements
* Add axis labels and unit annotations to the plot.
* Implement data transmission using a LoRa hat.
* Improve error handling and file format validation.
* Optimize the GUI layout for better usability.
* GPS to track location after launch. 

Contributions are welcome! Feel free to submit pull requests with improvements or bug fixes.

License

This project is open-source and available under the MIT License.

