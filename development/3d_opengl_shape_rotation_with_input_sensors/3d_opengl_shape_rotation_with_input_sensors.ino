/*
 *  3D OpenGL Shape Rotation With Input Sensors.
 *
 *  Copyright (C) 2010 Efstathios Chatzikyriakidis (stathis.chatzikyriakidis@gmail.com)
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

// data type definition for a sensor (each sensor represents a dimension).
typedef struct sensorT {
  int sensorPin; // the pin number for the sensor.
  int sensorMin; // the minimum value of the sensor.
  int sensorMax; // the maximum value of the sensor.
  int sensorVal; // the current value of the sensor.
} sensorT;

// initialize the sensors and set default values.
sensorT sensors[] = {
  {0, 1023, 0, -1}, // sensor for the dimension X.
  {1, 1023, 0, -1}  // sensor for the dimension Y.
};

// calculate the number of the dimensions.
const int NUM_DIMS = (int) (sizeof (sensors) / sizeof (sensors[0]));

// the separator character between the angles.
char sepChar = ':';

// the formatted message which contains the angles.
String msgString;

// calibration status led.
const int ledPin = 13;

// calibration time in millis.
const int CAL_TIME = 15000;

// startup point entry (runs once).
void setup () {
  // set each input sensor as input (each dimension angle data source).
  for(int dim = 0; dim < NUM_DIMS; dim++)
    pinMode(sensors[dim].sensorPin, INPUT);

  // set led as output.
  pinMode(ledPin, OUTPUT);

  // start serial communication.
  Serial.begin(9600);

  // calibrate all sensors at once.
  calibrationPeriod();
}

// loop the main sketch.
void loop () {
  // reset the value of the message.
  msgString = "";
  
  // read sensors' values and send all angles to the serial line.
  for(int dim = 0; dim < NUM_DIMS; dim++) {
    // get a value from the current sensor.
    sensors[dim].sensorVal = analogRead(sensors[dim].sensorPin);
  
    // map the value from the sensor for rotation angle.
    sensors[dim].sensorVal = map(sensors[dim].sensorVal,
                                 sensors[dim].sensorMin,
                                 sensors[dim].sensorMax,
                                 0, 360);

    // place the angle in the string.
    msgString += sensors[dim].sensorVal;

    // place separator character between angle values.
    if (dim < NUM_DIMS-1)
      msgString += sepChar;
  }

  // send group of angles (formatted message) to the serial line.
  Serial.println(msgString);
}

// input sensors calibration process.
void calibrationPeriod () {
  // the value that a sensor sends.
  int sensorValue = -1;

  // signal the start of the calibration period.
  digitalWrite(ledPin, HIGH);

  // calibrate all sensors during some time.
  while (millis() < CAL_TIME) {
    for(int dim = 0; dim < NUM_DIMS; dim++) {
      // get a value from the current sensor.
      sensorValue = analogRead(sensors[dim].sensorPin);

      // record the maximum sensor value.
      if (sensorValue > sensors[dim].sensorMax) {
        sensors[dim].sensorMax = sensorValue;
      }

      // record the minimum sensor value.
      if (sensorValue < sensors[dim].sensorMin) {
        sensors[dim].sensorMin = sensorValue;
      }
    }
  }

  // signal the end of the calibration period.
  digitalWrite(ledPin, LOW);
}
