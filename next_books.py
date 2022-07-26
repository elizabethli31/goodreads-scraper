import sys
import requests
import json
from bs4 import BeautifulSoup


def get_similar_books(soup):

    link = soup.find('a', text='See similar books…')

    similar_books_list = []

    if (link):

        similar_books_list.append('Similar Books:')

        similar_url = link['href']
        page = requests.get(similar_url)
        soup = BeautifulSoup(page.content, 'html.parser')

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


def get_lists_books(soup):

    link = soup.find('a', text='More lists with this book...')

    lists_books = []   

    if (link):

        lists_books.append('\nRecommendations from top 5 lists with your book:')

        lists_url = 'https://goodreads.com' + link['href']
        page = requests.get(lists_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        i = 0
        lists = soup.find_all('a', class_='listTitle')    
        while (i < 5 and lists[i]):
            one_list_url = 'https://goodreads.com' + lists[i]['href']
            one_page = requests.get(one_list_url)
            page_soup = BeautifulSoup(one_page.content, 'html.parser')

            j = 0
            books = page_soup.find_all('a', class_='bookTitle')
            authors = page_soup.find_all('a', class_='authorName')
            while (j < 5 and books[j] and authors[j]):

                lists_books.append(books[j].text + 'by ' + authors[j].text)
                j += 1

            i += 1

    return lists_books


def main():

    book_id = sys.argv[1]
    file = sys.argv[2]

    if(book_id): 
        url = 'https://goodreads.com/book/show/' + book_id
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        books_all = []
        this_book = soup.find('title')
        books_all.append('Recommendations for ' + this_book.text + '\n')
        
        sim_books = get_similar_books(soup)
        books_all.extend(sim_books)

        lists_books = get_lists_books(soup)
        books_all.extend(lists_books)

        with open(file, 'w') as f:
            for line in books_all:
                f.write(f"{line}\n")


if __name__=='__main__':
    main()
