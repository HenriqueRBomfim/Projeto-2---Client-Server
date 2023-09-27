#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        '''Retorna o comprimento do buffer'''
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """Pausa o thread, ou seja, impede ele de continuar mandando informações para o buffer.
        Depois salva o buffer atual em uma variável b.
        Zera/Limpa o buffer.
        Continua o Thread.
        Retorna o b, que era o buffer até a função ser usada."""
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """Pausa o Thread de mandar informações.
        Tendo em vista que o Buffer é uma lista de bytes:
        Salva o que estiver guardado no buffer do começo até um ponto de parada chamado nData.(Faz um recorte)
        Define o buffer como o que tinha nele a partir do nData até o final
        Libera o Thread para mandar informações novamente
        Retorna o trecho desejado do Buffer"""
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        tempo_inicial = time.time()
        duracao_maxima = 5
        while(self.getBufferLen() < size):
            time.sleep(0.05) 
            #print("Erro no NData")    
            if ((time.time() - tempo_inicial) > duracao_maxima):
                return None, True             
        return(self.getBuffer(size), False)

    def clearBuffer(self):
        self.buffer = b""


