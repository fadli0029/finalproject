/**********************************
	Variables for ACCELEROMETER 
**********************************/
float ax = 0;
float ay = 0;
float az = 0;
int sampleTime = 0;


/***********************************	
  	Var/Const for BUZZER/TAPS  
***********************************/
const int  buzzerPin = 13;
int numTaps = 0;
int counter = 0;


/***********************************	
  		Var/Const for BUTTONS 
***********************************/
const int  buttonPin = 12;
int currentState = 0;
int lastButtonState = 0;
int startedPushed = 0;
int pushingTime = 0;


/***********************************	
		Initializing FSM STATES  
***********************************/
int FSM_state = 0;


/***********************************	
			FUNCTIONS  :)
***********************************/
int detectTaps(unsigned long watchTime) {
	readAccelSensor();
	if (az < 2350 && ay < 1900 && ax > 1970) {
		numTaps++;
		delay(40); // to remove effect from shock
		counter = 0;
		FSM_state = 0;
		// if this if condition entered, there is a tap
		// so, stay at state 0 and detect taps
		// and reset counter to 0 
	}
	if (oneSecPassed(watchTime) == true) {
		counter++;
		if (counter == 4) {
			FSM_state = 2;
		}
		// this if statement has to be entered
		// 4 times in a row and in every second
		// to make the transition to state 2
		// where there is no tap for 4 secs
	}
	if (buttonStatus(watchTime) == true) {
		FSM_state = 1;
		// regardless of anything, if button is 
		// pushed for 4 secs, enter state 1 and reset numtaps
	}
	return numTaps;
}

void showNumTaps(int tapped) {
	String message = String(tapped);
	writeDisplay(message.c_str(), 3, true);
	// this is just a helper function to 
	// display numTaps on the OLED
}

void messageDisplay(int yourIntMessage, int your_row) {
	String theMsg = String(yourIntMessage);
	writeDisplay(theMsg.c_str(), your_row, true);
	// I sometimes need this when debugging to print
	// things on the OLEd
}

bool buttonStatus(unsigned long watchTime) {
	bool stat = false;
	if (currentState == HIGH) {
		pushingTime = watchTime - startedPushed;
		if (pushingTime >= 2000) {
			stat = true;
		}
	}
	return stat;
	// if button is pressed for 2 secs, this
	// function will return true
}

void startProgram() {
	unsigned long currentMillis = millis();
	currentState = !digitalRead(buttonPin);
	// read button state, and init millis()

	/* refer state diagrams on README.md for complete description */
	switch (FSM_state) {
		case 0: // TAPPING state
			showNumTaps(detectTaps(currentMillis));
			break;

		case 1: // RESET state
			numTaps = 0; // reset numtaps to 0
			showNumTaps(numTaps);
			FSM_state = 3; // go to state 3 bcoz numtap is 0
			break;

		case 2: // COUNTDOWN state
			decrementTaps(currentMillis);
			// decrement numtaps by 1 every second
			showNumTaps(detectTaps(currentMillis));
			break;

		case 3: // BUZZ MOTOR state
			showNumTaps(numTaps);
			digitalWrite(buzzerPin, HIGH);
			// buzz the motor
			break;
	}
}


/***********************************	
			PROGRAMS START.  
***********************************/
void setup() {
	setupAccelSensor();
	setupDisplay();
	pinMode(buzzerPin, OUTPUT);
	pinMode(buttonPin, INPUT_PULLUP);
	Serial.begin(9600);
}

void loop() {
	startProgram();
}
