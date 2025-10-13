# Importa funcionalidades do FastAPI:
# - APIRouter: para organizar rotas da API em "módulos" ou "grupos"
# - HTTPException: para lançar exceções com código HTTP customizado
# - Query: para definir e validar parâmetros de consulta (query params)
# Importa o pandas para manipulação e leitura de dados tabulares (como arquivos CSV)
# Importa Path da biblioteca pathlib para trabalhar com caminhos de arquivos de forma segura e multiplataforma
# Cria um roteador (APIRouter) para registrar rotas relacionadas a livros ou categorias

from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from pathlib import Path

router = APIRouter()

# Define o caminho absoluto até o arquivo books.csv
csv_path = Path(__file__).resolve().parent.parent / "api" / "data" / "books.csv"

# Lê o arquivo CSV com pandas e armazena o conteúdo no DataFrame `df_books`
df_books = pd.read_csv(csv_path, encoding="utf-8")

#Criação das rotas GET
# Lista titulo de todos os livros
@router.get("/books", tags=["Livros"])
def get_books():
    """
    Retorna uma lista com os títulos de todos os livros disponíveis.

    Retorno:
        list[str]: Lista contendo os títulos dos livros.
    """
    return df_books["title"].tolist()


# Detalhes de um livro pelo ID
@router.get("/books/{book_id}", tags=["Livros"])
def get_book(book_id: int):
    """
    Retorna os detalhes completos de um livro pelo seu ID.

    Parâmetros:
        book_id (int): ID único do livro a ser buscado.

    Retorna:
        dict: Dicionário com as informações do livro correspondente.

    Erros:
        HTTP 404: Se nenhum livro com o ID fornecido for encontrado.
    """
    book = df_books[df_books["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book.to_dict(orient="records")[0]

#Lista detalhes dos livros por titulo e/ou categoria
@router.get("/books/search", tags=["Categorias"])
def search_books(title: str | None = Query(None), category: str | None = Query(None)):
    """
    Busca livros filtrando por título e/ou categoria.

    Parâmetros de consulta:
        - title (str, opcional): Parte do título do livro (case-insensitive).
        - category (str, opcional): Parte do nome da categoria (case-insensitive).

    Retorna:
        Lista de dicionários com os livros encontrados. Se nenhum livro for encontrado,
        retorna HTTP 404.
    """
    result = df_books

    if title:
        result = result[result["title"].str.contains(title, case=False, na=False)]

    if category:
        result = result[result["category"].str.contains(category, case=False, na=False)]

    if result.empty:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado com os critérios fornecidos.")

    return result.to_dict(orient="records")

# Lista todas as categorias
@router.get("/categories", tags=["Categorias"])
def get_categories():
    """
    Retorna uma lista com todas as categorias únicas disponíveis nos livros.

    Retorno:
        dict: Um dicionário contendo a chave "categories" com uma lista de strings,
              onde cada string representa uma categoria distinta.
    """
    categories = df_books["category"].unique().tolist()
    return {"categories": categories}

#Verifica saúde da API, analisando se há dados da fonte csv
@router.get("/health", tags=["Saúde"])
def health():
    """
    Verifica o status da API e a disponibilidade da base de dados (CSV).

    Retorna:
        dict: {"status": "ok"} se tudo estiver funcionando corretamente.
    
    Levanta HTTPException 503 se o arquivo CSV não estiver acessível ou inválido.
    """
    if not csv_path.is_file():
        raise HTTPException(status_code=503, detail="Base de dados não encontrada")

    try:
        pd.read_csv(csv_path)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao ler base de dados: {str(e)}")

    return {"status": "ok"}
