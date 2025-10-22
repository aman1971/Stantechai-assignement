from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str
    
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

