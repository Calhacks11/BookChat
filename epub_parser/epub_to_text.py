import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os


def get_chapter(bookname: str, ch_no: int):
    chapter_file = f'data/{bookname}/ch-{ch_no}.txt'
    with open(chapter_file, 'r') as file:
        content = file.read()

    return content


def epub_to_chapters(epub_file_name):
    # Read the EPUB file
    epub_file = f'data/{epub_file_name}'
    book = epub.read_epub(epub_file)
    book_dir = epub_file.removesuffix(".epub")
    os.makedirs(book_dir, exist_ok=True)


    # Initialize an empty list to store the text
    chapters = []

    # Loop through the items in the book
    count = 0
    for i, item in enumerate(book.get_items()):
        # print('-----type-------------', item.get_type())
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # count += 1
            # Parse the document content with BeautifulSoup
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            # Append the text to the list, stripped of HTML tags
            chapter = soup.get_text()
            # print('-------text length--------', len(text))
            chapters.append(chapter)
            # print(chapter)
            with open(f'{book_dir}/ch-{i + 1}.txt', 'w', encoding='utf-8') as output_file:
                output_file.write(chapter)

    # Join all the text content into a single string
    # return '\n'.join(chapters)
    return chapters

