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

def verifica_eop(pacote, head):
    tamanho = head[2]
    eop = pacote[12+tamanho:]
    print(eop)
    if eop == b'\x00\x00\x00':
        print('Payload recebido integralmente. Esperando um novo pacote')
        return True
    print('Erro no EOP enviado. Tente novamente.')
    return False

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

        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        #print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        print ("A recepção vai começar")

        print("esperando 1 byte de sacrifício")
        rxBuffer, _, check = com1.getData(1)
        com1.rx.clearBuffer()
        print('1 byte de sacrifício recebido. Limpou o buffer')

        time.sleep(0.2)
        
        rxBuffer, nRx, check = com1.getData(15)
        print(rxBuffer)
        time.sleep(.1)
        print(len(rxBuffer))
        print(rxBuffer[0])
        if rxBuffer[0] == 1:
            resposta = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            time.sleep(.2)
            com1.sendData(resposta)
            print("Enviou")

        EOP = b'\x00\x00\x00'

        img = b''
        pacote_anterior = 1
        pacotes_recebidos = 0

        while True:
            erro = False
            print('Esperando pacote')
            HEAD_cliente, _, check = com1.getData(8)
            print(HEAD_cliente)
            time.sleep(0.5)
            total_de_pacotes, pacote_atual, tamanho = HEAD_cliente[0], HEAD_cliente[1], HEAD_cliente[2]
            print(total_de_pacotes)

            if pacote_atual != pacote_anterior:
                print(pacote_atual, pacote_anterior)
                print('Erro na ordem dos pacotes recebidos.')
                HEAD_server = bytes([6,0,0,0,0,0,0,0,0,0,0,0])
                com1.sendData(HEAD_server+EOP)
                erro = True
            else:
                HEAD_server = bytes([7,0,0,0,0,0,0,0,0,0,0,0])
                com1.sendData(HEAD_server+EOP)
                time.sleep(0.5)

            pacotes_recebidos += 1
            pacote_anterior = pacote_atual

            resto_do_pacote, _, check = com1.getData(tamanho + 3)
            time.sleep(0.2)
            package_client = HEAD_cliente + resto_do_pacote
            print(package_client)
            
            HEAD_cliente, payload_client, EOP_client = package_client[0:12], package_client[12:12+tamanho], package_client[12+tamanho:len(package_client)]
            
            eop_certo = verifica_eop(package_client, HEAD_cliente) #verificando se eop está no lugar certo
            if not eop_certo:
                erro = True
                return
                
            if pacotes_recebidos == total_de_pacotes:
                break
            if pacotes_recebidos != total_de_pacotes:
                pacote_anterior += 1
            
            if erro == False:
                img += payload_client # pegando e guardando as informações do payload

        final_HEAD_client = bytes([0,0,0,0,3,0,0,0,0,0,0,0])
        if pacotes_recebidos != total_de_pacotes:
            print('Número de pacotes recebidos diferente do total enviado')
        else:
            final_HEAD_client = bytes([0,0,0,0,2,0,0,0,0,0,0,0])
            print('Transmissão foi um sucesso')

        final_package = final_HEAD_client + EOP
        com1.sendData(final_package); time.sleep(.2)
        img_received_name = '../../P3/img/imageR.png'
        print("Salvando dados no arquivo")
        f = open(img_received_name, 'wb')
        f.write(img)
        f.close() # fecha o arquivo de imagem

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
