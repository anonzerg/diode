float resistance = 22.0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  float voltage_A0 = 0.0;
  float voltage_A1 = 0.0;
  float voltage_A2 = 0.0;

  float voltage_diode = 0.0;
  float voltage_resistance = 0.0;
  float current = 0.0;
  
  // read voltage difference from diode and resistance
  voltage_A0 = analogRead(A0);
  voltage_A1 = analogRead(A1);
  voltage_A2 = analogRead(A2);

  voltage_diode = (voltage_A0 - voltage_A1) * 5.0 / 1023.0;
  voltage_resistance = (voltage_A1 - voltage_A2) * 5.0 / 1023.0;
  // current in mA
  current = (voltage_resitance / resistance) * 1000.0;

  Serial.print(voltage_diode);
  Serial.print(" ");
  Serial.print(current);
  Serial.println();
  delay(100);
}
