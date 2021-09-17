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
import numpy as np
import os

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName2 = "COM4"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com2 = enlace(serialName2)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com2.enable()
        print("primeiro checkpoint, comunicação aberta")
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
        
        rxmensagem, nRxmensagem = com2.getData(14)
        print(rxmensagem)
        print("Handshake recebido!")

        if rxmensagem == b'Mandando!!Fim!':
            answer = head+EOP
            com2.sendData(answer)

            print("Enviado com sucesso")

        recebido = 0
        
        rxPacote1, rxPacote1size = com2.getData(128)
        print("recebeu {}" .format(rxPacote1size))

        rxPacote1 = rxPacote1.decode("utf-8")
        pacote = rxPacote1[9]

        if pacote == recebido+1:
            print("Pacote {} recebido".format(pacote))
            recebido+=1

        rxPacote2, rxPacote2size = com2.getData(100)
        print("recebeu {}" .format(rxPacote2size))

        rxPacote2 = rxPacote2.decode("utf-8")
        pacote = rxPacote2[9]

        if pacote == recebido+1:
            print("Pacote {} recebido".format(pacote))
            recebido+=1



        imgWrite = "comandos.txt"

        with open(imgWrite, "wb") as imagem:
            imagem.write(rxBuffer)
            imagem.close()

        com2.sendData(rxBuffersize)
        print("Devolveu o tamanho!!!")
            
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()