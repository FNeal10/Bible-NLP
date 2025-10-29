import os
import pandas as pd
import json

class BibleUtilities:

    @staticmethod
    def saveFile(contents: dict, filename:str) -> None:
        try:
            dump_path = os.getenv("DATA_DUMP_PATH") + filename
            with open(dump_path, "w") as file:
                json.dump(contents, file, indent=4)
        except Exception as e:
            raise Exception(f"Failed to save file at {dump_path}: {str(e)}")
        
    @staticmethod
    def saveAsCSV(data: pd.DataFrame, filename:str) -> None:
        dump_path = os.getenv("DATA_DUMP_PATH") + filename
        data.to_csv(dump_path, index=False, encoding="utf-8")

    @staticmethod
    def readFile(filename:str):
        try:
            source_path = os.getenv("DATA_DUMP_PATH") + filename
            with open(source_path, "r") as file:
                contents = json.load(file)
            return contents
        except Exception as e:
            raise Exception(f"Failed to read file at {source_path}: {str(e)}")
