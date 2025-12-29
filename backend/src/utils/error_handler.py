"""Error handling and logging infrastructure for the RAG Chatbot application."""

import logging
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import traceback
import sys
from datetime import datetime
import json


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class AppException(HTTPException):
    """Custom application exception with detailed logging."""

    def __init__(self, status_code: int, detail: str, error_code: str = "APP_ERROR", additional_details: Optional[Dict] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.timestamp = datetime.utcnow().isoformat()
        self.additional_details = additional_details or {}

        # Log the exception with context
        log_data = {
            "error_code": error_code,
            "status_code": status_code,
            "detail": detail,
            "timestamp": self.timestamp,
            "additional_details": additional_details,
            "traceback": traceback.format_exc()
        }
        logger.error(log_data)


class ValidationError(AppException):
    """Exception for validation errors."""

    def __init__(self, detail: str, field: Optional[str] = None):
        additional_details = {"field": field} if field else {}
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
            additional_details=additional_details
        )


class DatabaseError(AppException):
    """Exception for database-related errors."""

    def __init__(self, detail: str, query_info: Optional[Dict] = None):
        additional_details = {"query_info": query_info} if query_info else {}
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR",
            additional_details=additional_details
        )


class ExternalServiceError(AppException):
    """Exception for external service errors (Cohere, Qdrant, etc.)."""

    def __init__(self, detail: str, service_name: str, service_error_code: Optional[str] = None):
        additional_details = {"service_name": service_name, "service_error_code": service_error_code} if service_error_code else {"service_name": service_name}
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External service {service_name} error: {detail}",
            error_code=f"{service_name.upper()}_ERROR",
            additional_details=additional_details
        )


class NotFoundError(AppException):
    """Exception for resource not found errors."""

    def __init__(self, resource_type: str, resource_id: str):
        detail = f"{resource_type} with ID '{resource_id}' not found"
        additional_details = {"resource_type": resource_type, "resource_id": resource_id}
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND_ERROR",
            additional_details=additional_details
        )


class RateLimitError(AppException):
    """Exception for rate limiting errors."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=message,
            error_code="RATE_LIMIT_ERROR"
        )


def handle_exception(exc: Exception, request_info: dict = None) -> JSONResponse:
    """Generic exception handler that logs and formats errors according to API contract."""

    # Log the exception with context
    logger.error({
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "request_info": request_info,
        "timestamp": datetime.utcnow().isoformat(),
        "traceback": traceback.format_exc()
    })

    # Return appropriate response based on exception type
    if isinstance(exc, AppException):
        error_response = {
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "details": exc.additional_details
            }
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    elif isinstance(exc, HTTPException):
        # Handle standard HTTP exceptions
        error_response = {
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail or f"HTTP {exc.status_code} error",
                "details": {}
            }
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    else:
        # For unhandled exceptions, return a generic 500 error following the API contract
        error_response = {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred",
                "details": {
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        }
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response
        )


def create_error_response(error_code: str, message: str, details: Optional[Dict] = None) -> Dict:
    """Create a standardized error response following the API contract."""
    error_response = {
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        }
    }
    return error_response


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)


def log_api_call(endpoint: str, method: str, user_id: str = None, params: dict = None):
    """Log API calls for monitoring and analytics."""
    logger.info({
        "event": "api_call",
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "params": params,
        "timestamp": datetime.utcnow().isoformat()
    })


def log_query(query_text: str, response_text: str, confidence_score: float, user_id: str = None):
    """Log query and response for quality assurance."""
    logger.info({
        "event": "query_response",
        "query": query_text,
        "response": response_text,
        "confidence_score": confidence_score,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    })