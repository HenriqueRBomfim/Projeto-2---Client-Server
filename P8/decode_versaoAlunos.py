
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import os

# Frequências DTMF em Hz
# dtmf_freqs = [[941, 1336],[697, 1209],[697, 1336],[697, 1477],[770, 1209],[770, 1336],[770, 1477],[852, 1209],[852, 1336],[852, 1477]]
dtmf_freqs = {
    1: (697, 1209),
    2: (697, 1336),
    3: (697, 1477),
    4: (770, 1209),
    5: (770, 1336),
    6: (770, 1477),
    7: (852, 1209),
    8: (852, 1336),
    9: (852, 1477),
    0: (941, 1336),
}

#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2 # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = 4 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    freqDeAmostragem = 44100 #taxa de amostragem
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = freqDeAmostragem * duration

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    print("...     A captação começará em 3 segundos")

    #use um time.sleep para a espera
    time.sleep(3)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("...     Gravação inicializada")

    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1) 
    #audio = os.path.join(os.path.dirname(__file__), 'dtmf_9.wav')
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    #print(audio)
    dados = audio[:,0]
  
    #y = dados[0]
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, duration, numAmostras, endpoint=False)
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, freqDeAmostragem)
    signal.plotFFT(dados, freqDeAmostragem)
    # Encontre os picos no espectro da transformada de Fourier
    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.1, min_dist=100)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    picos = []
    xpico1 = 0
    xpico2 = 0
    for pico in index:
        #print("Pico em {} Hz".format(xf[pico]))
        valor = xf[pico]
        if valor >=690 and valor <= 950:
            xpico1 = valor 
        elif valor >= 1200 and valor <= 1500:
            xpico2 = valor
        
    picos = [xpico1, xpico2]
    

    
    print(picos)
    
    tecla = 0
    for tupla in dtmf_freqs.values():
        if (tupla[0] + 20) > picos[0] > (tupla[0] - 20):
            if (tupla[1] + 20) > picos[1] > (tupla[1] - 20):
                tecla = list(dtmf_freqs.keys())[list(dtmf_freqs.values()).index(tupla)]
                break
            
    print("A tecla pressionada foi: {}".format(tecla))
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
