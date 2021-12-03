// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
const int buttonPin = /*0;*/ 12;

bool sending, oldStatus, isShoot;

int currentState = 0;
int lastButtonState;
bool vibrate = false;
unsigned long timer1 = millis();
/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupMotor();
  sending = false;    // activate/deactivate receiving acclerometer value
  oldStatus = false;  // for button/buzzer
  isShoot = false;    // to detect if button is pressed

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
  else if(command == "Dead") { // player loose :(
    sending = false;
    writeDisplay("You Died!!!", 0, true);
    vibrate = true;
    timer1 = currentMillis;
    activateMotor(255); // buzz motor
  }
  else if(command == "Hit") { // player is hit by buller
    writeDisplay("You've been Hit!", 0, true);
    vibrate = true;
    timer1 = currentMillis;
    activateMotor(255); // buzz motor
  }
  else if (command != ""){
    writeDisplayCSV(command,1);
  }
  if(sending && sampleSensors()) {
    // receives sensor values
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);

    if (isShoot) {
      // player pressed button, he's firing!
      sendMessage(String(2) + "," + response);
    }
    else {
      // player didn't pressed button, he's not firing
      sendMessage(String(7) + "," + response);
    }
  }
  if(vibrate && (currentMillis - timer1 >500)){
    vibrate = false;
    deactivateMotor();
  }
  oldStatus = isShoot;
}
