# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 17:50:33 2018

@author: Eneias
"""

""" mp3Details.py - Programa python feito para pegar as informações da musica
    em MP3 e salva-las no arquivo. """

#Importa os módulos necessários
import eyed3 as eye
import os

for fName, subFs, fileNames in os.walk(r'.\IN'):
    print('The current folder is ' + fName)
    
    for subF in subFs:
        print('Subfolder: ' + subF)

    for fileName in fileNames:
        print('Arquive: ' + fileName)
    print(' ')
