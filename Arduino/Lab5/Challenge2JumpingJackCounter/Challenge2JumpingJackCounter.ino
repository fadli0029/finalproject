int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())

int currentState = 0;
int lastButtonState;
const int buttonPin = 12;

bool sending, processingData, oldStatus;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  writeDisplay("Sleep", 0, true);
  pinMode(buttonPin, INPUT_PULLUP);
  processingData = false; // for button
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
    writeDisplay("Jumping Jack!", 0, true);
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

  /*BUTTON STATE CHECKING*/
  currentState = !digitalRead(buttonPin);
  if (currentState != lastButtonState) { // button is pressed
    if (currentState == HIGH) {
      processingData = true;
      if (oldStatus == true) {
        processingData = false;
      }
      if (oldStatus == false) {
        processingData = true;
      }
    }
  }
  lastButtonState = currentState;

  if (processingData == true) {
    // button is pressed
    sending = false;
    Serial.print('m');
    // tell python program to process the data
    // and show jump counts
  }

  else if (processingData == false) {
    // button is not pressed, keep taking data
    sending = true;
  }
  oldStatus = processingData;

}
