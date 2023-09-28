import crcmod
from math import ceil

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
            print('tamanho do ultimo payload ' , len(payload))
        else:
            payload = informacao[114*i:(i+1)*114]
            print('tamanho dos payloads intermediarios : ',len(payload))
        payloads.append(payload)
    return payloads

img = 'client/img/imageW.png'; img_bin = open(img,'rb').read() # id = 1
payloads_list = monta_payload(img_bin) # Lista com a imagem divida em varios payloads

payload = payloads_list[3]

crc16 = crcmod.predefined.Crc('crc-16')
crc16.update(payload)
crc_bytes = crc16.crcValue.to_bytes(2, byteorder='little')
# byte1 = crc_bytes[0]
# byte2 = crc_bytes[1]

CRC = b""
# CRC += bytes([byte1])
# CRC += bytes([byte2])

print(crc16.crcValue.to_bytes(2, byteorder='big'))
# print(bytes([byte1]))
# print(bytes([byte2]))
print(crc16)