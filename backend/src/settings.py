from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MONGO_CONNECTION_URI: str
    OPENAI_API_KEY: str


global_settings = Settings()
