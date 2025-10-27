import pandas as pd
import json
import re
import os
import PyPDF2

from dotenv import load_dotenv

load_dotenv()


def extractContents(reader):
    content_table = reader.pages[2]
    content_text = content_table.extract_text()

    book_and_pages = {}
    start = re.search(r"Genesis\s*\.\.\.", content_text)
    if start:
        q = content_text[start.start():]  
    else:
        q = content_text

    pattern = r"([1-3]?\s?\w+(?: \w+)?)\s*\.\.\.\s*(\d+)"
    matches = re.findall(pattern, q)

    for book, page in matches:
        book_and_pages[book.strip()] = int(page)

    with open(os.getenv("DATA_DUMP_PATH") + "books.json", "w") as f:
        json.dump(book_and_pages, f, indent=4)

def getBookName(text):

    text = text.strip()
    lines = text.splitlines()
    first_line = lines[0].strip()

    # Format 1: Page <num> BookName
    match = re.match(r'^Page\s+\d+\s+((?:\d\s*)?[A-Z][a-z]*(?:\s+[A-Z][a-z]*)*)', first_line)
    if match:
        book_name = match.group(1).strip()
        return book_name

    # Format 2: BookName Page <num>
    match = re.match(r'^((?:\d\s*)?[A-Z][a-z]*(?:\s+[A-Z][a-z]*)*)\s+[Pp]age\s+\d+', first_line)
    if match:
        book_name = match.group(1).strip()
        return book_name
    
    return None


if __name__ == "__main__":
    start_page = 21
    books = {}
    current_book = None
    
    reader = PyPDF2.PdfReader(os.getenv("DATA_SOURCE_PATH"))

    try:
        extractContents(reader)

        for i in range(start_page, len(reader.pages)):
            start_of_chapter = False


    except Exception as e:
       print("Error extracting contents:", e)
       raise e   
    