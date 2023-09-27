#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
from utils import *
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
       
       #bit de sacrificio
        com1.sendData(b'\x00')
        time.sleep(1)

        #carregando imagem
        imagemR = "client\imagem.png"
        imagem_bytes = open(imagemR, "rb").read()
        #tamanho = len(txBuffer)    

        #comecando a transmissao de pacotes
        handshake(com1)
       
        payloads,qtd = monta_payloads(imagem_bytes, len(imagem_bytes))
        pacotes = monta_pacotes(payloads, qtd,0)

        #enviando pacotes
        for pacote in pacotes:
            com1.sendData(pacote)
            print("Pacote enviado")
            print(pacote)
            time.sleep(0.1)
        
            data,_ = com1.getData(15)
            print(data[0])
            time.sleep(0.1)
            if data[0] == b'\x07':
                pass
            else:
                print("Erro no pacote")
                print(data)
                com1.sendData(pacote)
                time.sleep(0.1)
            
       
        
    
    

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
