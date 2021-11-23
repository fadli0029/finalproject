/*
   In this .ino file, I make functions to handle
   timed events. I could've just put it in the main
   .ino file, but i'd like to keep things more organized
*/
const long oneSec = 1000; 
const long pointFiveSec = 500; 
long prevMillis = 0;
bool secPassed(unsigned long nowMillis, const long sec) {
	bool stat = false;
	if (nowMillis - prevMillis >= sec) {
		stat = true;
		prevMillis = nowMillis;
	}
	return stat;
}
