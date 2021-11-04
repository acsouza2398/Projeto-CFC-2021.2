
#importe as bibliotecas
import numpy as np
import sounddevice as sd
import os as sys
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

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
    
    
    duration = 10 #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.
    numero = False
    while not numero:
        try:
            NUM = int(input("Digite um número entre 0 e 9: "))
            break
        except:
            print("Tente novamente, o valor que você digitou não é válido")
    print("Gerando Tom referente ao símbolo : {}".format(NUM))

    if NUM == 1:
        f1 = 1209
        f2 = 697
    elif NUM == 2:
        f1 = 1336
        f2 = 697
    elif NUM == 3:
        f1 = 1477
        f2 = 697
    elif NUM == 4:
        f1 = 1209
        f2 = 770
    elif NUM == 5:
        f1 = 1336
        f2 = 770
    elif NUM == 6:
        f1 = 1477
        f2 = 770
    elif NUM == 7:
        f1 = 1209
        f2 = 852
    elif NUM == 8:
        f1 = 1336
        f2 = 852
    elif NUM == 9:
        f1 = 1477
        f2 = 852
    elif NUM == 0:
        f1 = 1336
        f2 = 941

    tone1_x, tone1_y = sinal.generateSin(f1, amplitude, tempo, fs)
    tone2_x, tone2_y = sinal.generateSin(f2, amplitude, tempo, fs)
    tone = tone1_y + tone2_y

    array_tempo = np.linspace(0, tempo, fs*tempo)

    print("Frequências: {0} + {1}".format(f1, f2))

    
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    
    #printe o grafico no tempo do sinal a ser reproduzido
    # reproduz o som
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

if __name__ == "__main__":
    main()
