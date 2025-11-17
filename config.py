"""
Configuration management for Qase Reporter
Supports both local .env files and Streamlit secrets for deployment
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()


class Config:
    """Configuration class to store settings"""
    
    # Detect if running in Streamlit Cloud
    @staticmethod
    def _get_secret(key: str, default: Optional[str] = None):
        """
        Get secret from Streamlit secrets (cloud) or environment variables (local)
        
        Args:
            key: The secret key name
            default: Default value if not found
            
        Returns:
            Secret value or default
        """
        try:
            # Try Streamlit secrets first (for cloud deployment)
            import streamlit as st
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except (ImportError, FileNotFoundError, KeyError):
            pass
        
        # Fall back to environment variables (for local development)
        return os.getenv(key, default)
    
    # Qase API Configuration
    QASE_API_TOKEN = None  # Will be set dynamically
    PROJECT_CODE = None  # Will be set dynamically
    QASE_PROJECT_CODE = None  # Alias for compatibility
    
    @classmethod
    def load_config(cls):
        """Load configuration from secrets or environment"""
        cls.QASE_API_TOKEN = cls._get_secret('QASE_API_TOKEN', 'your_qase_api_token_here')
        cls.PROJECT_CODE = cls._get_secret('QASE_PROJECT_CODE', 'PROJ')
        cls.QASE_PROJECT_CODE = cls.PROJECT_CODE
    
    # Export settings
    EXPORT_DIR = None
    
    # API settings (Based on Qase API Documentation)
    API_BASE_URL = "https://api.qase.io/v1"
    API_TIMEOUT = None
    MAX_RESULTS = None
    API_RATE_LIMIT = 600
    API_RETRY_AFTER = 60
    
    # Sprint Configuration
    CURRENT_SPRINT_NAME = None
    
    # Analysis Parameters
    TEAM_PRODUCTIVITY_DAYS = None
    PASS_RATE_TREND_MONTHS = None
    
    # Output Configuration
    OUTPUT_FORMAT = None
    
    # Team Members
    TEAM_MEMBERS = [
        "Chinthaka Somarathna",
        "Rukshani Jayathilaka",
        "Madushika Deshappriya",
        "Pasindu Liyanage"
    ]
    
    # Quality Targets
    PASS_RATE_TARGET = None
    EXECUTION_RATE_TARGET = None
    
    @classmethod
    def load_all_settings(cls):
        """Load all configuration settings"""
        cls.load_config()
        cls.EXPORT_DIR = cls._get_secret('EXPORT_DIR', 'exports')

        # API_TIMEOUT (safe parse)
        _api_timeout = cls._get_secret('API_TIMEOUT', '300')
        try:
            cls.API_TIMEOUT = int(_api_timeout) if _api_timeout is not None else 300
        except (TypeError, ValueError):
            cls.API_TIMEOUT = 300

        # MAX_RESULTS (safe parse)
        _max_results = cls._get_secret('MAX_RESULTS', '1000')
        try:
            cls.MAX_RESULTS = int(_max_results) if _max_results is not None else 1000
        except (TypeError, ValueError):
            cls.MAX_RESULTS = 1000

        cls.CURRENT_SPRINT_NAME = cls._get_secret('CURRENT_SPRINT_NAME', 'Sprint 24')

        # TEAM_PRODUCTIVITY_DAYS (safe parse)
        _team_days = cls._get_secret('TEAM_PRODUCTIVITY_DAYS', '30')
        try:
            cls.TEAM_PRODUCTIVITY_DAYS = int(_team_days) if _team_days is not None else 30
        except (TypeError, ValueError):
            cls.TEAM_PRODUCTIVITY_DAYS = 30

        # PASS_RATE_TREND_MONTHS (safe parse)
        _pass_rate_trend = cls._get_secret('PASS_RATE_TREND_MONTHS', '6')
        try:
            cls.PASS_RATE_TREND_MONTHS = int(_pass_rate_trend) if _pass_rate_trend is not None else 6
        except (TypeError, ValueError):
            cls.PASS_RATE_TREND_MONTHS = 6

        cls.OUTPUT_FORMAT = cls._get_secret('OUTPUT_FORMAT', 'both')

        # PASS_RATE_TARGET (safe parse)
        _pass_rate_target = cls._get_secret('PASS_RATE_TARGET', '90.0')
        try:
            cls.PASS_RATE_TARGET = float(_pass_rate_target) if _pass_rate_target is not None else 90.0
        except (TypeError, ValueError):
            cls.PASS_RATE_TARGET = 90.0

        # EXECUTION_RATE_TARGET (safe parse)
        _exec_rate_target = cls._get_secret('EXECUTION_RATE_TARGET', '80.0')
        try:
            cls.EXECUTION_RATE_TARGET = float(_exec_rate_target) if _exec_rate_target is not None else 80.0
        except (TypeError, ValueError):
            cls.EXECUTION_RATE_TARGET = 80.0
    
    # Export settings
    EXPORT_DIR = os.getenv('EXPORT_DIR', 'exports')
    
    # API settings (Based on Qase API Documentation)
    # Reference: https://developers.qase.io/reference/introduction-to-the-qase-api
    API_BASE_URL = "https://api.qase.io/v1"  # Official Qase API endpoint
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '300'))
    MAX_RESULTS = int(os.getenv('MAX_RESULTS', '1000'))
    API_RATE_LIMIT = 600  # 600 requests per minute (official limit)
    API_RETRY_AFTER = 60  # Retry after 60 seconds if rate limited
    
    # Sprint Configuration
    CURRENT_SPRINT_NAME = os.getenv('CURRENT_SPRINT_NAME', 'Sprint 24')
    
    # Analysis Parameters
    TEAM_PRODUCTIVITY_DAYS = int(os.getenv('TEAM_PRODUCTIVITY_DAYS', '30'))
    PASS_RATE_TREND_MONTHS = int(os.getenv('PASS_RATE_TREND_MONTHS', '6'))
    
    # Output Configuration
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'both')  # Options: 'excel', 'chart', or 'both'
    
    # Team Members (Your QA Team)
    TEAM_MEMBERS = [
        "Chinthaka Somarathna",
        "Rukshani Jayathilaka",
        "Madushika Deshappriya",
        "Pasindu Liyanage"
    ]
    
    # Quality Targets
    PASS_RATE_TARGET = float(os.getenv('PASS_RATE_TARGET', '90.0'))
    EXECUTION_RATE_TARGET = float(os.getenv('EXECUTION_RATE_TARGET', '80.0'))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.QASE_API_TOKEN or cls.QASE_API_TOKEN == 'your_qase_api_token_here':
            raise ValueError(
                "QASE_API_TOKEN not found or not configured. "
                "Please create a .env file with: QASE_API_TOKEN=your_token_here"
            )
        
        if not cls.PROJECT_CODE or cls.PROJECT_CODE == 'PROJ':
            raise ValueError(
                "QASE_PROJECT_CODE not found or using default. "
                "Please set in .env file: QASE_PROJECT_CODE=your_project_code"
            )
        
        # Ensure EXPORT_DIR is a valid string path and create directory if it doesn't exist
        export_dir = cls.EXPORT_DIR or 'exports'
        # Normalize to string to satisfy type checkers and avoid passing None
        export_dir = str(export_dir)
        cls.EXPORT_DIR = export_dir
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        return True
    
    @classmethod
    def display_config(cls):
        """Display current configuration (for debugging)"""
        print("\n" + "=" * 60)
        print("CURRENT CONFIGURATION")
        print("=" * 60)
        print(f"Project Code: {cls.PROJECT_CODE}")
        print(f"Sprint Name: {cls.CURRENT_SPRINT_NAME}")
        print(f"Team Productivity Days: {cls.TEAM_PRODUCTIVITY_DAYS}")
        print(f"Pass Rate Trend Months: {cls.PASS_RATE_TREND_MONTHS}")
        print(f"Output Format: {cls.OUTPUT_FORMAT}")
        print(f"Pass Rate Target: {cls.PASS_RATE_TARGET}%")
        print(f"Execution Rate Target: {cls.EXECUTION_RATE_TARGET}%")
        print(f"Export Directory: {cls.EXPORT_DIR}")
        print(f"API Token: {'*' * 20} (hidden)")
        print("=" * 60 + "\n")


# Auto-load configuration on module import
Config.load_config()
