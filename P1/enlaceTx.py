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
class TX(object):
 
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False


    def thread(self):
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen    = self.fisica.write(self.buffer)
                self.threadMutex = False

    def threadStart(self):
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def sendBuffer(self, data):
        """ O transLen diz o tamanho do que está no transmissor será 0, ou seja, zera a informação que se sabe sobre o tamanho dele
        Depois define o buffer como a informação que a função recebe
        Aí define o threadMutex como True
        """
        self.transLen = 0
        self.buffer = data
        self.threadMutex = True

    def getBufferLen(self):
        return(len(self.buffer))

    def getStatus(self):
        # Quem controla é a Thread, tem um programa rodando tudo linha a linha, e tem outro 
        # É como quando vamos atravessar a rua, olhamos rápido e não vemos nada, mas alguma hora pode passar um carro à milhão
        # Mudar o self.threadMutex para true
        return(self.transLen)

    def getIsBussy(self):
        return(self.threadMutex)

