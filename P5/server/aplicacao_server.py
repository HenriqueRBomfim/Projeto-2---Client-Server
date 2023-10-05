#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from operator import truediv
from enlace import *
import time
import numpy as np
from utils import *
import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu  (variacao de)
#serialName = "/dev/tty.usbmodem1411"  # Mac     (variacao de)
serialName = "COM4"                    # Windows (variacao de)


def main():
    try:
        com1 = enlace(serialName); com1.enable()
        with open('Server4.txt', 'w') as f:
             # Ativa comunicacao. Inicia os threads e a comunicação serial
            
            

            ocioso = com1.rx.getIsEmpty()
            print('Esperando o cliente se conectar')
            print("esperando 1 byte de sacrifício")
            rxBuffer, _ = com1.getData(1); 
            com1.rx.clearBuffer(); time.sleep(.1)
            print('1 byte de sacrifício recebido. Limpou o buffer')
            HEAD_handshake_client, _  = com1.getData(10); time.sleep(.1)
            f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +"/recebido/ 1 / 14 /" '\n')
            is_handshake_correct = verifica_handshake(HEAD_handshake_client[0:2], False)
            print('verifiquei handshake') #verificando se o handshake é o esperado


            if is_handshake_correct:
                payload_size = int(HEAD_handshake_client[5])
                total_of_packages = HEAD_handshake_client[3]
                resto_of_handshake_client, _ = com1.getData(4) ; time.sleep(.1)
                print(f'passou do datateste')
                handshake_client = HEAD_handshake_client + resto_of_handshake_client
                handshake_server = np.asarray(HEAD_handshake_server + EOP)
                com1.sendData(handshake_server); time.sleep(.1) #mensagem do tipo2
                f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +"/enviado/ 2 / 14" '\n')
                print('Resposta do handshake enviado')

            img_received = b''
            package_before, packages_received = 0, 0
            cont = 1
            
            
            while cont <= total_of_packages:
                estourou_tempo = False
                time_2 = time.time()//1
                
                while (atualiza_tempo(time_2) < 20) and cont <= total_of_packages:
                    time1 = time.time()//1
                    while atualiza_tempo(time1) < 2:
                        if cont <= total_of_packages: 
                            HEAD_client, _  = com1.getData(10); time.sleep(.1)
                            #print(f'HEAD_client: {HEAD_client}')
                            #print(f'cont: {cont}')
                            tipo_de_mensagem,total_of_packages, current_package, variavel, pacote_erro, ultimo_pacote_sucesso, crc1,crc2 = retirando_informacoes_do_head(HEAD_client) 
                            CRC = b""
                            CRC += bytes([crc1])
                            CRC += bytes([crc2])
                            CRC = int.from_bytes(CRC, byteorder='little')
                            print(f'')
                            #print(f' tipo da mensagem: {tipo_de_mensagem}')
                            if tipo_de_mensagem == 5:
                                print('chegou na mensagem tipo 5')
                                f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +"/recebido/ 5 / 14" '\n')
                                print('Tempo de espera excedido')
                                print("-------------------------\nComunicação encerrada\n-------------------------"); com1.disable()
                                
                                
                            if tipo_de_mensagem == 3:
                                time_2 = time.time()
                                packages_received += 1
                                print('chegou na mensagem tipo 3')
                                rest_of_package_client, _ = com1.getData(variavel + 4); time.sleep(.1)
                                package_client = HEAD_client + rest_of_package_client
                                f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/recebido/ 3 / {variavel + 14 }/{current_package}/{total_of_packages}/{hex(CRC)}" '\n')
                                HEAD_client, payload_client, EOP_client = tratar_pacote_recebido(package_client) #separando head, payloas e eop.

                                if not verifica_pacote(package_client):
                                    com1.sendData(bytes([6,0,0,0,0,0,ultimo_pacote_sucesso + 1 ,0,0,0])+EOP)
                                    print('Pacote com erro')
                                    f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +"/enviado/ 6 / 14" '\n')

                                    
                                else:
                                    print(f'Pacote {current_package} recebido')
                                    #com1.sendData(bytes([4,0,0,0,0,0,0,ultimo_pacote_sucesso,0,0])+EOP)
                                    #f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +"/enviado/ 4 / 14" '\n')
                                    cont += 1
                                    #print('mensagem tipo 4 enviada')
                                    img_received += payload_client # pegando e guardando as informações do payload
                        
                if atualiza_tempo(time_2) >= 20:
                    ocioso = True
                    com1.sendData(bytes([5,0,0,0,0,0,current_package,0,0,0])+EOP)
                    print('Tempo de espera excedido')
                    f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +"/enviado/ 5 / 14" '\n')
                    com1.disable()
                
                
            if cont != total_of_packages + 1:
                print('Número de pacotes recebidos diferente do total enviado')

            else:
                with open('img_received.jpg', 'wb') as img:
                    img.write(img_received)
                print('Transmissão foi um sucesso')
                print('Salvando dados no arquivo')
            
     
        print("-------------------------\nComunicação encerrada\n-------------------------"); com1.disable()
        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
