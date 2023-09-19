import time
import numpy as np
from math import ceil

HEAD_handshake_server = bytes([5,1,0,0,0,0,0,0,0,0,0,0])

EOP = bytes([0,0,0]) # Montando o EOP


def atualiza_tempo(tempo_ref):
    tempo_atual = float(time.time())
    referencia = float(tempo_atual-tempo_ref)
    return referencia 

def verifica_handshake(head, is_server):
    """
    Função que verifica se o handshake é a resposta esperada (SIM)
    """
    handshake = head[:2] # primeiro e segundo bytes do head
    delta_t = 0
    conferencia = bytes([5,1])
    if not is_server:
        conferencia = bytes([4,0])
    while delta_t <= 5: # loop para gerar o timeout
        tempo_atual = float(time.time())
        if handshake == conferencia: # 5 é a mensagem de handshake e 1 é a resposta positiva
            print('Handshake realizado com sucesso')
            return True
        delta_t = atualiza_tempo(tempo_atual)
    return False

def verifica_eop(pacote, head):
    """
    Função que verifica se o payload é o mesmo que o esperado e se o pacote está correto
    """
    tamanho = head[2]
    eop = pacote[12+tamanho:]
    if eop == b'\x00\x00\x00':
        print('Payload recebido integramente. Esperando novo pacote')
        return True
    print('Erro no EOP enviado. Tente novamente.')
    return False

def verifica_ordem(recebido, numero_do_pacote_atual):
    """
    Como combinado o byte que diz o número do pacote é o de número 4 do head ,
    função que será utilizada pelo server
    """
    head = recebido[0:13]
    numero_do_pacote = head[3]
    if numero_do_pacote == numero_do_pacote_atual:
        return True
    return False

def monta_payload(informacao):
    """
    Lembremos que o payload tem tamanho máximo de 50 bytes, então se uma informação tiver um tamanho maior
    terá que enviar pacotes de 50 ou menos até que a informação inteira seja recebida
    """
    tamanho = len(informacao)
    pacotes = ceil(tamanho/50)
    payloads = []
    for i in range(pacotes):
        if i == (pacotes-1):
            payload = informacao[50*i:tamanho]
            print('tamanho do ultimo payload ' , len(payload))
        else:
            payload = informacao[50*i:(i+1)*50]
            print('tamanho dos payloads intermediarios : ',len(payload))
        payloads.append(payload)
    return payloads

def reagrupamento(lista_dos_payloads,tamanho_total_da_info, numero_de_pacotes_recebidos):
    """
    Nessa função iremos juntar os payloads dos pacotes recebidos e verificar se o número de pacotes recebidos foi correto 
    """
    info_total = ''
    for payload in lista_dos_payloads:
        info_total += payload
    
    if numero_de_pacotes_recebidos == tamanho_total_da_info:
        return True
    else:
        return False
        
def tratar_pacote_recebido(pacote):
    head = pacote[0:12]

    tamanho = head[2]
    payload = pacote[12:12+tamanho]

    eop = pacote[12+tamanho:len(pacote)]

    return head,payload,eop
    

def retirando_informacoes_do_head(head):
    tamanho_do_payload = head[2]
    numero_do_pacote = head[3]
    numero_total_de_pacotes = head[4]

    return tamanho_do_payload,numero_do_pacote, numero_total_de_pacotes