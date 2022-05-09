from collections import defaultdict
import pandas as pd
from bs4 import BeautifulSoup
import os

"""
A Estratégia usada para criar o script foi usar a biblioteca  BeautifulSoup,
ferramenta bastante utilizada para realização da técnica de 'scrapping' e Pandas,
outra biblioteca python, muito utilizada para analise e manipulação de dados.

Primeiro tive que estudar os arquivos html enviados,
verificar a estrutura para entender quando deveria seguir para 
alternativa de captura, limpeza dos dados e como escrever o html de saída.


Links usados para realização a tarefas:
 - https://beautiful-soup-4.readthedocs.io/en/latest/
 - https://pandas.pydata.org/docs/
 - https://medium.com/geekculture/web-scraping-tables-in-python-using-beautiful-soup-8bbc31c5803e
 - https://www.youtube.com/watch?v=kqvWOcPog4s
 - https://www.youtube.com/watch?v=Yi0XgxPK14I
 - https://www.youtube.com/watch?v=kqvWOcPog4s
"""

def scraper_using_beautifulsoup(file):
    """
    Este método abre o arquivo em html e lê as tags do html e busca as informações
    de cnpj, resultado, número do pedido, data do deposito, 'título, ipc.
        Parameters:
            file (str): nome do arquivo

        Returns:
            data (list): resultado, cnpj, número do pedido, data do deposito, título, ipc agrupados.
    """
    data = []
    message = """Nenhum resultado foi encontrado para a sua pesquisa. Para efetuar outra pesquisa, pressione o botão de VOLTAR."""
    with open(file, 'rb') as text:
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table')
        tables = soup.find_all('table')

        if len(tables) > 1:
            try:
                columns3 = tables[1].find('tbody').text
                lista = columns3.strip().split('\r')[-1]
                if 'CNPJ' in lista:
                    elemento = lista.split(':')[-1].strip(' \\')
                    data.append(elemento)
            except (AttributeError, TypeError):
                pass
            
            if message in tables[2].find('tbody').text:
                data.append(0)

        for row in table.tbody.find_all('tr'):
            columns = row.find('td')
            try:
                if columns.font['class'] == ["normal"]:
                    elemento = columns.font.text.strip()
                    if 'CNPJ' in elemento:
                        data.append(elemento.split(':')[1].replace('\\','').replace(" ",''))
            except (AttributeError, TypeError):
                continue
        

        try:
            for row2 in table.find('tbody', class_="Context"):
                elementos2 = row2.text.replace('\n\n\n\r\n\t','').replace('\r\n\t', '').replace('\n\n','').split('\n')
                if len(elementos2) != 2:
                    data.append(elementos2)
        except TypeError:
            pass
        text.close()

    return data 


def generate_html():
    """
    Este método gera o arquivo PATENTES.html após finalizar a extração de todos os dados.

    """
    os.chdir('PATENTES/')
    data = defaultdict(dict)
    cnpj= []
    resultado = []
    pedido = []
    deposito = []
    titulo = []
    ipc = []
    nome = []

    for file in os.listdir():
        file_name = file.split('.')[0]
        data[file_name] = scraper_using_beautifulsoup(file)

    for key in data.keys():
        if len(data[key]) > 2:
            for value in data[key]:                
                if type(value) is list:
                    pedido.append(value[0].strip())
                    deposito.append(value[1].strip())
                    titulo.append(value[2].strip())
                    ipc.append(value[3].strip())
                    resultado.append(len(data[key])-1)
                    cnpj.append(value)
                    nome.append(key)
                
        elif len(data[key]) <=2:
            cnpj.append(data[key][0])
            resultado.append(data[key][1])
            pedido.append('----')
            deposito.append('----')
            titulo.append('----')
            ipc.append('----')
            nome.append(key)
    
    df = pd.DataFrame({'Nome do Arquivo':nome, 'CNPJ':cnpj,
    'RESULTADO':resultado,'NÚMERO DO PEDIDO':pedido, 'DATA DEPOSITO':deposito, 'TÍTULO':titulo, 'IPC':ipc})

    df.to_html("PATENTES.html")

if __name__ == "__main__":
    generate_html()


    