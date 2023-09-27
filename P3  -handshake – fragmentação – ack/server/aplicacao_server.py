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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)



def main():
    try:
        com1 = enlace(serialName); com1.enable() # Ativa comunicacao. Inicia os threads e a comunicação serial
        
        while com1.rx.getIsEmpty():

            print("esperando 1 byte de sacrifício")
            rxBuffer, _ = com1.getData(1); com1.rx.clearBuffer(); time.sleep(.1)
            print('1 byte de sacrifício recebido. Limpou o buffer')

            HEAD_handshake_client, _ = com1.getData(12); time.sleep(.1)
            is_handshake_correct = verifica_handshake(HEAD_handshake_client[0:2], False)
            total_of_packages = HEAD_handshake_client[4]

        if is_handshake_correct:
            payload_size = int(HEAD_handshake_client[2])
            resto_of_handshake_client, _ = com1.getData(payload_size+3) ; time.sleep(.1)
            handshake_client = HEAD_handshake_client + resto_of_handshake_client
            eop_verificado = verifica_eop(handshake_client, HEAD_handshake_client)
            if not eop_verificado:
                return
            handshake_server = np.asarray(HEAD_handshake_server + EOP)
            com1.sendData(handshake_server); time.sleep(.1)
            print('Resposta do handshake enviado')

        img_received = b''
        package_before, packages_received = 1, 0
        while True:
            HEAD_client, _ = com1.getData(12); time.sleep(0.5)
            payload_size, current_package, _ = retirando_informacoes_do_head(HEAD_client)
            print(f'Pacote {current_package} recebido')

            if current_package != package_before:
                #print(f"pacote atual:{current_package},pacote anterior: {package_before}")
                print('Erro na ordem dos pacotes recebidos.')
                HEAD_server = bytes([6,0,0,0,0,0,0,0,0,0,0,0])
                com1.sendData(HEAD_server+EOP); com1.disable(); return
            else:
                HEAD_server = bytes([7,0,0,0,0,0,0,0,0,0,0,0])
                com1.sendData(HEAD_server+EOP); time.sleep(0.5)

            packages_received += 1
            package_before = current_package

            rest_of_package_client, _ = com1.getData(payload_size + 3); time.sleep(0.2)
            package_client = HEAD_client + rest_of_package_client
            
            HEAD_client, payload_client, EOP_client = tratar_pacote_recebido(package_client) #separando head, payloas e eop.
            if len(payload_client) != payload_size:
                print('Tamanho do payload informado é diferente do tamanho real')
                com1.disable(); return
            img_received += payload_client # pegando e guardando as informações do payload
            
            is_eop_correct = verifica_eop(package_client, HEAD_client) #verificando se eop está no lugar certo
            if not is_eop_correct:
                com1.sendData(bytes([6,0,0,0,0,0,0,0,0,0,0,0])+EOP)
                # TODO placeholder para implementacao de reenvio 
                # Aqui quando der erro no eop deve mostrar que ou o EOP esta errado ou o tamanho do payload informado est[a incorreto]]
                
            if packages_received == total_of_packages:
                break
            if packages_received != total_of_packages:
                package_before += 1

        final_HEAD_client = bytes([1,0,0,0,0,0,0,0,0,0,0,0])
        if packages_received != total_of_packages:
            print('Número de pacotes recebidos diferente do total enviado')
        else:
            final_HEAD_client = bytes([1,0,0,0,0,1,0,0,0,0,0,0])
            print('Transmissão foi um sucesso')

        final_package = final_HEAD_client + EOP
        com1.sendData(final_package); time.sleep(.2)
        img_received_name = 'server\imagem.png'
        print("Salvando dados no arquivo")
        f = open(img_received_name, 'wb')
        f.write(img_received)
        f.close() # fecha o arquivo de imagem

        print("-------------------------\nComunicação encerrada\n-------------------------"); com1.disable()
        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
