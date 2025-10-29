import pandas as pd
import re
import PyPDF2
from .utils import BibleUtilities

class BibleExtractor:
    def __init__(self, source_path, dump_path, start_page=21):
        self.source_path = source_path
        self.dump_path = dump_path
        self.start_page = start_page
        self.testament = "Old Testament"
        self.reader = PyPDF2.PdfReader(self.source_path)    


    def extractTableOFContents(self):

        content_table = self.reader.pages[2]
        content_text = content_table.extract_text()

        book_and_pages = {}
        start = re.search(r"Genesis*\.\.\.", content_text)
        if start:
            starting_point = content_text(start.start())
        else:
            starting_point = content_text

        pattern = r"([1-3]?\s?\w+(?: \w+)?)\s*\.\.\.\s*(\d+)"
        matches = re.findall(pattern, starting_point)

        for book, page in matches:
            book_and_pages[book.strip()] = int(page)   

        utils = BibleUtilities()
        utils.saveFile(book_and_pages,"books.json")

    @staticmethod
    def getBookNameFromHeader(text) -> str: 
        
        lines = text.splitlines()
        first_line = lines[0].strip()

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

    @staticmethod
    def cleanBookText(text):        
        match = re.search(r'\{1:1\}', text)
        if match:
            text = text[match.start():]
        else:
            match = re.search(r'Page\s+\d{1,3}', text, re.IGNORECASE)
            if match:
                text = text[match.end():]
            else:
                return None  

        text = re.sub(r'Downloaded from .*', '', text)
        text = text.replace('\n', ' ')
        
        return text
    
    @staticmethod
    def getVerses(text):    
        append_text = None

        if '{' not in text: 
            return text, None

        if not text.startswith('{'):
            append_text = text.split('{',1)[0].strip()
        
        verses = text.split('{',1)[1].strip()
        verses = '{' + verses

        pattern = r'\{(\d+:\d+)\}\s*(.*?)(?=\{\d+:\d+\}|$)'
        matches = re.findall(pattern, verses)

        verse_dict = {verse: verse_text.strip() for verse, verse_text in matches}

        return append_text, verse_dict

    def runExtraction(self):
        books = {}
        current_book = None

        self.extractTableOFContents()

        for i in range(self.start_page, len(self.reader.pages)):
            start_of_chapter = False
            text = self.reader.pages[i].extract_text().strip()

            if "{1:1}" in text:
                start_of_chapter = True
            
            book_name = self.getBookNameFromHeader(text)
            if book_name == "Song":
                book_name = "Song of Songs"
            
            if book_name and "Matthew" in book_name:
                self.testament = "New Testament"
            
            if self.testament not in books:
                books[self.testament] = {}
            
            if book_name and book_name != "Psalms":
               book_text = self.cleanBookText(text) 
               book_verses = self.getVerses(book_text)
            
            if start_of_chapter:
                current_book = book_name    
                books[self.testament][current_book] = book_verses[1]
            else:
                if book_verses[0] is not None:
                    last_verse = books[self.testament][current_book]
                    last_key = list(last_verse.keys())[-1]
                    last_verse[last_key] += " " + book_verses[0]
                if book_verses[1] is not None:
                    books[self.testament][current_book].update(book_verses[1])
            
        utils = BibleUtilities()
        utils.saveFile(books,"verses.json")