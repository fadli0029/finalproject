float ax = 0;
float ay = 0;
float az = 0;

void setup() {

	Serial.begin(9600);
	setupAccelSensor();

}

void loop() {

	readAccelSensor();

	Serial.print(ax);
	Serial.print(",");
	Serial.print(ay);
	Serial.print(",");
	Serial.println(az);

}
