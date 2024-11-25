import os
from pathlib import Path

from dotenv import load_dotenv


if not os.getenv("MODE"):
    load_dotenv(f"{Path(os.path.dirname(os.path.abspath(__file__))).parent.parent}/.dev.env", override=True)


class DBConfig:
    @classmethod
    def DB_NAME(cls) -> str:
        return os.getenv("DATABASE_NAME")
    
    
    @classmethod
    def DB_PASSWORD(cls) -> str:
        return os.getenv("DATABASE_PASSWORD")
    

    @classmethod
    def USER(cls) -> str:
        return os.getenv("USER")


    @classmethod
    def DB_HOST(cls) -> str:
        return os.getenv("HOST")
    

    @classmethod
    def DB_PORT(cls) -> str:
        return os.getenv("PORT")
    

    @classmethod
    def DB_URL(cls) -> str:
        return "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
            cls.USER(), 
            cls.DB_PASSWORD(), 
            cls.DB_HOST(), 
            cls.DB_PORT(), 
            cls.DB_NAME()
        )
    

class ApplicationConfig:

    @classmethod
    def SECRET_KEY(cls) -> str:
        return os.getenv("SECRET_KEY")


    @classmethod
    def BASE_DIR(cls) -> Path:
        return Path(os.path.dirname(os.path.abspath(__file__))).parent
