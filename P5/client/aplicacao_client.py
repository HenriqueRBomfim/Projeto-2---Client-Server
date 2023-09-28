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
import datetime
import crcmod

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def main():
    try:
        with open('client/Client3.txt', 'w') as f:
            print("Iniciou o main")
            com1 = enlace(serialName)
            com1.enable()

            print("Abriu a comunicação")
            img = 'client/img/imageW.png'; img_bin = open(img,'rb').read() # id = 1
            payloads_list = monta_payload(img_bin) # Lista com a imagem divida em varios payloads
            
            # Mensagem tipo 1
            HEAD_handshake = bytes([1,35,0,len(payloads_list),0,1,0,0,0,0]) 
            handshake_client = np.asarray(HEAD_handshake + EOP) # msg tipo 1

            com1.sendData(b'00'); time.sleep(.1) # bit de sacrificio
            com1.sendData(handshake_client); time.sleep(.1)
            f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/envio/ 1 / {0 + 14 }/" '\n')
            print('Handshake enviado. Esperando resposta do servidor.')

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
                        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/envio/ 1 / {0 + 14 }/" '\n')
                    elif inicia == 'N':
                        print('Servidor inativo. Tente novamente mais tarde.'); com1.disable(); return
                else:
                    handshake_server, _, estourou_tempo = com1.getData(14)
                    f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/receb/ 2 / {0 + 14 }/" '\n')
                    # Vê se é mensagem tipo 2
                    print('Handshake está certo')
                    is_handshake_correct = verifica_handshake(handshake_server, True)
                    print('Verificou o handshake')
                    if not is_handshake_correct:
                        print('Handshake diferente do esperado. Tente novamente mais tarde.'); com1.disable(); return
                    elif is_handshake_correct:
                        print("Handshake vindo do server está correto."); break

            current_package = 1
            ultimo_pacote_certo = 0
            permissao = True
            while current_package <= len(payloads_list):
                payload = payloads_list[current_package - 1]
                tamanho = len(payload)
                # if current_package == 4:
                #     tamanho = len(payload) - 1

                if current_package == 4 and permissao == True:
                    current_package += 1

                print("Ultimo pacote certo: ", ultimo_pacote_certo)
                print("Pacote atual: ", current_package)

                crc16 = crcmod.predefined.Crc('crc-16')
                crc16.update(payload)
                crc_bytes = crc16.crcValue.to_bytes(2, byteorder='little')
                byte1 = crc_bytes[0]
                byte2 = crc_bytes[1]
                CRC = b""
                CRC += bytes([byte1])
                CRC += bytes([byte2])

                # Mensagem tipo 3
                HEAD_content_client = bytes([3,0,0,len(payloads_list),current_package,tamanho,0,ultimo_pacote_certo,byte1,byte2]) 
                package = HEAD_content_client + payload + EOP

                estourou_tempo = True
                time_2 = time.time()//1
                
                while (atualiza_tempo(time_2) < 20) and (estourou_tempo == True):
                    # Recepção da mensagem tipo 4
                    feedback_to_client, _, estourou_tempo = com1.getData(14) # Tenta pegar por 5 segundos
                    if feedback_to_client != None:
                        print("Feedback",feedback_to_client)
                    if estourou_tempo == True: # Se passar de 5 segundos entra aqui
                        com1.sendData(np.asarray(package))
                        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/envio/ 3 / {tamanho + 14 }/{current_package}/{len(payloads_list)}/{hex(int.from_bytes(CRC, byteorder='little'))}" '\n')
                    time.sleep(.1)
                    com1.rx.clearBuffer()
                
                if atualiza_tempo(time_2) >= 20:
                    HEAD_timeout_client = bytes([5,0,0,len(payloads_list),current_package,tamanho,0,ultimo_pacote_certo,0,0]) 
                    package = HEAD_timeout_client + EOP
                    com1.sendData(np.asarray(package))
                    f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/envio/ 5 / {tamanho + 14 }/{current_package}/{len(payloads_list)}/" '\n')
                    print("--------------------------------------\nComunicação encerrada por tempo limite excedido\n--------------------------------------")
                    com1.disable()
                    break
                else:
                    if feedback_to_client[0] == 4:
                        ultimo_pacote_certo += 1
                        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/receb/ 4 / {tamanho + 14 }/{current_package}/{len(payloads_list)}/" '\n')
                        print(f'Pacote {current_package} enviado com sucesso.')
                        current_package += 1
                    elif feedback_to_client[0] == 6:
                        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/receb/ 6 / {tamanho + 14 }/{current_package}/{len(payloads_list)}/" '\n')
                        pacote_certo = feedback_to_client[6]
                        current_package = pacote_certo
                        permissao = False
                        com1.sendData(np.asarray(HEAD_content_client + payloads_list[current_package - 1] + EOP))
                        print("com1")
                        f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' - ' +f"/envio/ 3 / {tamanho + 14 }/{current_package}/{len(payloads_list)}/" '\n')

                com1.rx.clearBuffer(); time.sleep(.1)

            if current_package >= len(payloads_list):
                print('Transmissão bem sucedida')
                print("-------------------------\nComunicação encerrada\n-------------------------"); com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()