int pinoServidor = 8; // número do pino usado pelo Arduino para receber dados
float baudrate = 9600; // 9600 bits por segundo
int mensagem;

void setup() {
  pinMode(pinoServidor, INPUT); // define o pino digital como entrada, já que o servidor está recebendo dados do cliente
  Serial.begin(baudrate); // inicia a porta serial, configurando a taxa de recebimento de dados para 9600 bits por segundo
}

float aguardarTempo(float tempoDeEspera = 1, float baudrate = 9600, float T0 = 0){
  double clock = 1 / (16 * pow(10, 6)); // tempo de 1 clock (T = 1/frequência), onde a frequência = 21MHz
  double T = 1 / baudrate; // tempo entre cada clock, em segundos
  int numeroDeClocks = floor(T / clock) + 1; // número de clocks a esperar, arredondado para o inteiro mais próximo
  for (int i = 0; i < int(numeroDeClocks * tempoDeEspera); i++){ asm("NOP"); } // aguarde o tempo especificado
}

void loop() {
  if (digitalRead(pinoServidor) == 0){
    int quantidadeDe1s = 0;
    aguardarTempo(1.5); // posicionando o momento de leitura dos bits no meio de cada bit (portanto, o bit de início é ignorado)
    for (int i = 0; i < 8; i++){
      int bitAtual = digitalRead(pinoServidor); // leia o bit atual
      aguardarTempo(); // sempre chamado após a leitura de um bit
      if (bitAtual == 1){ quantidadeDe1s++; } // conte a quantidade de 1s na mensagem
      mensagem |= (bitAtual << i); // adicione o bit atual à mensagem
    }
    int bitDeParidadeRecebido = digitalRead(pinoServidor); // leia o bit de paridade recebido
    int bitDeParidadeCalculado = (quantidadeDe1s % 2); // calcule o bit de paridade a partir da mensagem enviada
    if (bitDeParidadeRecebido == bitDeParidadeCalculado){ // se o bit de paridade recebido for igual ao bit de paridade calculado, a mensagem está correta
      Serial.print("Dados recebidos: ");
      Serial.println(char(mensagem));
      Serial.println("O bit de paridade está correto");
    } else { // se o bit de paridade recebido for diferente do bit de paridade calculado, a mensagem está incorreta
      Serial.println("ERRO. O bit de paridade NÃO está correto");
    }
    for (int i = 0; i < 2084; i++){ // envie
      aguardarTempo();
    }
  }
}
