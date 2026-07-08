"""
Museum Information System - Configuration Management
Centralizes all configuration with environment-based settings
"""

import os
from datetime import timedelta
from typing import Optional

DEFAULT_LOG_DIR = os.environ.get('LOG_DIR', 'logs')
DEFAULT_LOG_FILE = os.path.join(DEFAULT_LOG_DIR, 'museum_info_system.log')


class Config:
    """Base configuration class."""

    # Flask Core
    SECRET_KEY: Optional[str] = os.environ.get('SECRET_KEY')
    DEBUG: bool = False
    TESTING: bool = False

    # Security Settings
    WTF_CSRF_ENABLED: bool = os.environ.get('WTF_CSRF_ENABLED', 'True').lower() == 'true'
    WTF_CSRF_TIME_LIMIT: int = int(os.environ.get('WTF_CSRF_TIME_LIMIT', '3600'))

    # Session Configuration
    SESSION_TYPE: str = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_FILE_DIR: str = os.environ.get('SESSION_FILE_DIR', './flask_session')
    SESSION_PERMANENT: bool = os.environ.get('SESSION_PERMANENT', 'False').lower() == 'true'
    SESSION_USE_SIGNER: bool = os.environ.get('SESSION_USE_SIGNER', 'True').lower() == 'true'
    SESSION_KEY_PREFIX: str = os.environ.get('SESSION_KEY_PREFIX', 'museum:')
    SESSION_INVALIDATE_ON_RESTART: bool = os.environ.get('SESSION_INVALIDATE_ON_RESTART', 'False').lower() == 'true'
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(
        seconds=int(os.environ.get('PERMANENT_SESSION_LIFETIME', '28800'))  # 8 hours default
    )
    SESSION_COOKIE_SECURE: bool = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY: bool = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
    SESSION_COOKIE_SAMESITE: str = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')

    # Rate Limiting
    RATELIMIT_ENABLED: bool = os.environ.get('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_STORAGE_URL: str = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY: str = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED: bool = True

    # Password Policy
    PASSWORD_MIN_LENGTH: int = int(os.environ.get('PASSWORD_MIN_LENGTH', '12'))
    PASSWORD_REQUIRE_UPPERCASE: bool = os.environ.get('PASSWORD_REQUIRE_UPPERCASE', 'True').lower() == 'true'
    PASSWORD_REQUIRE_LOWERCASE: bool = os.environ.get('PASSWORD_REQUIRE_LOWERCASE', 'True').lower() == 'true'
    PASSWORD_REQUIRE_NUMBERS: bool = os.environ.get('PASSWORD_REQUIRE_NUMBERS', 'True').lower() == 'true'
    PASSWORD_REQUIRE_SPECIAL: bool = os.environ.get('PASSWORD_REQUIRE_SPECIAL', 'True').lower() == 'true'

    # Account Security
    MAX_LOGIN_ATTEMPTS: int = int(os.environ.get('MAX_LOGIN_ATTEMPTS', '5'))
    ACCOUNT_LOCKOUT_DURATION: int = int(os.environ.get('ACCOUNT_LOCKOUT_DURATION', '1800'))  # 30 minutes
    SESSION_TIMEOUT_WARNING: int = int(os.environ.get('SESSION_TIMEOUT_WARNING', '300'))  # 5 minutes

    # Database Configuration
    DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
    DB_PORT: int = int(os.environ.get('DB_PORT', '3306'))
    DB_USER: str = os.environ.get('DB_USER', 'root')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD', '')
    DB_NAME: str = os.environ.get('DB_NAME', 'museum_timesheet_local')
    DB_CHARSET: str = os.environ.get('DB_CHARSET', 'utf8mb4')

    # Connection Pooling
    DB_POOL_SIZE: int = int(os.environ.get('DB_POOL_SIZE', '10'))
    DB_POOL_RECYCLE: int = int(os.environ.get('DB_POOL_RECYCLE', '3600'))
    DB_POOL_PRE_PING: bool = os.environ.get('DB_POOL_PRE_PING', 'True').lower() == 'true'

    # SQLite Databases
    MINERAL_DATABASE_PATH: str = os.environ.get('MINERAL_DATABASE_PATH', 'PrirodnjackiMuzej/prirodnjacki_muzej.sqlite')
    BIRD_DATABASE_PATH: str = os.environ.get('BIRD_DATABASE_PATH', 'data/bird_ringing.db')
    INVENTORY_DATABASE_PATH: str = os.environ.get('INVENTORY_DATABASE_PATH', 'data/inventory_book.db')

    # Authentication
    AUTH_SYSTEM_ENABLED: bool = os.environ.get('AUTH_SYSTEM_ENABLED', 'True').lower() == 'true'
    ENABLE_FALLBACK_AUTH: bool = os.environ.get('ENABLE_FALLBACK_AUTH', 'False').lower() == 'true'
    REQUIRE_PASSWORD_CHANGE_ON_FIRST_LOGIN: bool = os.environ.get('REQUIRE_PASSWORD_CHANGE_ON_FIRST_LOGIN', 'True').lower() == 'true'
    CHAT_SERVICE_ENABLED: bool = os.environ.get('CHAT_SERVICE_ENABLED', 'False').lower() == 'true'

    # Admin Credentials
    ADMIN_EMAIL: str = os.environ.get('ADMIN_EMAIL', 'admin@nhmbeo.rs')
    ADMIN_USERNAME: Optional[str] = os.environ.get('ADMIN_USERNAME')
    ADMIN_DEFAULT_PASSWORD: Optional[str] = os.environ.get('ADMIN_DEFAULT_PASSWORD')

    # Logging
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.environ.get('LOG_FILE', DEFAULT_LOG_FILE)
    LOG_FORMAT: str = os.environ.get('LOG_FORMAT', 'json')
    LOG_MAX_BYTES: int = int(os.environ.get('LOG_MAX_BYTES', '10485760'))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.environ.get('LOG_BACKUP_COUNT', '10'))

    # Sentry
    SENTRY_DSN: Optional[str] = os.environ.get('SENTRY_DSN')
    SENTRY_ENVIRONMENT: str = os.environ.get('SENTRY_ENVIRONMENT', 'production')
    SENTRY_TRACES_SAMPLE_RATE: float = float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1'))
    SENTRY_SEND_DEFAULT_PII: bool = os.environ.get('SENTRY_SEND_DEFAULT_PII', 'False').lower() == 'true'

    # OpenTelemetry
    OTEL_ENABLED: bool = os.environ.get('OTEL_ENABLED', 'False').lower() == 'true'
    OTEL_SERVICE_NAME: str = os.environ.get('OTEL_SERVICE_NAME', 'museum-info-system')
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')

    # External APIs
    MINDAT_API_KEY: Optional[str] = os.environ.get('MINDAT_API_KEY')
    RRUFF_API_KEY: Optional[str] = os.environ.get('RRUFF_API_KEY')

    # Server
    HOST: str = os.environ.get('HOST', '0.0.0.0')
    PORT: int = int(os.environ.get('PORT', '5555'))
    WORKERS: int = int(os.environ.get('WORKERS', '1'))

    # File Upload
    MAX_CONTENT_LENGTH: int = int(os.environ.get('MAX_CONTENT_LENGTH', '52428800'))  # 50MB
    UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER', 'storage/uploads')
    ALLOWED_EXTENSIONS: set = set(os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif,pdf,xlsx,csv').split(','))

    # Image Storage - actual image files stored here, references in PostgreSQL
    # On server, set IMAGE_STORAGE_PATH to a mount point on the storage drive
    IMAGE_STORAGE_PATH: str = os.environ.get('IMAGE_STORAGE_PATH', './ImagesDatabase')

    # Document library - uploaded document files stored here, references in
    # PostgreSQL. On server, set DOCUMENTS_STORAGE_PATH under /data/mis.
    DOCUMENTS_STORAGE_PATH: str = os.environ.get('DOCUMENTS_STORAGE_PATH', './data/dokumenti')

    # Фототека - RAW originals are write-once (production: /data/arhiva, in
    # the nightly backup); derivatives are regenerable (production:
    # /data/mis/media, excluded from backup).
    FOTOTEKA_ARHIVA_PATH: str = os.environ.get('FOTOTEKA_ARHIVA_PATH', './data/arhiva')
    FOTOTEKA_MEDIA_PATH: str = os.environ.get('FOTOTEKA_MEDIA_PATH', './data/fototeka_media')
    # Samba share mount that the import screen scans (admin enters a subpath
    # under this root; the app never reads outside it).
    FOTOTEKA_IMPORT_PATH: str = os.environ.get('FOTOTEKA_IMPORT_PATH', './data/fototeka_import')
    # Serve legacy specimen images from Фототека (after migration) instead of
    # the old images store. Off by default; flip on per host only once
    # migrate_images_to_fototeka.py has been run and verified.
    FOTOTEKA_SERVE_LEGACY_IMAGES: bool = os.environ.get(
        'FOTOTEKA_SERVE_LEGACY_IMAGES', 'false').strip().lower() in ('1', 'true', 'yes', 'on')

    # Redis
    REDIS_URL: str = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE: str = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT: int = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '300'))
    CACHE_KEY_PREFIX: str = os.environ.get('CACHE_KEY_PREFIX', 'museum_cache:')

    # Email
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'smtp.nhmbeo.rs')
    MAIL_PORT: int = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS: bool = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME', 'noreply@nhmbeo.rs')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER: str = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@nhmbeo.rs')

    # Backup
    BACKUP_ENABLED: bool = os.environ.get('BACKUP_ENABLED', 'True').lower() == 'true'
    BACKUP_DIRECTORY: str = os.environ.get('BACKUP_DIRECTORY', '/var/backups/museum')
    BACKUP_RETENTION_DAYS: int = int(os.environ.get('BACKUP_RETENTION_DAYS', '30'))

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET: Optional[str] = os.environ.get('AWS_S3_BUCKET')
    AWS_REGION: str = os.environ.get('AWS_REGION', 'eu-central-1')

    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-secret-key')
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    ENABLE_FALLBACK_AUTH = True  # Allow fallback auth in dev


class TestingConfig(Config):
    """Testing configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'test-secret-key')
    TESTING = True
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    RATELIMIT_ENABLED = False  # Disable rate limiting for testing


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_SECURE = True  # Require HTTPS
    ENABLE_FALLBACK_AUTH = False  # No fallback auth in production

    @classmethod
    def init_app(cls, app):
        """Production-specific initialization."""
        Config.init_app(app)

        if not app.config.get('SECRET_KEY'):
            raise RuntimeError('SECRET_KEY must be set in production')
        if app.config.get('ENABLE_FALLBACK_AUTH'):
            raise RuntimeError('ENABLE_FALLBACK_AUTH must be disabled in production')
        if not app.config.get('SESSION_COOKIE_SECURE'):
            raise RuntimeError('SESSION_COOKIE_SECURE must be enabled in production')
        session_type = os.environ.get('SESSION_TYPE', app.config.get('SESSION_TYPE', 'redis')).lower()
        redis_url = os.environ.get('REDIS_URL', app.config.get('REDIS_URL'))
        app.config['SESSION_TYPE'] = session_type
        app.config['REDIS_URL'] = redis_url

        if session_type != 'redis':
            raise RuntimeError('Production session storage must use Redis (SESSION_TYPE=redis)')
        if not redis_url:
            raise RuntimeError('REDIS_URL must be set in production for Redis sessions/shared state')

        if app.config.get('RATELIMIT_STORAGE_URL', 'memory://').startswith('memory'):
            app.config['RATELIMIT_STORAGE_URL'] = redis_url

        # Fail closed if in-memory rate limiting is used with multiple workers.
        ratelimit_url = app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
        workers = int(os.environ.get('WEB_CONCURRENCY', os.environ.get('WORKERS', app.config.get('WORKERS', 1))))
        if workers > 1 and ratelimit_url.startswith('memory'):
            raise RuntimeError(
                "RATELIMIT_STORAGE_URL must use shared storage when WORKERS > 1. "
                f"Current workers={workers}, storage={ratelimit_url!r}."
            )

        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        try:
            syslog_handler = SysLogHandler()
            syslog_handler.setLevel(logging.WARNING)
            app.logger.addHandler(syslog_handler)
        except OSError as exc:
            app.logger.warning(f'Syslog unavailable, skipping syslog handler: {exc}')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}


def get_config(config_name: Optional[str] = None) -> Config:
    """Get configuration by name."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')

    return config.get(config_name, ProductionConfig)
