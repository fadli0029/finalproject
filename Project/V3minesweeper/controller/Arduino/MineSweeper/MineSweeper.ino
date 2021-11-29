// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;              // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0;       // Time of last sample (in Sampling tab)
const int buttonPin1 = 0; /*12;*/
const int buttonPin2 = 0; /*12;*/
int x = 0;
int y = 0;
bool sending, oldStatus1, oldStatus2, isShoot;

int currentState1 = 0;
int lastButtonState1;
int currentState2 = 0;
int lastButtonState2;
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
  sending = false;
  isShoot = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);

  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
}

/*
 * The main processing loop
 */
void loop() {
  //unsigned long currentMillis = millis();

  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }

  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }

  else if(command == "choose") {
    int both = false;
      
    while(1) {
      // print to display
      writeDisplay("Select Tile!", 0, true);
      String h = String(x)+"x"+String(y);
      writeDisplay(h.c_str(), 1, false);
      
      // if button 1 ++
      currentState1 = !digitalRead(buttonPin1);
      if (currentState1 != lastButtonState1) { 
        if (currentState1) {
          x++;
          both = true;
        }
        if(x == 7) {
          x =0;
        }
      }
      lastButtonState1 = currentState1;

      // if button 2 ++
      currentState2 = !digitalRead(buttonPin2);
      if (currentState2 != lastButtonState2) { 
        if (currentState2) {
          y++;
          
        }
        else {
          both = false;
        }
        if(y == 7) {
          y =0;
        }
      }
      lastButtonState2 = currentState2;

      // if button 1 and 2 send and break
      if(both) {
        sendMessage(String(x)+","+ String(y));
        writeDisplay("Selecting",0,true);
        break;
      }
    }
  }

  else if(command !="") {
    writeDisplay("",0,true);
    writeDisplayCSV(command , 1);
  }
  
  if(sending && sampleSensors()) {
    //String response = String(sampleTime) + ",";
    //response += String(ax) + "," + String(ay) + "," + String(az);

    if (isShoot) {
      //sendMessage(String(2) + "," + response);
      sendMessage(String(2));
    }
    else {
      //sendMessage(String(7) + "," + response);
      sendMessage(String(7));
    }
  }
}
