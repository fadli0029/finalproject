int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;
int counter = 0; // for displaying message for x seconds

const int buzzerPin = 13;
int fsm_state = 0;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  pinMode(buzzerPin, OUTPUT);
  writeDisplay("Sleep", 0, true);
  sending = false;
}

void loop() {

  unsigned long currentMillis = millis();

  String command = receiveMessage();
  
  if (command == "sleep") { // check command received
    sending = false;
    writeDisplay("Sleep", 0, true);
  }

  else if (command == "wearable") { // check command received
    sending = true;
    writeDisplay("Wearable", 0, true);
  }

  if (sending && sampleSensors()) { 
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
    // send data to be intepreted by our .py program
  }

  switch (fsm_state) {
    case 0: // neutral (i.e: state checking)
      if (oneSecPassed(currentMillis) == true) {
        digitalWrite(buzzerPin, LOW);
      }
      if (command == "walk") {
        fsm_state = 1;
      }
      else if (command == "Good") {
        fsm_state = 2;
      }
      break;

    case 1: // inactive state
      writeDisplay("Go WALK!", 0, true);
      digitalWrite(buzzerPin, HIGH);
      if (oneSecPassed(currentMillis) == true) {
        counter++;
      }
      if (counter == 1) {
        counter = 0;   // reset counter
        digitalWrite(buzzerPin, LOW);
        fsm_state = 0; // go to case 0, to check state again
      }
      break;

    case 2: // active state
      writeDisplay("Good!", 0, true);
      fsm_state = 0; // go to case 0, to check state again
      break;
  }
  sending = true;
}
