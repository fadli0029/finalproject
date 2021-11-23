/* 
   	to increment counter, so that I can keep track if x seconds
	have passed 
*/ 
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



