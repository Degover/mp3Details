# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 17:50:33 2018

@author: Eneias
"""

""" mp3Details.py - Programa python feito para pegar as informações da musica
    em MP3 e salva-las no arquivo. """

#Importa os módulos necessários
from mutagen.easyid3    import EasyID3      as mp3
from mutagen.mp3        import MP3
from mutagen.id3        import ID3, APIC, TT2, TPE1, TRCK, TALB, USLT, error
from getInfo            import searchGoogle as search
from urllib.request     import urlopen
import requests as req
import os

# ID3 info:
# APIC: picture
# TIT2: title
# TPE1: artist
# TRCK: track number
# TALB: album
# USLT: lyric

#Funções usadas
def imgSave(audioPath, imgUrl, letra):
    #Abre o audio
    audio = ID3(audioPath)
    
    #Abre a imagem
    res = req.get(imgUrl)
    res.raise_for_status()
    #Faz o download da imagem
    imgPath = 'image.' + imgUrl[-3:]
    imageFile = open(imgPath, 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    #Abre a imagem baixada
    imageData = open(imgPath, 'rb').read()
    #Salva a imagem no arquivo de audio
    audio.add(APIC(3, 'image/jpeg', 3, 'Front cover', imageData))

    #Salva a letra
    if letra != None:
        audio.add(USLT(encoding=3, lang=u'eng', desc=u'desc', text=letra))
        
    #Salva e fecha o arquivo de audio
    audio.save(v2_version=3)

    #Deleta a imagem baixada
    os.remove(imgPath)

#Percorre todos os arquivos dentro de IN
for fName, subFs, fileNames in os.walk(r'.\IN'):
    #Variaveis para mostrar quanto foi feito
    numeroDeFiles = len(fileNames)
    fileAtual = 0

    #Pesquisa e altera cada arquivo dentro da pasta IN
    for fileName in fileNames:
        #Pula o arquivo gerado pelo Python
        if fileName == 'Thumbs.db':
            continue
        
        #Faz a pesquisa
        details = search(fileName[:-4])
        '''Keys = 'Titulo', 'Artista', 'Álbum', 'Data de lançamento',
            'Gênero', 'Imagem', 'Letra'''

        #Abre o arquivo de audio
        path = '.\\IN\\' + fileName
        audio = mp3(path)

        #Coloca os detalhes no arquivo
        #Titulo
        if details['Titulo'] != None:
            audio['title'] = details['Titulo']

        #Artista
        if details['Artista'] != None:
            audio['artist'] = details['Artista']
            audio['albumartist'] = details['Artista']

        #Album
        if details['Álbum'] != None:
            audio['album'] = details['Álbum']

        #Data de lançamento
        if details['Data de lançamento'] != None:
            audio['date'] = details['Data de lançamento']

        #Gênero
        if details['Gênero'] != None:
            audio['genre'] = details['Gênero']

        #Salva e fecha o arquivo
        set(audio)
        audio.save()

        #Salva a imagem e letra
        imgSave(path, details['Imagem'], details['Letra'])

        #Move e renomeia o arquivo
        #Fornece o novo caminho do arquivo
        newPath = ''
        if details['Titulo'] != None or details['Artista'] != None:
            newFileName = details['Titulo'] + ' - ' + details['Artista']
            newPath = '.\\OUT\\' + newFileName + '.mp3'
        else:
            newPath = '.\\OUT\\' + fileName
        #Move e renomeia
        os.rename(path, newPath)

        #Incrementa a variavel de contagem
        fileAtual += 1

        #Mostra o estado atual
        completed = 'Completado: ' + str(fileAtual) + r'/' + str(numeroDeFiles)
        prcnt = round(((fileAtual/numeroDeFiles) * 100), 2)
        print(completed + ' - ' + str(prcnt) + r'%')
        print('[' + ('|' * round(prcnt/2)).ljust(50) + ']')

        # TODO: Melhorar a imagem no getInfo.py

#Mostra ao usuario que completou o ciclo
fileAtual += 1
completed = 'Completado: ' + str(fileAtual) + r'/' + str(numeroDeFiles)
prcnt = round(((fileAtual/numeroDeFiles) * 100) - 1, 2)
print(completed + ' - ' + str(prcnt) + r'%')
print('[' + ('|' * round(prcnt/2)).ljust(50) + ']')
print('Done!')
