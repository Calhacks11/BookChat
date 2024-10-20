import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


# Function to extract text from EPUB
def epub_to_text(epub_file):
    # Read the EPUB file
    book = epub.read_epub(epub_file)

    # Initialize an empty list to store the text
    text_content = []

    # Loop through the items in the book
    count = 0
    for item in book.get_items():
        # print('-----type-------------', item.get_type())
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # count += 1
            # Parse the document content with BeautifulSoup
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            # Append the text to the list, stripped of HTML tags
            text = soup.get_text()
            # print('-------text length--------', len(text))
            text_content.append(text)
            print(text)

    # Join all the text content into a single string
    return '\n'.join(text_content)



def main():
    # Usage example
    # epub_file_path = 'shaw-caesar-and-cleopatra.epub'
    epub_file_path = 'conversation.epub'
    text = epub_to_text(epub_file_path)

    # Print or save the extracted text
    # print(text)

    # Optionally, save the text to a file
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(text)

if __name__ == '__main__':
    main()
