#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
from random import randint
import numpy as np
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        print("primeiro checkpoint, comunicação aberta")
        timeinicial = time.time()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
    

    
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
        
        answer = 0
        
        while answer != 1:
            vivo = 3
            vivo = vivo.to_bytes(2, byteorder="big")
            com1.sendData(vivo)
            timestart = time.time()
            answer, answerlen = com1.getData(1)
            answer = int.from_bytes(answer, "big")
            print("Resposta recebida")
            timefinal = time.time()
            print(timefinal-timestart)
            if timefinal-timestart > 5:
                tentar = input("Servidor inativo. Tentar novamente? S/N")
                if tentar == "S":
                    pass
                elif tentar == "N":
                    com1.disable()
                    exit()  

        Comando1 = "00FF"
        Comando2 = "00"
        Comando3 = "0F"
        Comando4 = "F0"
        Comando5 = "FF00"
        Comando6 = "FF"

        c = randint(10,30)
        listaComandos = []
        
        for i in range(c):
            n = randint(1,6)
            if n == 1:
                listaComandos.append("2")
                listaComandos.append(Comando1)
            elif n == 2:
                listaComandos.append(Comando2)
            elif n == 3:
                listaComandos.append(Comando3)
            elif n == 4:
                listaComandos.append(Comando4)
            elif n == 5:
                listaComandos.append("2")
                listaComandos.append(Comando5)
            elif n == 6:
                listaComandos.append(Comando6)



        txBuffer = listaComandos #dados
        print(txBuffer)
        txbufferlen = len(txBuffer)
        txBufferhexa = txbufferlen.to_bytes(2, byteorder="big")
        print("txBufferhexa",txBufferhexa)
        com1.sendData(txBufferhexa)
        time.sleep(1)


        txBuffer = np.asarray(txBuffer)
        print(txBuffer)

        
        com1.sendData(txBuffer)
    
        print ("transmissão sucedida!!!")
    
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com1.tx.getStatus()
        #print("txSize:",txSize)

        rxBufferClient, nRxClient = com1.getData(2)
        resposta = int.from_bytes(rxBufferClient, "big")

        if resposta == txbufferlen:
            print("Deu Certo! Não perdeu informação!")
        else:
            print("Deu ruim!!!")

        timefinal = time.time()
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        timetotal = timefinal - timeinicial
        print("tempo:", timetotal)
        com1.disable()
        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
