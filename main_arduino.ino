#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
int contor = 7200;
Adafruit_MPU6050 mpu;

const int keyPin = A0;

const int soundSensorPin = A0;  // Sound sensor analog pin
const int snapThreshold = 600;  // Adjust this threshold based on your environment

void setup(void) {
  Serial.begin(9600);
  while (!Serial)
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens

  // Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    // Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  delay(100);
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  // Serial.print("Acceleration X: ");
  // Serial.print(a.acceleration.x);
  // Serial.print(", Y: ");
  // Serial.print(a.acceleration.y);
  // Serial.print(", Z: ");
  // Serial.print(a.acceleration.z);
  // Serial.println(" m/s^2");

  // Serial.print("Rotation X: ");
  // Serial.print(g.gyro.x);
  // Serial.print(", Y: ");
  // Serial.print(g.gyro.y);
  // Serial.print(", Z: ");
  // Serial.print(g.gyro.z);
  // Serial.println(" rad/s");

  if (a.acceleration.y < -7.0) {
    Serial.println(contor + 1000000);
  } else {
    int keyState = analogRead(keyPin);
    if (keyState < 1000 && a.acceleration.y < 3) {
      contor = -1000000 - contor;
      Serial.println(contor);
      delay(400);
      contor *= -1;
      contor = contor - 1000000;
    }
    if (contor > 1000000) {
      contor = contor - 1000000;
    }
    if (a.acceleration.x > 8.0) {
      contor++;
      Serial.println(contor);
      delay(400);
    }
    if (a.acceleration.x < -8.0) {
      contor--;
      Serial.println(contor);
      delay(400);
    }
    Serial.println(contor);
  }
  delay(100);  //Default 100
}
