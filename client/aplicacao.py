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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)

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
        
        comando_1 = b'\x00\x00\x00\x00'
        comando_2 = b'\x00\x00\xBB\x00'
        comando_3 = b'\xBB\x00\x00'
        comando_4 = b'\x00\xBB\x00'
        comando_5 = b'\x00\x00\xBB'
        comando_6 = b'\x00\xAA'
        comando_7 = b'\xBB\x00'
        comando_8 = b'\x00'
        comando_9 = b'\xBB'
        comandos = [comando_1, comando_2, comando_3, comando_4, comando_5, comando_6, comando_7, comando_8, comando_9]

        N = random.randint(10, 30)

        comandos_a_serem_enviados = []

        i = 0
        while i < N:
            comandos_a_serem_enviados.append(comandos[random.randint(0, 8)])
            i += 1

        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        #print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        print ("A transmissão vai começar")

        bitFim = b'\xCC'
        bitErro = b'\xDD'
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        
        i = 0
        while i < N:
            item_da_lista = comandos[random.randint(0, 8)]
            tamanho = len(item_da_lista)
            enviar = bytes([tamanho])

            print('enviado tamanho', np.asarray(enviar))

            com1.sendData(np.asarray(enviar))
            time.sleep(0.2)
            com1.sendData(np.asarray(item_da_lista))
            print('mostrando o byte enviado ' ,item_da_lista)
            time.sleep(0.2)

            print("Comando número: ", i)

            i += 1
        
        com1.sendData(np.asarray(bitFim))
        print("Enviou Bit Fim")
        
        tempo_inicial = time.time()//1
        while com1.rx.getIsEmpty():
            tempo2 = time.time()//1
            if ((tempo2 - tempo_inicial) >= 5):
                print("time out")
                break
        else:
            rxBuffer, nRx = com1.getData(1)
            Nrecebido = rxBuffer[0]
            print("Recebeu {} comandos" .format(Nrecebido))
            if Nrecebido != N:
                com1.sendData(bitErro)
                print("Inconsistência no número de comandos")

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
