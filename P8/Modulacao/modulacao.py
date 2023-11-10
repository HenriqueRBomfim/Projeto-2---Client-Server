import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.io import wavfile
from scipy import signal, fft
from suaBibSignal import signalMeu

#Aviso antes de gravar o áudio
# print("Aguarde antes de começar a falar. A gravação terá uma duração de 5 segundos.")
# duration = 5  # segundos
# samplerate = 44100
# audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
# sd.wait()
# write('P8/gravacao.wav', samplerate, audio)

# Aviso antes de abrir o arquivo de áudio
print("Gravação concluída. Agora vamos processar o áudio.")

signall = signalMeu()

# Abrir o arquivo de áudio corretamente
yAudio, samplerate = sf.read('P8/gravacao.wav')
max_amplitude = np.max(np.abs(yAudio))
yAudioNormalizado = yAudio / max_amplitude
wavfile.write('P8/audio_normalizado.wav', samplerate, np.array(yAudioNormalizado))

def filtrar(signal):
    a = 0.002988
    b = 0.002834
    c = 1
    d = -1.847
    e = 0.8532
    Ylist = []
    Ylist.append(signal[0])
    Ylist.append(signal[1])
    for i in range(2, len(signal)):
        H = -d * Ylist[i - 1] - e * Ylist[i - 2] + a * signal[i - 1] + b * signal[i - 2]
        Ylist.append(H)
    return Ylist

# # Parâmetros do filtro
# nyq_rate = samplerate / 2
# width = 5.0 / nyq_rate
# ripple_db = 60.0  # dB
# N, beta = signal.kaiserord(ripple_db, width)
# cutoff_hz = 4000.0
# taps = signal.firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))

#taps = filtrar(yAudioNormalizado)

# Aviso antes de filtrar o áudio
print("Áudio carregado. Agora aplicaremos um filtro.")

# Filtrar o áudio corretamente
#yFiltrado = signal.lfilter(taps, 1.0, yAudioNormalizado)
yFiltrado = filtrar(yAudioNormalizado)

# Aviso antes de salvar o áudio filtrado
print("Filtro aplicado. Agora salvaremos o áudio filtrado.")

# Salvar áudio filtrado
wavfile.write('P8/audio_filtrado.wav', samplerate, np.array(yFiltrado))

# Aviso antes de iniciar a modulação em amplitude
print("Áudio filtrado salvo. Agora realizaremos a modulação em amplitude.")

# Modulação em Amplitude (AM)
portadora_freq = 14000.0
portadora = np.sin(2 * np.pi * portadora_freq * np.arange(len(yFiltrado)) / samplerate)
sinal_modulado = yFiltrado * portadora

# Salvar áudio modulado
wavfile.write('P8/audio_modulado.wav', samplerate, np.array(sinal_modulado))

# Aviso antes de reproduzir o áudio modulado
print("Modulação em amplitude concluída. Agora reproduziremos o áudio modulado.")

# Reproduzir o áudio modulado
audio_modulado, _ = sf.read('P8/audio_modulado.wav')

# Aviso antes de normalizar o sinal modulado
print("Reprodução concluída. Agora normalizaremos o sinal modulado.")

# Normalizar o sinal modulado
max_amplitude = np.max(np.abs(sinal_modulado))
sinal_modulado_normalizado = sinal_modulado / max_amplitude

# Aviso antes de plotar os gráficos
print("Sinal normalizado. Agora plotaremos os gráficos.")

# Gráfico 1: Sinal de áudio original normalizado – domínio do tempo
plt.figure()
plt.plot(yAudioNormalizado)
plt.title('Sinal de Áudio Normalizado - Tempo')
plt.show()

# Gráfico 2: Sinal de áudio filtrado – domínio do tempo
plt.figure()
plt.plot(yFiltrado)
plt.title('Sinal de Áudio Filtrado - Tempo')
plt.show()

# Gráfico 3: Sinal de áudio filtrado – domínio da frequência (Fourier)
signall.plotFFT(yFiltrado, samplerate)
plt.title('Sinal de Áudio Filtrado - Frequência')
plt.show()

# Gráfico 4: Sinal de áudio modulado – domínio do tempo
plt.figure()
plt.plot(sinal_modulado)
plt.title('Sinal de Áudio Modulado - Tempo')
plt.show()

# Gráfico 5: Sinal de áudio modulado – domínio da frequência
signall.plotFFT(sinal_modulado, samplerate)
plt.title('Sinal de Áudio Modulado - Frequência')
plt.show()

# Ajustar layout
plt.tight_layout()

