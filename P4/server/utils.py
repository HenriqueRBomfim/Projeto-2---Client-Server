import time
import numpy as np
from math import ceil

HEAD_handshake_server = bytes([2,1,0,0,0,0,0,0,0,0,0,0])

EOP = b'\xAA\xBB\xCC\xDD' # Montando o EOP


def atualiza_tempo(tempo_ref):
    tempo_atual = float(time.time())
    referencia = float(tempo_atual-tempo_ref)
    return referencia 

def verifica_handshake(head, is_server):
    """
    Função que verifica se o handshake é a resposta esperada (SIM)
    """
    handshake = head[:2] # primeiro a quinto  byte do head
    delta_t = 0
    conferencia = bytes([1,35])
    #if not is_server:
        #conferencia = bytes([2,0])
    while delta_t <= 5: # loop para gerar o timeout
        tempo_atual = float(time.time()//1)
        if handshake == conferencia: # 5 é a mensagem de handshake e 1 é a resposta positiva
            print('Handshake realizado com sucesso')
            return True
        delta_t = atualiza_tempo(tempo_atual)
    return False

def verifica_eop(pacote, head):
    """
    Função que verifica se o payload é o mesmo que o esperado e se o pacote está correto
    """
    # head = pacote[:10]
    tamanho = head[5]
    eop = pacote[10 + tamanho:]
    if eop == b'\xAA\xBB\xCC\xDD':
        print(f'Payload {head[4]} de {head[3]} recebido integramente. Esperando novo pacote')
        

        return True
    print('Erro no EOP enviado. Tente novamente.')
    return False

def verifica_ordem(recebido, numero_do_pacote_atual):
    """
    Como combinado o byte que diz o número do pacote é o de número 4 do head ,
    função que será utilizada pelo server
    """
    head = recebido[0:10]
    ultimo_pacote_sucesso = head[7]
    if ultimo_pacote_sucesso == numero_do_pacote_atual:
        return True
    return False

def monta_payload(informacao):
    """
    Lembremos que o payload tem tamanho máximo de 50 bytes, então se uma informação tiver um tamanho maior
    terá que enviar pacotes de 50 ou menos até que a informação inteira seja recebida
    """
    tamanho = len(informacao)
    pacotes = ceil(tamanho/114)
    payloads = []
    for i in range(pacotes):
        if i == (pacotes-1):
            payload = informacao[114*i:tamanho]
            print(f'tamanho do ultimo payload { len(payload)}')
        else:
            payload = informacao[114*i:(i+1)*114]
            print(f'tamanho dos payloads intermediarios :{len(payload)} ')
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

    tamanho_pacote = len(pacote)
    head = pacote[0:10]

    tamanho = head[5] #acho que é tamanho do payload
    payload = pacote[10:10+tamanho]

    eop = pacote[10+tamanho:len(pacote)]
    # eop = pacote[tamanho_pacote-4:tamanho_pacote]

    return head,payload,eop
    

def retirando_informacoes_do_head(head):

    # tamanho_pacote = len(pacote)
    # head = pacote[0:10]
    tipo_de_mensagem = head[0]
    numero_total_de_pacotes = head[3]
    numero_do_pacote = head[4]
    variavel = head[5] 
    pacote_erro = head[6]
    ultimo_pacote_sucesso = head[7]

    return tipo_de_mensagem, numero_total_de_pacotes, numero_do_pacote, variavel, pacote_erro, ultimo_pacote_sucesso
    
def verifica_pacote(pacote):
    tipo_de_mensagem, numero_total_de_pacotes, numero_do_pacote, variavel, pacote_erro, ultimo_pacote_sucesso = retirando_informacoes_do_head(pacote[:10])
    if tipo_de_mensagem == 3:
        if variavel != len(pacote) - 14:
            return False
        elif len(pacote) > 128 or len(pacote) < 14:
            return False
        if numero_do_pacote != ultimo_pacote_sucesso + 1:
            return False
        if not verifica_eop(pacote, pacote[:10]):
            return False
    return True 
    
    
