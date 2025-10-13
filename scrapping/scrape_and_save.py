from extract_data import scrape_all_books
from load_data import save_books_csv

def main():
    """
    Função principal que orquestra o processo:
    1. Coleta os dados dos livros via web scraping.
    2. Salva os dados em um arquivo CSV.
    """
    books = scrape_all_books()    # Extrai todos os livros do site
    save_books_csv(books)         # Salva os livros extraídos em um arquivo CSV

# Este bloco garante que a função main() será executada somente
# se o script for executado diretamente (e não importado como módulo).
if __name__ == "__main__":
    main()
