import csv  # Módulo para manipulação de arquivos CSV
import os   # Módulo para interações com o sistema de arquivos

def save_books_csv(books: list[dict], filename: str = "api/data/books.csv"):
    """
    Salva uma lista de dicionários representando livros em um arquivo CSV.

    Parâmetros:
        books (list[dict]): Lista de livros, onde cada livro é representado como um dicionário.
        filename (str): Caminho onde o arquivo CSV será salvo. Padrão: 'api/data/books.csv'.
    """

    # Garante que o diretório onde o arquivo será salvo exista. Se não existir, ele será criado.
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Abre o arquivo no modo escrita ('w'), com codificação UTF-8 e sem quebra de linha adicional.
    with open(filename, "w", newline="", encoding="utf-8") as f:
        # Cria um escritor que usará as chaves do primeiro dicionário como cabeçalhos do CSV
        writer = csv.DictWriter(f, fieldnames=books[0].keys())

        # Escreve a linha de cabeçalho no CSV (nomes das colunas)
        writer.writeheader()

        # Escreve todas as linhas (livros) no CSV
        writer.writerows(books)
    
    # Imprime no terminal a quantidade de livros salvos e o caminho do arquivo
    print(f"{len(books)} livros salvos em {filename}")
