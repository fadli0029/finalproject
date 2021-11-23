/*
 * Global variables
 */
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending, sendDate, oldStatus, buzzIt;

int currentState = 0;
int lastButtonState;
const int buzzerPin = 13;
const int buttonPin = 12;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupCommunication();
  setupDisplay();

  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);

  setupAccelSensor();
  setupPhotoSensor();

  sendDate = false;   // for button
  oldStatus = false;  // for button/buzzer
  sending = false;    // for triggering data sending
  buzzIt = false;     // for buzzer

  writeDisplay("Sleep", 0, true, false);
}

/*
 * The main processing loop
 */
void loop() {

  unsigned long currentMillis = millis();

  /*BUTTON STATE CHECKING*/
  currentState = !digitalRead(buttonPin);
  if (currentState != lastButtonState) { 
    if (oldStatus == true) {
      sendDate = false;
      buzzIt = false;
    }
    if (oldStatus == false) {
      sendDate = true;
      buzzIt = true;
    }
  }
  lastButtonState = currentState;

  if (sendDate == true) {
    Serial.print('m');
  }

  if (buzzIt == true) {
    // buzz the buzzer for x second(s)
    digitalWrite(buzzerPin, HIGH);
  }
  if (secPassed(currentMillis, 500)) {
    digitalWrite(buzzerPin, LOW);
  }
  oldStatus = sendDate;

  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true, false);
  }
  else if(command == " ") {
    sending = true;
    writeDisplay(" ", 0, true, false);
  }

  else {
    String val = String(command);

    String hr = "";             // 'h'
    String mystep = "";         // 'x'
    String time = "";           // 't'
    String weather_date = "";   // 'q'

    int i, j, k, l;
    if (val.charAt(0) == 'h') {
      for (i = 1; val[i] != 'x'; i++) {
        hr += val[i];
      }
      for (j = i+1; val[j] != 't'; j++) {
        mystep += val[j];
      }
      for (k = j+1; val[k] != 'q'; k++) {
        time += val[k];
      }
      for (l = k+1; val[l] != 'z'; l++) {
        weather_date += val[l];
      }
    }

    String hr_out = "Heart Rate: " + hr;
    String mystep_out = "Steps Count: " + mystep;
    String time_out = "Time: " + time;
    String weather_date_out = "^_^ " + weather_date;
    writeDisplay(hr_out.c_str(), 0, false, true);
    writeDisplay(mystep_out.c_str(), 1, false, true);
    writeDisplay(time_out.c_str(), 2, false, true);
    writeDisplay(weather_date_out.c_str(), 3, false, true);
  }

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ppg) + ","; 
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);
  }

}
