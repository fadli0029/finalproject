// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
const int buttonPin = 12;

bool sending, oldStatus, isShoot;

int currentState = 0;
int lastButtonState;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  oldStatus = false;  // for button/buzzer
  isShoot = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);

  pinMode(buttonPin, INPUT_PULLUP);
}

/*
 * The main processing loop
 */
void loop() {
  unsigned long currentMillis = millis();

  /*BUTTON STATE CHECKING*/
  currentState = !digitalRead(buttonPin);
  if (currentState != lastButtonState) { 
    if (oldStatus) {
      isShoot = false;
    }
    if (oldStatus == false) {
      isShoot = true;
    }
  }
  lastButtonState = currentState;

  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);

    if (isShoot) {
      sendMessage(String(2) + "," + response);
    }
    else {
      sendMessage(String(7) + "," + response);
    }
  }
  oldStatus = isShoot;
}
