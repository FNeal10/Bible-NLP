import os
import pandas as pd
from .utils import BibleUtilities

class BibleTransformer:
    def __init__(self):
        pass



    def runTransform(self) -> pd.DataFrame:
        """
        Reads the Bible verses JSON and returns a flattened DataFrame
        with columns: testament, book, chapter, verse, text
        """
        # Read nested JSON using your utility function
        verses = BibleUtilities.readFile("verses.json")  # returns dict

        # Build list of records inline
        records = []
        for testament, books in verses.items():
            for book, verses_dict in books.items():
                for verse_ref, text in verses_dict.items():
                    chapter, verse = map(int, verse_ref.split(":"))
                    records.append({
                        "testament": testament,
                        "book": book,
                        "chapter": chapter,
                        "verse": verse,
                        "text": text
                    })


        df = pd.DataFrame(records)
        BibleUtilities.saveAsCSV(df, "bible_verses.csv")