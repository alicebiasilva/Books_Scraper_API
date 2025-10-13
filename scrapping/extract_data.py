import requests
from bs4 import BeautifulSoup
import os
import re

# URL base do site de onde os livros serão coletados
BASE_URL = "https://books.toscrape.com/"

# URL base onde as imagens estarão hospedadas publicamente (ex: GitHub Pages)
IMAGE_BASE_URL = "https://github.com/alicebiasilva/Pos_Tech_Machine_Learning_Engineer/blob/main/public/images/"

def fetch_page(url: str) -> str:
    """
    Realiza uma requisição HTTP para o URL fornecido e retorna o conteúdo HTML da página.

    Args:
        url (str): URL da página a ser requisitada.

    Returns:
        str: Conteúdo HTML da página com codificação apropriada.
    """
    response = requests.get(url)
    response.raise_for_status()  # Lança erro se a resposta for inválida (status 4xx ou 5xx)
    response.encoding = 'ISO-8859-1'  # Corrige possíveis problemas de codificação de caracteres

    return response.text

def download_image(img_url: str, save_folder: str = "public/images") -> str:
    """
    Faz o download de uma imagem a partir de uma URL e salva localmente no diretório especificado.

    Args:
        img_url (str): URL completa da imagem a ser baixada.
        save_folder (str): Caminho da pasta local onde a imagem será salva.

    Returns:
        str: Caminho local do arquivo de imagem salvo.
    """
    os.makedirs(save_folder, exist_ok=True)  # Garante que a pasta exista
    filename = os.path.join(save_folder, img_url.split("/")[-1])  # Extrai o nome do arquivo da URL

    response = requests.get(img_url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Erro ao baixar imagem: {img_url}")

    return filename

def parse_books_from_page(html: str, category_name: str) -> list[dict]:
    """
    Faz o parsing do HTML da página e extrai informações de todos os livros exibidos nela.

    Args:
        html (str): HTML da página.
        category_name (str): Nome da categoria associada à página.

    Returns:
        list[dict]: Lista de dicionários, cada um representando um livro.
    """
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for book in soup.select("article.product_pod"):
        # Extrai informações principais do livro
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        price = float(re.sub(r"[^\d.]", "", price))  # Remove símbolos e converte para float
        availability = book.select_one(".availability").text.strip()
        rating_class = book.p["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "None"  # Ex: 'One', 'Two', etc.

        # Monta o caminho completo da imagem
        img_relative = book.select_one("div.image_container img")["src"]
        img_url = BASE_URL + img_relative.replace("../", "")  # Corrige o caminho relativo
        img_path = download_image(img_url)  # Baixa e salva a imagem localmente

        img_filename = os.path.basename(img_path)  # Pega apenas o nome do arquivo
        public_img_url = IMAGE_BASE_URL + img_filename  # Constrói URL pública para uso na API

        # Cria o dicionário representando um livro
        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating,
            "category": category_name,
            "image_path": public_img_url  # URL acessível da imagem
        })

    return books

def scrape_all_books() -> list[dict]:
    """
    Percorre todas as categorias e páginas do site e extrai informações de todos os livros.

    Retorna uma lista de livros com todas as informações, incluindo ID único para cada livro.

    Returns:
        list[dict]: Lista completa de livros extraídos com IDs.
    """
    # Coleta HTML da página inicial para extrair as categorias
    categories_html = fetch_page(BASE_URL)
    soup = BeautifulSoup(categories_html, "html.parser")

    # Mapeia nome da categoria para sua URL
    categories = {
        cat.text.strip(): BASE_URL + cat["href"]
        for cat in soup.select(".side_categories ul li ul li a")
    }

    all_books = []
    current_id = 1  # Inicializa contador de IDs únicos

    # Itera por todas as categorias
    for name, url in categories.items():
        print(f"Coletando livros da categoria: {name}")
        page_url = url

        # Percorre todas as páginas da categoria (caso haja paginação)
        while True:
            html = fetch_page(page_url)
            books = parse_books_from_page(html, name)

            # Atribui ID sequencial a cada livro encontrado
            for book in books:
                book['id'] = current_id
                current_id += 1

            # Adiciona livros da página atual à lista geral
            all_books.extend(books)

            # Verifica se há uma próxima página
            next_page = BeautifulSoup(html, "html.parser").select_one("li.next a")
            if next_page:
                # Constrói a URL da próxima página
                page_url = url.rsplit("/", 1)[0] + "/" + next_page["href"]
            else:
                break  # Sai do loop se não houver próxima página

    return all_books
