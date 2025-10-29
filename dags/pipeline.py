import os
from src.extract import BibleExtractor
from src.transform import BibleTransformer

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    extractor = BibleExtractor(
        source_path=os.getenv("DATA_SOURCE_PATH"),
        dump_path=os.getenv("DATA_DUMP_PATH"),
        start_page=21
    )

    extractor.runExtraction()

    transformer = BibleTransformer()
    transformer.runTransform()

