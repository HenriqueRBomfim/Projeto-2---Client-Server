import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.io.wavfile import write
from scipy import fft

samplerate = 44100

# Reproduzir o áudio modulado
audio_modulado, _ = sf.read('audio_modulado.wav')
sd.play(audio_modulado, samplerate)

# Aguardar a reprodução terminar
sd.wait()

# Aviso antes de normalizar o sinal modulado
print("Reprodução concluída. Agora normalizaremos o sinal modulado.")

# Normalizar o sinal modulado
max_amplitude = np.max(np.abs(sinal_modulado))
sinal_modulado_normalizado = sinal_modulado / max_amplitude

# Aviso antes de plotar os gráficos
print("Sinal normalizado. Agora plotaremos os gráficos.")

# Gráfico 1: Sinal de áudio original normalizado – domínio do tempo
plt.figure(figsize=(15, 10))
plt.subplot(3, 3, 1)
plt.plot(yAudioNormalizado)
plt.title('Sinal de Áudio Original Normalizado - Tempo')

# Gráfico 2: Sinal de áudio filtrado – domínio do tempo
plt.subplot(3, 3, 2)
plt.plot(yFiltrado)
plt.title('Sinal de Áudio Filtrado - Tempo')

# Gráfico 3: Sinal de áudio filtrado – domínio da frequência (Fourier)
plt.subplot(3, 3, 3)
frequencies, amplitudes = fft.fftfreq(len(yFiltrado), 1/samplerate), np.abs(fft.fft(yFiltrado))
plt.plot(frequencies, amplitudes)
plt.title('Sinal de Áudio Filtrado - Frequência')

# Demodulação
demodulado = filtrar(sinal_modulado_normalizado)

# Gráfico 4: Sinal de áudio demodulado – domínio do tempo
plt.subplot(3, 3, 4)
plt.plot(demodulado)
plt.title('Sinal de Áudio Demodulado - Tempo')

# Gráfico 5: Sinal de áudio demodulado – domínio da frequência
plt.subplot(3, 3, 5)
frequencies_demod, amplitudes_demod = fft.fftfreq(len(demodulado), 1/samplerate), np.abs(fft.fft(demodulado))
plt.plot(frequencies_demod, amplitudes_demod)
plt.title('Sinal de Áudio Demodulado - Frequência')

# Filtragem
sinal_filtrado = filtrar(demodulado)

# Gráfico 6: Sinal de áudio demodulado e filtrado – domínio do tempo
plt.subplot(3, 3, 6)
plt.plot(sinal_filtrado)
plt.title('Sinal de Áudio Demodulado e Filtrado - Tempo')

# Gráfico 7: Sinal de áudio demodulado e filtrado – domínio da frequência
plt.subplot(3, 3, 7)
frequencies_filtrado, amplitudes_filtrado = fft.fftfreq(len(sinal_filtrado), 1/samplerate), np.abs(fft.fft(sinal_filtrado))
plt.plot(frequencies_filtrado, amplitudes_filtrado)
plt.title('Sinal de Áudio Demodulado e Filtrado - Frequência')

# Ajustar layout
plt.tight_layout()

# Mostrar os gráficos
plt.show()

# Aviso antes de reproduzir o áudio demodulado e filtrado
print("Gráficos exibidos. Agora reproduziremos o áudio demodulado e filtrado.")

# Reproduzir o áudio demodulado e filtrado
sd.play(sinal_filtrado, samplerate)

# Aguardar a reprodução terminar
sd.wait()