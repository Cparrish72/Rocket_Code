#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include <MPU6050_tockn.h>
#include <ESP32Servo.h>
#include "FS.h"
#include "SD.h"
#include "SPI.h"

// MPU6050
#define MPU_SCL_PIN 22
#define MPU_SDA_PIN 21

// Servo motor pins
#define SERVO_X_PIN 13
#define SERVO_Y_PIN 14

// BMP390
#define BMP_SDA_PIN 33
#define BMP_SCL_PIN 32

#define SEALEVELPRESSURE_HPA (1013.25)

// SD Card pins
#define SD_CS 5
#define SD_MOSI 23
#define SD_MISO 19
#define SD_SCK 18

Adafruit_BMP3XX bmp;
MPU6050 mpu6050(Wire1);
Servo servoX;
Servo servoY;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  // SD Card setup
  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
  if (!SD.begin(SD_CS)) {
    Serial.println("Card Mount Failed");
    return;
  }

  // MPU6050 setup
  Wire1.begin(MPU_SDA_PIN, MPU_SCL_PIN);
  mpu6050.begin();

  // Servo setup
  servoX.attach(SERVO_X_PIN);
  servoY.attach(SERVO_Y_PIN);
  servoX.write(90); // Initial position, 90 degrees
  servoY.write(90); // Initial position, 90 degrees

  // BMP390 setup
  Wire.begin(BMP_SDA_PIN, BMP_SCL_PIN);

  if (!bmp.begin_I2C()) { // hardware I2C mode, can pass in address & alt Wire
    Serial.println("Could not find a valid BMP3 sensor, check wiring!");
    while (1);
  }

  // Set up oversampling and filter initialization
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);
}

void loop() {
  if (!bmp.performReading()) {
    Serial.println("Failed to perform BMP3XX reading :(");
  } else {
    String bmpData = "Temperature: " + String(bmp.temperature) + " *C, Pressure: " + String(bmp.pressure / 100.0) + " hPa, Approx. Altitude: " + String(bmp.readAltitude(SEALEVELPRESSURE_HPA)) + " m\n";
    Serial.print(bmpData);

    // Write BMP390 data to SD card
    appendFile(SD, "/bmpData.txt", bmpData.c_str());
  }

  // MPU6050 code
  mpu6050.update();

  int servoXPos = map(mpu6050.getAccX() * 1000, -1000, 1000, 0, 180);
  int servoYPos = map(mpu6050.getAccY() * 1000, -1000, 1000, 0, 180);

  servoX.write(servoXPos);
  servoY.write(servoYPos);

  String mpuData = "MPU6050 AccX: " + String(mpu6050.getAccX()) + " g, AccY: " + String(mpu6050.getAccY()) + " g, Servo X Position: " + String(servoXPos) + ", Servo Y Position: " + String(servoYPos) + "\n";
  Serial.print(mpuData);

  // Write MPU6050 data to SD card
  appendFile(SD, "/mpuData.txt", mpuData.c_str());

  delay(10);
}

void appendFile(fs::FS &fs, const char *path, const char *message) {
  Serial.printf("Appending to file: %s\n", path);

  File file = fs.open(path, FILE_APPEND);
  if (!file) {
    Serial.println("Failed to open file for appending");
    return;
  }
  if (file.print(message)) {
    Serial.println("Message appended");
  } else {
    Serial.println("Append failed");
  }
  file.close();
}
