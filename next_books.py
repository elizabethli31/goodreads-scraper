import sys
import requests
import json
from bs4 import BeautifulSoup


def get_similar_books(soup):

    link = soup.find('a', text='See similar books…')

    if (link):

        similar_books_list = []
        similar_books_list.append("Similar Books")

        similar_url = link['href']
        page = requests.get(similar_url)
        soup = BeautifulSoup(page.content, "html.parser")

        similar_books_mult = soup.find_all(
            'div', {'data-react-class': 'ReactComponents.SimilarBooksList'})
        similar_books_mult.pop(0)

        for similar_books in similar_books_mult:
            dat = similar_books['data-react-props']
            dat_json = json.loads(dat)
            books = dat_json.get('similarBooks')
            for book in books:
                this = book.get('book')
                similar_books_list.append(
                    this.get('title') + " by " + this.get('author').get('name'))

    return similar_books_list


def main():
    book_id = sys.argv[1]
    file = sys.argv[2]

    if(book_id): 
        url = "https://goodreads.com/book/show/" + book_id
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")

        books_all = []

        sim_books = get_similar_books(soup)
        books_all.extend(sim_books)

        with open(file, 'w') as f:
            for line in books_all:
                f.write(f"{line}\n")


if __name__=="__main__":
    main()
