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
import math

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

        head = b'Mandando!!'
        EOP = b'\x00\x00\x00\x00'
        
        answer = ""

        #Handshake
        
        while answer == "":
            mensagem = head+EOP

            print("Enviando a mensagem")
            com1.sendData(mensagem)
            timestart = time.time()

            answer, answerlen = com1.getData(14)
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


        #Montando o Datagrama

        filepath = "./payload.txt"
        sizePayload = 114 

        print("Montando os pacotes")

        QntPackages = []
        with open(filepath, "rb") as file:
            payload_bin = bytearray(file.read())
            pacote_size = (len(payload_bin)/sizePayload)
            for i in range(math.ceil(pacote_size)):
                QntPackages.append(payload_bin[:sizePayload])
                del payload_bin[:sizePayload]


        print("Montando o datagrama")

        datagramas = []
        for i in range(len(QntPackages)):
            pacote_size = len(QntPackages).to_bytes(1, byteorder="big")
            pacote_num = (i+1).to_bytes(1, byteorder="big")
            Head = pacote_num + b'/' + pacote_size + b'\x00\x00\x00\x00\x00\x00\x00'
            datagrama_string = Head+QntPackages[i]+EOP
            datagramas.append(datagrama_string)
        
        print("Foram montados {} pacotes".format(len(QntPackages)))

        print(len(datagramas))

        print(datagramas)

        #Enviando o Datagrama

        print("Iniciando o envio dos datagramas")

        i=0

        while i < len(datagramas):
            print(i)
            pacote_atual = (len(datagramas[i])).to_bytes(2, byteorder="big")
            print("Tamanho do pacote ", pacote_atual)
            dg_pacote_atual = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'+pacote_atual+EOP
            print(dg_pacote_atual)

            print("Enviando tamanho pacote {}".format(i+1))
            time.sleep(1)
            com1.sendData(np.asarray(dg_pacote_atual))

            check_tamanho, check_tamanho_size = com1.getData(16)

            if check_tamanho == dg_pacote_atual:
                print("Tamanho recebido corretamente")
                print("Enviando o pacote")
                com1.sendData(np.asarray(datagramas[i]))

            check_pacote, check_pacote_size = com1.getData(17)

            if check_pacote[10:13] == b'sim':
                print("Confirmação recebida")
                i=i+1


        print ("transmissão finalizada!!!")
    
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com1.tx.getStatus()
        #print("txSize:",txSize)

        #Verificação


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
