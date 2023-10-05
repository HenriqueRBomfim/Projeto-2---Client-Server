const int rxPin = 7; // Pino digital usado para receber os dados
const int baudrate = 9600; // Taxa de baud (bps)

void setup() {
  pinMode(rxPin, INPUT);
  Serial.begin(baudrate);
}

void loop() {
  receberByteSerial();
}

void receberByteSerial() {
  while (digitalRead(rxPin) == LOW); // Aguarda o bit de início

  delayMicroseconds(1000000 / baudrate / 2); // Move-se para o meio do bit
  byte dado = 0;

  // Lê os 8 bits de dados (LSB primeiro)
  for (int i = 0; i < 8; i++) {
    delayMicroseconds(1000000 / baudrate);
    dado |= (digitalRead(rxPin) << i);
  }

  delayMicroseconds(1000000 / baudrate / 2); // Move-se para o meio do bit de paridade
  int paridadeRecebida = digitalRead(rxPin);

  delayMicroseconds(1000000 / baudrate / 2); // Move-se para o meio do bit de parada
  int bitParada = digitalRead(rxPin);

  // Verifica a paridade (paridade par)
  int paridadeCalculada = 0;
  for (int i = 0; i < 8; i++) {
    if ((dado >> i) & 1) {
      paridadeCalculada ^= 1; // XOR para calcular a paridade
    }
  }

  // Verifica se a paridade recebida coincide com a paridade calculada
  if (paridadeRecebida == paridadeCalculada && bitParada == HIGH) {
    Serial.print("Byte Recebido: ");
    Serial.println(char(dado));
  }
}
