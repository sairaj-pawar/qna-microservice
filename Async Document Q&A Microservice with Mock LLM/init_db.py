#!/usr/bin/env python3
"""
Database initialization script for Async Document Q&A Microservice
"""
import asyncio
import logging
from app.database import init_db
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Initialize the database"""
    try:
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main()) 