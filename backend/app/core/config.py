from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "dev"
    DATABASE_URL: str = "postgresql://localhost:5432/cinefluent_dev"
    
    # External APIs
    OPENSUBTITLES_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production-make-it-long-and-random"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()