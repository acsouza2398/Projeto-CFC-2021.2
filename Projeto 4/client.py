#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from sys import byteorder
from enlace import *
import time
from random import randint
import numpy as np
import datetime
import math

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)
#Ana - COM3
#Tiago - COM5


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        inicia = False

        '''
            h0 – tipo de mensagem
            h1 – id do sensor
            h2 – id do servidor
            h3 – número total de pacotes do arquivo
            h4 – número do pacote sendo enviado
            h5 – se tipo for handshake:id do arquivo
            h5 – se tipo for dados: tamanho do payload
            h6 – pacote solicitado para recomeço quando a erro no envio.
            h7 – último pacote recebido com sucesso.
            h8 – h9 – CRC
        '''

        h0=b'0'
        h1=b'A'
        h2=b'B'
        h3=b'0'
        h4=b'0'
        h5=b'0'
        h6=b'0'
        h7=b'0'
        h8=b'0'
        h9=b'0'


        head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9
        EOP = b'0xFF0xAA0xFF0xAA'


        log = []

        while not inicia:

            print("Quero Falar com você")
            timeinicial = time.time()

            answer = b""
            i=0

            #Handshake

            print("-------------------------")
            print("Handshake")
            print("-------------------------")

            while answer == b"":
                h0=b'1'
                h5=b'C'

                head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9

                mensagem = head+EOP

                tempo = datetime.datetime.now()
                log_str = str(tempo) + " /envio /" + h0.decode("utf-8") + " /14"
                log.append(log_str)

                print("Enviando o handshake")
                com1.sendData(mensagem)

                print("Na escuta")

                answer, answerlen = com1.getData(26)

                answer_d = answer.decode("utf-8")

                tempo = datetime.datetime.now()
                log_str = str(tempo) + " /recebe /" + answer_d[0] + " /14"
                log.append(log_str)

                if answer_d[2] == h2.decode("utf-8"):
                    print("Resposta recebida")
                    inicia = True

        #Montando o Datagrama

        filepath = "./payload.txt"
        sizePayload = 114 
        
        print("-------------------------")
        print("Montando o Datagrama")
        print("-------------------------")

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
            datagrama_string = QntPackages[i]+EOP
            datagramas.append(datagrama_string)
        
        print("Foram montados {} pacotes".format(len(QntPackages)))

        numPck = len(QntPackages)

        time.sleep(1)

        #Enviando o Datagrama
        print("-------------------------")
        print("Iniciando o envio do datagrama")
        print("-------------------------")

        cont=1

        while cont <= numPck:
            h0=b'3'
            h3=numPck.to_bytes(1, byteorder='big')
            h4=cont.to_bytes(1, byteorder='big')
            h5=(len(datagramas[cont-1])-16).to_bytes(2, byteorder="big")
            
            head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9

            print("Começando o processo de envio do pacote {}".format(cont))
            pacote_atual = (len(datagramas[cont-1])).to_bytes(2, byteorder="big")

            tempo = datetime.datetime.now()
            size_tot = 14 + int.from_bytes(h5, "big")
            log_str = str(tempo) + " /envio /" + h0.decode("utf-8") + " / " + str(size_tot) + " / " + str(cont) + " / " + str(numPck)
            log.append(log_str)

            print("Enviando o tamanho do pacote")
            com1.sendData(np.asarray(head+EOP))

            time.sleep(2)

            print("Enviando o pacote {}".format(cont))
            com1.sendData(np.asarray(head+datagramas[cont-1]))

            t_inicial1 = time.time()
            t_inicial2 = time.time()

            print("Aguardando confirmação")
            check_pacote, check_pacote_size = com1.getData(26)

            check_pacote_str = check_pacote.decode("utf-8")

            tempo = datetime.datetime.now()
            log_str = str(tempo) + " /recebe /" + check_pacote_str[0] + " /14"
            log.append(log_str)

            if check_pacote_str[0] == '4':
                print("Confirmação recebida")
                print("-------------------------")
                cont+=1
            else:
                if time.time() - t_inicial1 > 5:
                    print("Erro. Reinviando o pacote {}".format(cont))
                    tempo = datetime.datetime.now()
                    size_tot = 14 + int.from_bytes(h5, "big")
                    log_str = str(tempo) + " /envio /" + h0.decode("utf-8") + " / " + str(size_tot) + " / " + str(cont) + " / " + str(numPck)
                    log.append(log_str)
                    com1.sendData(np.asarray(head+datagramas[cont-1]))
                    t_inicial1 = 0
                if time.time() - t_inicial2 > 20:
                    print("Timeout")
                    h0 = b'5'
                    head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9
                    tempo = datetime.datetime.now()
                    log_str = str(tempo) + " /envio /" + h0.decode("utf-8") + " /14"
                    log.append(log_str)
                    com1.sendData(np.asarray(head+EOP))
                    print("ops! :-\\")
                    com1.disable()
                    exit()
                elif check_pacote_str[0] == '6':
                    cont = check_pacote[6]

        print ("Transmissão finalizada")
    
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com1.tx.getStatus()
        #print("txSize:",txSize)

        #Verificação

        imgWrite = "Client.txt"

        with open(imgWrite, "w") as imagem:
            for i in log:
                imagem.writelines(i + "\n")
            imagem.close()


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
