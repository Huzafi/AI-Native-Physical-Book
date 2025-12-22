"""
Comprehensive logging configuration for AI-Native Book backend
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Set up comprehensive logging for the application
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Define log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
    )

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    # File handler for general logs
    if log_file is None:
        log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    # Specialized loggers for different components
    setup_component_loggers(log_level)

    return root_logger

def setup_component_loggers(log_level):
    """
    Set up specialized loggers for different components
    """
    components = [
        'api',           # API request/response logging
        'database',      # Database operations
        'search',        # Search functionality
        'ai_assistant',  # AI assistant operations
        'translation',   # Translation services
        'cache',         # Caching operations
        'security',      # Security-related events
        'performance'    # Performance monitoring
    ]

    for component in components:
        logger = logging.getLogger(f'app.{component}')
        logger.setLevel(log_level)

def get_logger(name):
    """
    Get a logger for a specific component
    """
    return logging.getLogger(f'app.{name}')

def log_api_request(request, response_time=None, status_code=None):
    """
    Log API request details
    """
    logger = get_logger('api')
    logger.info(f"API Request: {request.method} {request.url.path} - "
                f"Response time: {response_time}s - Status: {status_code}")

def log_database_operation(operation, table, duration=None, success=True):
    """
    Log database operations
    """
    logger = get_logger('database')
    status = "SUCCESS" if success else "FAILED"
    duration_str = f" ({duration:.3f}s)" if duration else ""
    logger.info(f"DB Operation: {operation} on {table}{duration_str} - {status}")

def log_search_query(query, results_count, duration):
    """
    Log search queries
    """
    logger = get_logger('search')
    logger.info(f"Search Query: '{query}' - Results: {results_count} - Duration: {duration:.3f}s")

def log_ai_request(question, response_length, duration, success=True):
    """
    Log AI assistant requests
    """
    logger = get_logger('ai_assistant')
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"AI Request: '{question[:50]}...' - Response length: {response_length} - "
                f"Duration: {duration:.3f}s - {status}")

def log_translation_request(content_id, source_lang, target_lang, success=True):
    """
    Log translation requests
    """
    logger = get_logger('translation')
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Translation: {content_id} from {source_lang} to {target_lang} - {status}")

def log_performance_event(event_name, duration, metadata=None):
    """
    Log performance-related events
    """
    logger = get_logger('performance')
    metadata_str = f" - Metadata: {metadata}" if metadata else ""
    logger.info(f"Performance Event: {event_name} - Duration: {duration:.3f}s{metadata_str}")

def log_security_event(event_type, user_info=None, ip_address=None):
    """
    Log security-related events
    """
    logger = get_logger('security')
    user_str = f" - User: {user_info}" if user_info else ""
    ip_str = f" - IP: {ip_address}" if ip_address else ""
    logger.warning(f"Security Event: {event_type}{user_str}{ip_str}")

# Initialize the logging system
setup_logging()