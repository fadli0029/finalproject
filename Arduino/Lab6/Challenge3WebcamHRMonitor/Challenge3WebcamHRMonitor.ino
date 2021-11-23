/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupCommunication();
  setupDisplay();
  writeDisplay("Sleep", 0, true, false);
}

/*
 * The main processing loop
 */
void loop() {
  String command = receiveMessage();

  if(command == "sleep") {
    writeDisplay("Sleep", 0, true, false);
  }
  else if(command == "wearable") {
    writeDisplay("Wearable", 0, true, false);
  }

  else if(command == "measuring") {
    writeDisplay("Heart Rate: ", 0, true, false);
    writeDisplay("measuring...", 1, true, false);
  }

  else {
    String HR = String(command);
    writeDisplay(HR.c_str(), 2, false, true);
  }
}
