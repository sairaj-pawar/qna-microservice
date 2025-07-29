# Simple configuration without pydantic_settings
import os
from typing import Optional


class Settings:
    # Database
    database_url: str = "postgresql+asyncpg://postgres:sairaj@localhost:5432/document_qa"
    
    # Application
    secret_key: str = "your-secret-key-here-change-in-production"
    debug: bool = True
    log_level: str = "INFO"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database for Docker
    postgres_user: str = "postgres"
    postgres_password: str = "sairaj"
    postgres_db: str = "document_qa"
    postgres_host: str = "db"
    postgres_port: int = 5432


settings = Settings() 