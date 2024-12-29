import logging
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger instance with both file and console handlers.
    
    Args:
        name: Optional name for the logger. If None, uses root logger.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only add handlers if they haven't been added yet
    if not logger.handlers:
        # Configure logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Set logging level
        logger.setLevel(logging.DEBUG)
    
    return logger
