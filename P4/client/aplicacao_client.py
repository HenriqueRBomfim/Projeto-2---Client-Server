#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from timeit import repeat
from enlace import *
import time
import numpy as np
from utils import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM6"                  # Windows(variacao de)

def main():
    try:
        with open('log.txt', 'w') as f:
            print("Iniciou o main")
            com1 = enlace(serialName)
            com1.enable()

            print("Abriu a comunicação")
            img = 'img\imageW.png'; img_bin = open(img,'rb').read() # id = 1
            payloads_list = monta_payload(img_bin) # Lista com a imagem divida em varios payloads
            
            # Mensagem tipo 1
            HEAD_handshake = bytes([1,35,0,len(payloads_list),0,1,0,0,0,0]) 
            handshake_client = np.asarray(HEAD_handshake + EOP) # msg tipo 1

            com1.sendData(b'00'); time.sleep(.1) # bit de sacrificio
            com1.sendData(handshake_client); time.sleep(.1)

            inicia = False

            while True:
                com1.rx.clearBuffer()
                timer = time.time()
                while com1.rx.getIsEmpty() and (atualiza_tempo(timer) < 5):
                    pass
                if com1.rx.getIsEmpty():
                    inicia = str(input('Servidor inativo. Tentar novamente? S/N: '))
                    if inicia == 'S':
                        com1.sendData(b'00'); time.sleep(.1) # bit de sacrificio
                        com1.sendData(handshake_client); time.sleep(.1)
                    elif inicia == 'N':
                        print('Servidor inativo. Tente novamente mais tarde.'); com1.disable(); return
                else:
                    handshake_server, _, estourou_tempo = com1.getData(14)
                    # Vê se é mensagem tipo 2
                    is_handshake_correct = verifica_handshake(handshake_server, True)
                    if not is_handshake_correct:
                        print('Handshake diferente do esperado. Tente novamente mais tarde.'); com1.disable(); return
                    elif is_handshake_correct:
                        print("Handshake vindo do server está correto."); break

            current_package = 1
            while current_package <= len(payloads_list):
                payload = payloads_list[current_package - 1]
                tamanho = len(payload)
                # if current_package == 4:
                #     tamanho = len(payload) - 1

                # Mensagem tipo 3
                HEAD_content_client = bytes([3,0,0,len(payloads_list),current_package,tamanho,0,current_package-1,0,0]) 
                package = HEAD_content_client + payload + EOP
                com1.sendData(np.asarray(package))

                # if current_package == 4:
                #     current_package += 1

                estourou_tempo = False
                time_2 = time.time()//1
                
                while (atualiza_tempo(time_2) < 20) and estourou_tempo == True:
                    # Recepção da mensagem tipo 4
                    feedback_to_client, _, estourou_tempo = com1.getData(14) # Tenta pegar por 5 segundos
                    if estourou_tempo == True: # Se passar de 5 segundos entra aqui
                        com1.sendData(np.asarray(package))
                    time.sleep(.1)
                    com1.rx.clearBuffer()
                
                if atualiza_tempo(time_2) >= 20:
                    HEAD_timeout_client = bytes([5,0,0,len(payloads_list),current_package,tamanho,0,current_package-1,0,0]) 
                    package = HEAD_timeout_client + payload + EOP
                    com1.sendData(np.asarray(package))
                    print("-------------------------\nComunicação encerrada\n-------------------------")
                    com1.disable()
                else:
                    if feedback_to_client[0] == b'\x06':
                        erro_server, _, estourou_tempo = com1.getData(14)
                        pacote_certo = int.from_bytes(erro_server[6], "little")
                        current_package = pacote_certo
                        com1.sendData(np.asarray(payloads_list[current_package - 1]))
                        
                if feedback_to_client[0] == b'\x04':
                    print(f'Pacote {current_package} enviado com sucesso.')
                    current_package += 1

                com1.rx.clearBuffer(); time.sleep(.1)

            HEAD_final_server, _, estourou_tempo = com1.getData(10) # Recebendo o HEAD do server
            is_transmission_correct = (HEAD_final_server[2] == 1)
            EOP_final_server, _, estourou_tempo = com1.getData(4) # Recebendo o EOP do server
            package_final_server = HEAD_final_server + EOP_final_server
            is_eop_correct = verifica_eop(package_final_server, HEAD_final_server)

            if not is_transmission_correct:
                print('Erro no envio dos pacotes. Tente novamente.')
            if is_transmission_correct and is_eop_correct:
                print('Transmissão bem sucedida')
        
            print("-------------------------\nComunicação encerrada\n-------------------------"); com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()