#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
import sounddevice as sd
import os as sys
from suaBibSignal import signalMeu
import matplotlib.pyplot as plt
import time
import peakutils

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    tecla = ""
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    signal = signalMeu()

    fs = 44100
    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 10
    #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("Irei começar a escutar em 5 segundos")
    time.sleep(5)
   
    #faca um print informando que a gravacao foi inicializada
    print("A gravação foi iniciada")

    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    tempo = 2
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = fs*tempo
   
    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = []
    for i in range(numAmostras):
        dados.append(audio[i][0])   

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0,tempo,numAmostras)

    # plot do gravico  áudio vs tempo!

    plt.plot(t, dados)
    plt.title("Audio Gravado")
    plt.show()
   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, fs)
    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf,.3,10)
    tol = 10
    
    #printe os picos encontrados!
    print("Picos encontrados: {0}".format(xf[index]))   

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.scatter(xf[index], yf[index], c = "b", label = "Picos", marker = "o")
    plt.grid()
    plt.title('Picos Fourier Audio')
    plt.show()

    #print a tecla.
    if xf[index][0] >= (697-tol) and xf[index][0] <= (697+tol) and xf[index][1] >= (1209-tol) and xf[index][1] <= (1209+tol):
        tecla = 1
    elif xf[index][0] >= 697-tol and xf[index][0] <= 697+tol and xf[index][1] >= 1336-tol and xf[index][1] <= 1336+tol:
        tecla = 2
    elif xf[index][0] >= 697-tol and xf[index][0] <= 697+tol and xf[index][1] >= 1477-tol and xf[index][1] <= 1477+tol:
        tecla = 3
    elif xf[index][0] >= 770-tol and xf[index][0] <= 770+tol and xf[index][1] >= 1209-tol and xf[index][1] <= 1209+tol:
        tecla = 4
    elif xf[index][0] >= 770-tol and xf[index][0] <= 770+tol and xf[index][1] >= 1336-tol and xf[index][1] <= 1336+tol:
        tecla = 5
    elif xf[index][0] >= 770-tol and xf[index][0] <= 770+tol and xf[index][1] >= 1477-tol and xf[index][1] <= 1477+tol:
        tecla = 6
    elif xf[index][0] >= 852-tol and xf[index][0] <= 852+tol and xf[index][1] >= 1209-tol and xf[index][1] <= 1209+tol:
        tecla = 7
    elif xf[index][0] >= 852-tol and xf[index][0] <= 852+tol and xf[index][1] >= 1336-tol and xf[index][1] <= 1336+tol:
        tecla = 8
    elif xf[index][0] >= 852-tol and xf[index][0] <= 852+tol and xf[index][1] >= 1477-tol and xf[index][1] <= 1477+tol:
        tecla = 9
    elif xf[index][0] >= 941-tol and xf[index][0] <= 941+tol and xf[index][1] >= 1336-tol and xf[index][1] <= 1336+tol:
        tecla = 0
  
    print("A tecla original era {0}".format(tecla))

    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
