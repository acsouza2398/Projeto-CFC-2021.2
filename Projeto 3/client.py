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

        head = 'Mandando!!'
        EOP = "Fim!"

        head = bytes(head, encoding = 'utf-8')
        EOP = bytes(EOP, encoding = 'utf-8')
        
        answer = ""
        
        while answer == "":
            mensagem = head+EOP
            print(mensagem)

            print("Enviando a mensagem")
            com1.sendData(mensagem)
            timestart = time.time()

            answer, answerlen = com1.getData(4)
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

        Comando1 = "00"
        Comando2 = "0F"
        Comando3 = "F0"
        Comando4 = "FF"

        c = 200
        Comandos1 = ""
        Comandos2 = ""
        
        for i in range(c):
            n = randint(1,4)
            if i <= 113:
                if n == 1:
                    Comandos1 = Comandos1 + Comando1
                elif n == 2:
                    Comandos1 = Comandos1 + Comando2
                elif n == 3:
                    Comandos1 = Comandos1 + Comando3
                elif n == 4:
                    Comandos1 = Comandos1 + Comando4
            else:
                if n == 1:
                    Comandos2 = Comandos2 + Comando1
                elif n == 2:
                    Comandos2 = Comandos2 + Comando2
                elif n == 3:
                    Comandos2 = Comandos2 + Comando3
                elif n == 4:
                    Comandos2 = Comandos2 + Comando4


        txBuffer1 = Comandos1
        txBuffer2 = Comandos2 #dados

        #print(txBuffer)
        #txBufferhexa = txbufferlen.to_bytes(2, byteorder="big")
        #print("txBufferhexa",txBufferhexa)

        head1 = "2,pacote 1"
        head2 = "2,pacote 2"

        datagrama1 = head1+txBuffer1+EOP
        datagrama2 = head2+txBuffer2+EOP

        datagrama1 = bytes(datagrama1, encoding = "utf-8")
        datagrama2 = bytes(datagrama2, encoding = "utf-8")

        print("Enviando primeira parte do payload")
        com1.sendData(datagrama1)
        time.sleep(1)

        print("Enviando segunda parte do payload")
        com1.sendData(datagrama2)
        time.sleep(1)
    
        print ("transmissão sucedida!!!")
    
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com1.tx.getStatus()
        #print("txSize:",txSize)

        rxBufferClient, nRxClient = com1.getData(2)
        resposta = int.from_bytes(rxBufferClient, "big")

        if resposta == 200:
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
