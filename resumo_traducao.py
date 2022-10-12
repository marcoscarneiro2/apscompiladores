"""
Esse programa ira utilizar o processamento de linguagem natural
para criar um modelo que realiza sumarização automática de textos.

Sumarizar é sinônimo de resumir, sintetizar. Então o modelo em Python
sera capaz de ler um texto de uma fonte qualquer e depois criar um resumo desse texto.7

Iremos usar as bibliotecas NLTK, que significa Natural Language Toolkit, é uma biblioteca
disponível na linguagem Python para realizar tarefas de NLP.
É uma das principais bibliotecas de estudo para quem está ingressando nessa área,
pois nela se encontram datasets e alguns algoritmos essenciais para análise e pré-processamento textual.

A outra biblioteca é BeautifulSoap que utilizaremos para fazer web scraping,
que nada mais é do que garimpar dados na internet.
"""

import urllib.request

import pyperclip as pyperclip
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest
from googletrans import Translator
translator = Translator()

try:
    # Aqui selecionamos o codigo que iremos copiar
    texto = pyperclip.paste()
    print(
        "\n=============================================================================================================\n" +
        "TEXTO BASE COPIADO:\n", texto)

    # Agora vamos dividir o nosso texto em sentenças e depois em palavras:
    sentencas = sent_tokenize(texto)
    palavras = word_tokenize(texto.lower())
    '''
    Agora o mais importante no processamento de linguagens naturais é identificar as chamadas stopwords do idioma. 
    Stopword nada mais é que uma palavra que possui apenas significado sintático dentro da sentença, 
    porém não traz informações relevantes sobre o seu sentido. 
    As stopwords possuem uma frequência muito grande em todos os idiomas e por esse motivo 
    precisamos eliminá-las das palavras que extraímos do texto. 
    Caso contrário, nosso algoritmo poderia dar importância para palavras como: “e”, “ou”, “para”….
    O que atrapalharia nossa análise.

    Explicacao do Codigo:
    
    Utilizamos SET (não permite elementos repetidos) e também compreensão de lista. 
    Temos que configurar o idioma das stopwords que queremos, no caso português. 
    Retiramos também todas as pontuações utilizando ponctuation da biblioteca string.
    Agora temos nossa lista de palavras do texto sem as stopwords, armazenada na variável palavras_sem_stopwords.
    '''
    stopwords = set(stopwords.words('portuguese') + list(punctuation))
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
    '''
    Criamos nossa distribuição de frequência para essa lista de palavras_sem_stopwords e 
    descobrir quais são as mais importantes. 
    Para isso, vamos utilizar a função FreqDist da biblioteca nltk.probability:    
    '''
    frequencia = FreqDist(palavras_sem_stopwords)
    '''
    Vamos agora separar quais são as sentenças mais importantes do nosso texto no sentencas_importantes.
    Criaremos um “score” para cada sentença baseado no número de vezes que uma palavra importante 
    se repete dentro dela. Vamos utilizar um dicionário especial chamado defaultdict da biblioteca collections.
    '''
    sentencas_importantes = defaultdict(int)
    '''
    Criamos um looping para percorrer todas as sentenças e coletar todas as estatísticas.
    O código abaixo popula o dicionário com o índice da sentença (key) e a soma da frequência de cada palavra 
    presente na sentença (value).
    '''
    print(
        "\n=============================================================================================================\n" +
        "TEXTO RESUMIDO PELO NLTK:\n")
    for i, sentenca in enumerate(sentencas):
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in frequencia:
                sentencas_importantes[i] += frequencia[palavra]
    '''
    De posse dessas informações, podemos selecionar no nosso dicionário as “n” 
    sentenças mais importantes para formar o nosso resumo. 
    Utilizando a funcionalidade nlargest da biblioteca heapq, escolhendo as 4 sentenças mais importantes!
    '''
    idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)
    '''
    Agora iremos imprimir nosso resumo
    '''
    for i in sorted(idx_sentencas_importantes):
        print(sentencas[i])
    '''
    E imprimir o texto traduzido pelo GOOGLETRANS
    '''
    print(
        "\n=============================================================================================================\n" +
        "TEXTO TRADUZIDO EM INGLES PELO GOOGLETRANS:\n")
    for i in sorted(idx_sentencas_importantes):
        translated = translator.translate(sentencas[i], src='pt', dest='en')
        print(translated.text)
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except BaseException as err:
    print(f"Unexpected {err=}, {type(err)=}")
