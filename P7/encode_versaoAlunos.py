
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Frequências DTMF em Hz
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

# Função para gerar o sinal DTMF
def generate_dtmf_signal(number, duration=2, fs=44100):
    # Cria uma sequência de tempo 't' que representa o intervalo de tempo para a geração do sinal.
    # A sequência começa em 0 e vai até a 'duration' especificada, com 'int(fs * duration)' pontos no total.
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Obtém as frequências DTMF correspondentes ao número escolhido a partir do dicionário 'dtmf_freqs'.
    # 'freq1' e 'freq2' representam as duas frequências que compõem o sinal DTMF.
    freq1, freq2 = dtmf_freqs[number]
    
    # Gera um sinal DTMF somando duas senoides: uma com frequência 'freq1' e outra com frequência 'freq2'.
    signal = np.sin(2 * np.pi * freq1 * t) + np.sin(2 * np.pi * freq2 * t)
    
    # Retorna o sinal DTMF gerado.
    return signal

#funções a serem utilizadas
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    
    print("Inicializando encoder")
    print("Aguardando usuário")
    number = int(input("Digite o número que quer transmitir (0-9): "))
    
    if number not in dtmf_freqs:
        print("Número inválido. Escolha um número de 0 a 9.")
        return
    
    fs = 44100  # Taxa de amostragem
    duration = 2  # Duração em segundos

    # Gerar o sinal DTMF
    dtmf_signal = generate_dtmf_signal(number, duration, fs)

    print(f"Gerando tons para o número: {number}")
    
    # Emitir o som
    sd.play(dtmf_signal, fs)

    # Exibir o gráfico no domínio do tempo
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.title("Sinal no Domínio do Tempo")
    plt.plot(np.arange(0, duration, 1/fs), dtmf_signal)
    plt.xlabel("Tempo (s)")
    plt.grid()

    # Calcular e exibir a transformada de Fourier
    plt.subplot(2, 1, 2)
    plt.title("Transformada de Fourier")
    plt.specgram(dtmf_signal, Fs=fs, NFFT=1024, noverlap=512, cmap='viridis')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Frequência (Hz)")
    plt.grid()

    plt.tight_layout()
    plt.show()

    # Aguardar o fim do áudio
    sd.wait()

    # Opcional: Salvar o sinal em um arquivo WAV
    filename = f"dtmf_{number}.wav"
    scaled_signal = np.int16(dtmf_signal * 32767)  # Scale to 16-bit integer
    write(filename, fs, scaled_signal)
    print(f"Sinal salvo em {filename}")
    
if __name__ == "__main__":
    main()
