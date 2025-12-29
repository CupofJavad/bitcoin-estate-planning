"""Application configuration."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Bitcoin Estate Planning Platform"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # FastAPI Users
    USERS_VERIFICATION_TOKEN_SECRET: str = ""  # Will use SECRET_KEY if not set

    # Database
    DATABASE_URL: str = ""  # If provided, will be used instead of individual components
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "bitcoin_estate"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""  # Optional if DATABASE_URL is provided

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Bitcoin
    BITCOIN_NETWORK: str = "testnet"
    BITCOIN_RPC_URL: str = "http://localhost:18332"
    BITCOIN_RPC_USER: str = "bitcoin"
    BITCOIN_RPC_PASSWORD: str = "bitcoin"

    # CORS - can be comma-separated string or list
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:3001"

    # Chatbot
    OPENAI_API_KEY: str = ""
    CHATBOT_MODEL: str = "gpt-3.5-turbo"
    CHATBOT_MAX_TOKENS: int = 500
    CHATBOT_TEMPERATURE: float = 0.7

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def database_url(self) -> str:
        """Get database connection URL."""
        # If DATABASE_URL is provided, use it (convert postgresql:// to postgresql+asyncpg://)
        if self.DATABASE_URL:
            # Convert postgresql:// to postgresql+asyncpg:// for asyncpg
            if self.DATABASE_URL.startswith("postgresql://"):
                return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif self.DATABASE_URL.startswith("postgresql+asyncpg://"):
                return self.DATABASE_URL
            else:
                return self.DATABASE_URL
        # Otherwise, construct from individual components
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()

