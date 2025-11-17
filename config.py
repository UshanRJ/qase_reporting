"""
Configuration management for Qase Reporter
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to store settings"""
    
    # Qase API Configuration
    QASE_API_TOKEN = os.getenv('QASE_API_TOKEN', 'your_qase_api_token_here')
    PROJECT_CODE = os.getenv('QASE_PROJECT_CODE', 'PROJ')
    QASE_PROJECT_CODE = PROJECT_CODE  # Alias for compatibility
    
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
        
        # Create export directory if it doesn't exist
        if not os.path.exists(cls.EXPORT_DIR):
            os.makedirs(cls.EXPORT_DIR)
        
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