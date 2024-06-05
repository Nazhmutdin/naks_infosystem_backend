import os
from pathlib import Path

from dotenv import load_dotenv


if os.getenv("MODE") == "PROD":
    load_dotenv(f"{Path.cwd().parent}/.env")
else:
    load_dotenv(f"{Path.cwd().parent}/.dev.env")


class Settings:

    @classmethod
    def DB_NAME(cls) -> str:
        return os.getenv("DATABASE_NAME")
    
    
    @classmethod
    def DB_PASSWORD(cls) -> str:
        return os.getenv("DATABASE_PASSWORD")
    

    @classmethod
    def HOST(cls) -> str:
        return os.getenv("HOST")
    

    @classmethod
    def USER(cls) -> str:
        return os.getenv("USER")
    

    @classmethod
    def PORT(cls) -> str:
        return os.getenv("PORT")
    

    @classmethod
    def SECRET_KEY(cls) -> str:
        return os.getenv("SECRET_KEY")
    

    @classmethod
    def BASE_DIR(cls) -> Path:
        return Path(os.path.dirname(os.path.abspath(__file__))).parent
