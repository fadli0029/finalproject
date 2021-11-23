/*
 * Global variables
 */
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true, false);
}

/*
 * The main processing loop
 */
void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true, false);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true, false);
  }

  // still measuring BPM (i.e: not 500 samples yet)
  else if(command == "measuring") {
    sending = true;
    writeDisplay("Heart Rate: ", 0, true, false);
    writeDisplay("measuring...", 1, true, false);
  }

  // received BPM measured from python
  // print it out on the OLED
  else {
    String HR = String(command);
    writeDisplay(HR.c_str(), 2, false, true);
  }

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ppg);
    sendMessage(response);
  }
}
