from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str = "devsecret"
    model_config = {
        "env_file": ".env"
    }

settings = Settings() # type: ignore
