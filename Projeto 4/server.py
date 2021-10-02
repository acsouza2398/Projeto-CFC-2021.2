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
        h8=b'CRC'
        h9=b'CRC'


        head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9
        EOP = b'0xFF 0xAA 0xFF 0xAA'

        

        rxmensagem = b""

        print("-------------------------")
        print("Iniciando o handshake")
        print("-------------------------")

        h0=b'2'
        h5=b'C'

        head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9

        
        while rxmensagem == b"":
            rxmensagem, nRxmensagem = com2.getData(33)
            print(rxmensagem)
            
            print("Handshake recebido!")

            if rxmensagem != b'' :
                answer = head+EOP
                com2.sendData(answer)

                print("Handshake enviado")
            else:
                pass

        pacote_recebido = 1
        pacote_ultimo = 0
        terminou = False
        rxBuffer = b""

        print("-------------------------")
        print("Iniciando o recebimento do datagrama")
        print("-------------------------")

        while not terminou:
            h7 = pacote_ultimo.to_bytes(2, "big")
            head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9

            rxTamPacoteAt,rxTamPacoteAtSize = com2.getData(33)
            
            pacote_size = rxTamPacoteAt[5:7]
            pacote_size = int.from_bytes(pacote_size, "big")

            print("Tamanho do payload ", pacote_size)

            print("Recebendo o pacote")

            rxPacote, rxPacotesize = com2.getData(35+pacote_size)

            pacote = int.from_bytes(rxPacote[5:6], "big")
            pacote_final = int.from_bytes(rxPacote[4:5], "big")
            print("Serao recebidos {} pacotes".format(pacote_final))
            rxPacote_str = rxPacote.decode("utf-8")

            print("Recebi pacote {}".format(pacote))

            rxBuffer = rxBuffer + rxPacote[16:-19]   


            if pacote == pacote_recebido:
                print("Pacote {} recebido".format(pacote))
            else:
                print("Erro, pacote recebido diferente do esperado. Aguardando novo envio")
                redlight = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'+b'nao'+EOP
                com2.sendData(redlight)
                continue

            print("Enviando confirmação")

            if rxPacote[-19:] == EOP:
                h0 = b'4'
                h7 = b'1'
                head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9
                greenlight = head+EOP
                com2.sendData(greenlight)
                print("Tudo certo, pacote enviado completo")
                print("-------------------------")
                pacote_ultimo+=1
            else:
                h0 = b'6'
                h6 = pacote_recebido.to_bytes(2, "big")
                head = h0+h1+h2+h3+h4+h5+h6+h7+h8+h9
                redlight = head+EOP
                com2.sendData(redlight)
                print("Deu erro, pacote enviado incompleto. Aguardando novo envio")
                continue

            if pacote_recebido == pacote_final:
                terminou = True
            else:
                pacote_recebido+=1


        print("-------------------------")
        print("Transmissão encerrada")
        print("-------------------------")


        print("-------------------------")
        print("Reagrupando o arquivo enviado")
        print("-------------------------")

        imgWrite = "Payload_Novo.txt"

        with open(imgWrite, "wb") as imagem:
            imagem.write(rxBuffer)
            imagem.close()
            
            
    
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
