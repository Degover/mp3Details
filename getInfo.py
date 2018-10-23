# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 17:47:48 2018

@author: Eneias
"""

#Importa os módulos necessários
import requests
import bs4

#Funções para gerar os links
def getGoogle(name):
    newName = name.replace(' ', '+')
    link = r'https://www.google.com.br/search?q=' + newName
    return link
    
#Funções para pesquisar nos links
def searchGoogle(name):
    #Faz o download da pagina
    res = requests.get(getGoogle(name))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    
    #Acha os elementos da pagina e os coloca no dicionario
    elems = soup.select(u'div div div div div div span')
    detailsDic = {'Artista': None, 'Álbum': None,
           'Data de lançamento': None, 'Gênero': None, 
           'Imagem': None, 'Letra': None, 'Titulo':None}
    #Testa se o elemento esta no dicionario
    for elemNum in range(len(elems)):
        elem1 = elems[elemNum].getText()[:-2]
        elem2 = elems[elemNum].getText()[:-3]
        if elem1 in detailsDic.keys():
            detailsDic[elem1] = elems[(elemNum + 1)].getText()
        elif elem2 in detailsDic.keys():
            detailsDic[elem2] = elems[(elemNum + 1)].getText()
            
    #Retira o titulo da musica
    title = name.replace(detailsDic['Artista'].lower(), '').replace('-', '')
    #Formata o titulo
    newTitle = ''
    for word in title.split():
        if len(word) > 2:
            newTitle += word.title() + ' '
        else:
            newTitle += word  + ' '
    newTitle = newTitle[:-1]
    detailsDic['Titulo'] = newTitle       
    #Acha os sites das letras
    elems = soup.select(u'.r a')
    for elem in elems:
        site = elem['href'][7:].rsplit(r'&sa=')[0]
        if r'www.letras.mus.br' in site:
            detailsDic['Letra'] = searchLetras(site)

    
    #Acha a imagem
    #Faz o download da pagina de imagens
    album = detailsDic['Artista'] + ' ' + detailsDic['Álbum'] + r'&tbm=isch'
    res = requests.get(getGoogle(album))
    res.raise_for_status()
    #Procura as imagens
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    elems = soup.select(u'div a img')
    imgUrl = elems[0].get('src')
    #Salva a imagem no dicionario
    res = requests.get(imgUrl)
    res.raise_for_status()
    detailsDic['Imagem'] = res.iter_content()
        
    #Retorna o dicionario com os detalhes achados
    return(detailsDic)

def searchLetras(site):
    #Faz com que a HTML seja sem tradução
    if r'traducao.html' in site:
        site = site[:-14]
        
    #Faz o download da pagina
    res = requests.get(site)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    #Acha a letra da musica
    elems = soup.select('div div div div div div article p')
    
    #Formata a letra em uma string
    letra = ''
    for parag in elems:
        #Troca as marcações do HTML por espaços e linhas
        paragStr = str(parag)[3:].replace(r'</p>', '\n\n').replace(r'<p>', '\n')
        paragStr = paragStr.replace(r'<br/>', '\n').replace(r'</br>', 
                                   '').replace(r'<br>', '\n')
        #Adiciona na string
        letra += paragStr
    
    #Retorna a letra
    return letra
        
searchGoogle('Jim Croce Time in a bottle')