int pinoCliente = 7; // número do pino usado pelo Arduino para enviar dados
char mensagem = 'G'; // letra 'A' em hexadecimal
int mensagemBinaria = int(mensagem); // letra 'A' convertida de hexadecimal para binário
float baudrate = 9600; // 9600 bits por segundo

void setup() {
  pinMode(pinoCliente, OUTPUT); // define o pino digital como saída, já que o cliente está enviando para o servidor
  Serial.begin(baudrate); // inicia a porta serial, configurando a taxa de envio de dados para 9600 bits por segundo
  digitalWrite(pinoCliente, HIGH); // comece com o pino em nível alto (1)
}

float aguardarTempo(float tempoDeEspera = 1, float baudrate = 9600, float T0 = 0){
  double clock = 1 / (16 * pow(10, 6)); // tempo de 1 clock (T = 1/frequência), onde a frequência = 16MHz
  double T = 1 / baudrate; // tempo entre cada clock, em segundos
  int numeroDeClocks = floor(T / clock) + 1; // número de clocks a esperar, arredondado para o inteiro mais próximo
  for (int i = 0; i < int(numeroDeClocks * tempoDeEspera); i++){ asm("NOP"); } // aguarde o tempo especificado
}

void loop() {
  int quantidadeDe1s = 0; // contador para a quantidade de 1s na mensagem

  digitalWrite(pinoCliente, 0); // envie o bit de início
  aguardarTempo(); // sempre chamado após o envio de um bit

  for (int i = 0; i < 8; i++){ // envie os 8 bits (1 byte) da mensagem
    int bitAtual = 1 & (mensagemBinaria >> i); // obtenha o bit atual da mensagem, começando pelo bit menos significativo
    digitalWrite(pinoCliente, bitAtual); // envie o bit atual
    if (bitAtual == 1){ quantidadeDe1s++; } // conte a quantidade de 1s na mensagem
    aguardarTempo(); // sempre chamado após o envio de um bit
  }

  int bitDeParidade = quantidadeDe1s % 2; // se o resto for igual a 0, então é par, senão é ímpar
  digitalWrite(pinoCliente, bitDeParidade); // envie o bit de paridade
  aguardarTempo(); // sempre chamado após o envio de um bit

  digitalWrite(pinoCliente, 1); // envie o bit de parada
  aguardarTempo(); // sempre chamado após o envio de um bit

  Serial.print("Dados enviados: ");
  Serial.println(mensagem); // imprime a mensagem enviada (em hexadecimal)

  for (int i = 0; i < 2084; i++){ // envie
    aguardarTempo();
  }
  
}
