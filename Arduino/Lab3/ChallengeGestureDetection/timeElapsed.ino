/*
   In this .ino file, I make functions to handle
   timed events. I could've just put it in the main
   .ino file, but i'd like to keep things more organized
*/


/* EVENTS */


// To decrement every 1 second, for the COUNTDOWN state
const long decrement = 1000;
long decrement_prevMillis = 0;
void decrementTaps(unsigned long nowMillis) {
	if (nowMillis - decrement_prevMillis >= decrement) {
		if (numTaps > 0 && buttonStatus(nowMillis) == false) {
			numTaps--;
			// decrement numTaps, as long as it's more than 0
			// and button is not pushed more than 2 secs
		}
		if (numTaps == 0 && buttonStatus(nowMillis) == false) {
			FSM_state = 3; 
			// numTaps is 0, buzzer should be turned on
			// so enter state 3, provided that button
			// is not pushed more than 2 seconds
		}
		if (buttonStatus(nowMillis) == true) {
			FSM_state = 1;
			// if button is pushed more than 2 secs
			// enter reset state regardless
			// of numTaps value
		}
		decrement_prevMillis = nowMillis; // reset
	}
}


// to increment counter, so that I can keep track if 4 seconds
// have passed after a tap is detected in the detectTaps() method
const long oneSec = 1000; 
long oneSec_prevMillis = 0;
bool oneSecPassed(unsigned long nowMillis) {
	bool stat = false;
	if (nowMillis - oneSec_prevMillis >= oneSec) {
		stat = true;
		oneSec_prevMillis = nowMillis;
	}
	return stat;
}



