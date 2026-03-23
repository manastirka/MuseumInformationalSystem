"""Shared PostgreSQL connection helpers."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / '.env')


def get_database_url():
    """Return DATABASE_URL normalized for psycopg."""
    db_url = os.environ.get('DATABASE_URL', '')
    db_url = db_url.replace('postgresql+psycopg://', 'postgresql://')
    if not db_url:
        raise RuntimeError('DATABASE_URL is not configured')
    return db_url


def get_postgres_connection(**kwargs):
    """Create a psycopg connection using the configured database URL."""
    return psycopg.connect(get_database_url(), **kwargs)
