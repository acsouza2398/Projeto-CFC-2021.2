
#importe as bibliotecas
import numpy as np
import sounddevice as sd
import soundfile as sf
import os as sys
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
from funcoes_LPF import *
import time



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def normalize(audio):
    m = max(abs(audio))
    norm = []
    for i in audio:
        norm.append(i/m)

    return norm

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")

    sinal = signalMeu()

    fs = 44100
    
    
     #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa

    amplitude = 1
    tempo = 1

    print("Tocando o audio gravado")
    
    audio, samplerate = sf.read( sys.path.join(sys.path.dirname(__file__),"Audio.wav"))

    sd.playrec(audio)
    time.sleep(2)

    print("Normalizando")

    norm = normalize(audio)
    time.sleep(1)

    array_tempo = np.linspace(0, tempo, fs*tempo)

    #Gráfico 1: Sinal de áudio original normalizado – domínio do tempo
    plt.plot(array_tempo[:1000], norm[:1000])
    plt.title('Gráfico 1: Sinal de áudio original normalizado – domínio do tempo')
    plt.show()


    print("Filtrando audio e tocando novamente")
    
    filtro = LPF(norm, 4000, fs)

    sd.play(filtro)
    time.sleep(2)

    #Gráfico 2: Sinal de áudio filtrado – domínio do tempo. (repare que não se nota diferença). 
    plt.plot(array_tempo[:1000], filtro[:1000])
    plt.title('Gráfico 2: Sinal de áudio filtrado – domínio do tempo')
    plt.show()

    #Gráfico 3: Sinal de áudio filtrado – domínio da frequência. 
    xfiltro, yfiltro = sinal.calcFFT(filtro, fs)
    plt.plot(xfiltro, yfiltro)
    plt.title('Gráfico 3: Sinal de áudio filtrado – domínio da frequência')
    plt.show()


    print("Modulando para AM")

    #modular = audio og * onda portadora

    xport, yport = sinal.generateSin(14000, amplitude, tempo, fs)

    mod = yport*filtro
    time.sleep(1)

    print("Tocando audio modulado")

    sd.play(mod)
    time.sleep(2)

    #Gráfico 4: sinal de áudio modulado – domínio do tempo (mais uma vez, não se nota diferença)
    plt.title('Gráfico 4: sinal de áudio modulado – domínio do tempo')
    plt.plot(array_tempo[:1000], mod[:1000])
    plt.show()

    # Gráfico 5: sinal de áudio modulado – domínio da frequência
    xmod, ymod = sinal.calcFFT(mod, fs)
    plt.plot(xmod, np.abs(ymod))
    plt.title("Gráfico 5: sinal de áudio modulado – domínio da frequência")
    plt.show()

    print("Demodulando o audio")
    demod = yport*mod
    time.sleep(1)

    # Gráfico 6: sinal de áudio demodulado – domínio da frequência. (verifique que reobteve as baixas frequências)
    xdemod, ydemod = sinal.calcFFT(demod, fs)
    plt.plot(xdemod, np.abs(ydemod))
    plt.title("Gráfico 6: sinal de áudio demodulado – domínio da frequência")
    plt.show()

    print("Filtrando o demodulado")

    filtro_demod = LPF(demod, 4000, fs)

    # Gráfico 7: sinal de áudio demodulado e filtrado – domínio da frequência.
    xfiltro_demod, yfiltro_demod = sinal.calcFFT(filtro_demod, fs)
    plt.plot(xfiltro_demod, np.abs(yfiltro_demod))
    plt.title("Gráfico 7: sinal de áudio demodulado e filtrado – domínio da frequência")
    plt.show()

    print("Tocando audio demodulado e filtrado")

    sd.play(filtro_demod)
    time.sleep(2)

    sd.wait()

    '''
    sd.play(tone, fs)
    # Exibe gráficos
    plt.plot(array_tempo[:250], tone[:250], "red")
    plt.title("Frequência do sinal {0}".format(NUM))
    plt.show()

    # plotando fourier
    xf, yf = sinal.calcFFT(tone, fs)
    plt.plot(xf, yf)
    plt.title("Fourier do Sinal Gerado")
    plt.show()

    # aguarda fim do audio
    sd.wait()
    '''

if __name__ == "__main__":
    main()
