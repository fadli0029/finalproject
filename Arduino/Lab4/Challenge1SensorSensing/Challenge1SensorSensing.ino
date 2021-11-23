int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

void setup() {

  /* 
    setup accelerometer,
          communication,
          display.
  */
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);

}

void loop() {

  String command = receiveMessage(); // check message from .py
  if (command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }

  else if (command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }

  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);
    // send data to be intepreted by our .py program
  }

}
