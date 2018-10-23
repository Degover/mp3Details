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
           'Data de lançamento': None, 'Gêneros': None}
    for elemNum in range(len(elems)):
        elem = elems[elemNum].getText()[:-2]
        if elem in detailsDic.keys():
            detailsDic[elem] = elems[(elemNum + 1)].getText()
    
    #Retorna o dicionario com os detalhes achados
    return(detailsDic)
        
searchGoogle('Jim Croce Time in a bottle')