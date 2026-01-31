"""
AI Practice Platform Configuration

Environment-based configuration management.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'ai-practice-platform-dev-key')
    DEBUG: bool = False
    TESTING: bool = False

    # Claude API
    ANTHROPIC_API_KEY: Optional[str] = os.environ.get('ANTHROPIC_API_KEY')
    CLAUDE_MODEL: str = os.environ.get('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
    CLAUDE_MAX_TOKENS: int = int(os.environ.get('CLAUDE_MAX_TOKENS', 4096))

    # Database (for future use)
    DATABASE_URL: str = os.environ.get('DATABASE_URL', 'sqlite:///data/platform.db')

    # Application
    APP_NAME: str = "AI Practice Platform"
    APP_VERSION: str = "1.0.0"
    COMPANY_NAME: str = "Patriot Tech Systems Consulting LLC"

    # Assessment
    DEFAULT_SECTOR: str = "general"
    ASSESSMENT_TIMEOUT_HOURS: int = 24

    # Document Generation
    MAX_DOCUMENT_LENGTH: int = 50000
    DOCUMENT_STORAGE_PATH: str = os.environ.get('DOCUMENT_PATH', 'output/documents')

    # Logging
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


@dataclass
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG: bool = True
    LOG_LEVEL: str = 'DEBUG'


@dataclass
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG: bool = False
    LOG_LEVEL: str = 'WARNING'


@dataclass
class TestingConfig(Config):
    """Testing configuration"""
    TESTING: bool = True
    DEBUG: bool = True


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development').lower()

    configs = {
        'development': DevelopmentConfig(),
        'production': ProductionConfig(),
        'testing': TestingConfig()
    }

    return configs.get(env, DevelopmentConfig())


# Export default config
config = get_config()
