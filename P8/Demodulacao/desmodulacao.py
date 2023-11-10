import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.io import wavfile
from scipy import signal, fft
from suaBibSignal import signalMeu

# Reproduzir o áudio modulado
audio_modulado, _ = sf.read('P8/audio_modulado.wav')
samplerate = 44100
portadora = 14000
sinal = signalMeu()

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
#sd.play(audio_modulado, samplerate)

# Aguardar a reprodução terminar
sd.wait()

# Aviso antes de normalizar o sinal modulado
print("Reprodução concluída. Agora normalizaremos o sinal modulado.")

# Normalizar o sinal modulado
audio_modulado_normalizado = audio_modulado

# 9. Demodule o áudio enviado no segundo computador (receptor).

portadora = np.sin(2 * np.pi * 14000 * np.arange(len(audio_modulado_normalizado)) / samplerate)
sinal_demodulado = audio_modulado_normalizado * portadora

# 10. Filtre as frequências superiores a 4kHz.
sinal_demodulado_filtrado = filtrar(sinal_demodulado)
sd.play(sinal_demodulado_filtrado, samplerate)

# 11. Execute o áudio do sinal demodulado e verifique que novamente é audível.
wavfile.write('P8/audio_demodulado_filtrado.wav', samplerate, np.array(sinal_demodulado_filtrado))
audio_demodulado_filtrado, _ = sf.read('P8/audio_demodulado_filtrado.wav')

# Aviso antes de plotar os gráficos
print("Agora plotaremos os gráficos.")

# 12. Gráfico 6: Sinal de áudio demodulado – domínio do tempo.
plt.figure()
plt.plot(sinal_demodulado)
plt.title('Sinal de Áudio Demodulado - Tempo')
plt.show()

# 13. Gráfico 7: Sinal de áudio demodulado – domínio da frequência.
sinal.plotFFT(sinal_demodulado, samplerate)
plt.title('Sinal de áudio demodulado domínio da frequência')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude')
plt.show()

# 14. Gráfico 8: Sinal de áudio demodulado e filtrado – domínio da frequência.

sinal.plotFFT(sinal_demodulado_filtrado, samplerate)
plt.title('Sinal de áudio demodulado e filtrado domínio da frequência')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude')
plt.show()

sd.play(audio_demodulado_filtrado, samplerate)

# Aguarde a reprodução terminar
sd.wait()