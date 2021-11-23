int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())

bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  writeDisplay("Sleep", 0, true);

  sending = false;
}

void loop() {

  String command = receiveMessage();

  if (command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }

  else if (command == "wearable") {
    sending = true;
    writeDisplay("testing", 0, true);
  }

  else {
    // receive steps count from MCU
    String out = "Jumps: " + String(command);
    writeDisplay(out.c_str(), 1, true);
  }

  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }

}
