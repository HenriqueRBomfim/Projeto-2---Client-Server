const int txPin = 7; // Pino digital usado para transmitir os dados
const int baudrate = 9600; // Taxa de baud (bps)
const byte dado = 'A'; // Dado a ser transmitido (no exemplo, 'A')

void setup() {
  pinMode(txPin, OUTPUT);
  Serial.begin(baudrate);
}

void loop() {
  digitalWrite(txPin, HIGH); // ativa o pino digital 13         // espera por um segundo
  delay(1000)
  digitalWrite(txPin, LOW);  // desativa o pino digital 13 
}
