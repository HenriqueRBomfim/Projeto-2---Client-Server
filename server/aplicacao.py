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
       
        
        timeout = 5
        #acesso aos bytes recebidos
        comando_1 = b'\x00\x00\x00\x00'
        comando_2 = b'\x00\x00\xBB\x00'
        comando_3 = b'\xBB\x00\x00'
        comando_4 = b'\x00\xBB\x00'
        comando_5 = b'\x00\x00\xBB'
        comando_6 = b'\x00\xAA'
        comando_7 = b'\xBB\x00'
        comando_8 = b'\x00'
        comando_9 = b'\xBB'
        
        byteFim = b'\xCC'
        #txLen = len(txBuffer)
        
        #byte para dizer o tamanho do comando
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        print(rxBuffer)
        com1.rx.clearBuffer()
        print('limpou')
        time.sleep(.1)
       
        recebidos = 0
        comandos = []
        
       
        while rxBuffer[0] != byteFim:
            print("recebendo lenght do comando")
            rxBuffer,nRx = com1.getData(1)
            time.sleep(.2)
            
            clen = int.from_bytes(rxBuffer, byteorder="little")
            time.sleep(.5)
            
            if clen == 204:
                break
            
            else:
                print(f'o tamanho do comando esperado é: {clen}')
                time.sleep(.1)
                
                rxBuffer,nRx = com1.getData(clen)
                print(f'recebi: {rxBuffer}')
                comandos.append(rxBuffer)
                time.sleep(.1)
            

        
        print('')
        print(f'o número de comandos recebidos foi: {len(comandos)}')
        print('')
        
        #caso inconsistente
        comprimento_err = len(comandos) + 1
        comprimento = len(comandos)
        Ncomandos = int.to_bytes(comprimento_err,length=comprimento_rr,byteorder="little")
        #com1.sendData(np.asarray(Ncomandos))
    
        for cmd in comandos:
            print(cmd)
    
        
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
