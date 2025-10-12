from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from pathlib import Path

router = APIRouter()

csv_path = Path(__file__).resolve().parent.parent / "api" / "data" / "books.csv"
df_books = pd.read_csv(csv_path, encoding="utf-8")

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
