#!/usr/bin/env python3
"""
Database creation script for Async Document Q&A Microservice
"""
import asyncio
import asyncpg
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = await asyncpg.connect(
            user='postgres',
            password='sairaj',
            host='localhost',
            port=5432,
            database='postgres'
        )
        
        # Check if database exists
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            'document_qa'
        )
        
        if not result:
            # Create database
            await conn.execute('CREATE DATABASE document_qa')
            logger.info("Database 'document_qa' created successfully!")
        else:
            logger.info("Database 'document_qa' already exists!")
        
        await conn.close()
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        logger.info("Please make sure PostgreSQL is running and password is correct.")
        raise


if __name__ == "__main__":
    asyncio.run(create_database()) 