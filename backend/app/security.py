"""
Security configuration and utilities for AI-Native Book backend
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security settings
class SecurityConfig:
    SECRET_KEY: str = "your-secret-key-change-this-in-production"  # This should be set via environment
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

security_config = SecurityConfig()

# Security utilities
class SecurityUtils:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate a hash for a password"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, security_config.SECRET_KEY, algorithm=security_config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=security_config.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, security_config.SECRET_KEY, algorithm=security_config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token and return its payload"""
        try:
            payload = jwt.decode(token, security_config.SECRET_KEY, algorithms=[security_config.ALGORITHM])
            return payload
        except jwt.PyJWTError as e:
            logger.warning(f"Token verification failed: {e}")
            return None

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength"""
        issues = []

        if len(password) < security_config.PASSWORD_MIN_LENGTH:
            issues.append(f"Password must be at least {security_config.PASSWORD_MIN_LENGTH} characters long")

        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")

        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")

        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one number")

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            issues.append("Password should contain at least one special character")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues
        }

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Basic input sanitization to prevent XSS and SQL injection"""
        if not input_str:
            return input_str

        # Remove potentially dangerous characters
        # This is a basic implementation - consider using a dedicated library for production
        sanitized = input_str.replace('<', '&lt;').replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')
        sanitized = sanitized.replace('(', '&#x28;').replace(')', '&#x29;')

        # Remove potential SQL injection patterns
        sql_patterns = ['--', ';', '/*', '*/', 'xp_', 'sp_']
        for pattern in sql_patterns:
            if pattern in sanitized.lower():
                sanitized = sanitized.replace(pattern, '')

        return sanitized

    @staticmethod
    def generate_csrf_token() -> str:
        """Generate a CSRF token"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data using SHA-256"""
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def get_client_ip(request: Request) -> str:
        """Get client IP address from request, considering proxies"""
        # Check for forwarded headers first (for when behind a proxy/load balancer)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            # Handle multiple IPs in the header (comma separated)
            client_ip = forwarded_for.split(",")[0].strip()
            return client_ip

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        forwarded_host = request.headers.get("x-forwarded-host")
        if forwarded_host:
            # If we only have the host, we can't determine the IP
            pass

        # Fallback to client attribute
        if hasattr(request, "client") and request.client:
            return request.client.host

        # Last resort
        return "127.0.0.1"

# Rate limiting utilities
class RateLimiting:
    def __init__(self):
        self.requests = {}
        self.blocked_ips = {}

    def is_rate_limited(self, identifier: str, limit: int, window: int) -> bool:
        """
        Check if an identifier is rate limited
        :param identifier: Unique identifier (IP, user ID, etc.)
        :param limit: Number of requests allowed
        :param window: Time window in seconds
        :return: True if rate limited, False otherwise
        """
        current_time = datetime.now()

        # Check if IP is blocked
        if identifier in self.blocked_ips:
            block_until = self.blocked_ips[identifier]
            if current_time < block_until:
                return True
            else:
                # Remove expired block
                del self.blocked_ips[identifier]

        # Get or initialize request history
        if identifier not in self.requests:
            self.requests[identifier] = []

        # Clean old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < timedelta(seconds=window)
        ]

        # Check if limit exceeded
        if len(self.requests[identifier]) >= limit:
            # Block the identifier for a period if they exceed limits too often
            if len(self.requests[identifier]) > limit * 2:  # Double the limit
                self.blocked_ips[identifier] = current_time + timedelta(minutes=30)
                return True
            return True

        # Add current request
        self.requests[identifier].append(current_time)
        return False

# Global rate limiter instance
rate_limiter = RateLimiting()

# Security middleware for request logging and monitoring
class SecurityMiddleware:
    """
    Security middleware to log requests and monitor for suspicious activity
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # Process request
        request = Request(scope)

        # Log the request for security monitoring
        client_ip = SecurityUtils.get_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")
        path = request.url.path
        method = request.method

        logger.info(f"SECURITY_LOG: {method} {path} from {client_ip} - User-Agent: {user_agent}")

        # Check for suspicious patterns in the request
        suspicious_found = False
        for header, value in request.headers.items():
            if self._check_suspicious_content(value):
                logger.warning(f"Suspicious content detected in header {header} from {client_ip}")
                suspicious_found = True

        # Check query parameters
        for param_name, param_value in request.query_params.items():
            if self._check_suspicious_content(param_value):
                logger.warning(f"Suspicious content detected in query param {param_name} from {client_ip}")
                suspicious_found = True

        # Check request body (for POST/PUT requests)
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                body_str = body_bytes.decode('utf-8', errors='ignore')
                if self._check_suspicious_content(body_str):
                    logger.warning(f"Suspicious content detected in request body from {client_ip}")
                    suspicious_found = True
            except:
                # If we can't read the body, continue but log
                logger.warning(f"Could not read request body from {client_ip}")

        # Add security headers to response
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Add security headers
                headers = message.get("headers", [])
                headers.append([b"x-content-type-options", b"nosniff"])
                headers.append([b"x-frame-options", b"SAMEORIGIN"])
                headers.append([b"x-xss-protection", b"1; mode=block"])
                headers.append([b"strict-transport-security", b"max-age=31536000; includeSubDomains"])
                headers.append([b"referrer-policy", b"no-referrer-when-downgrade"])
                headers.append([b"content-security-policy", b"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;"])
                message["headers"] = headers

            await send(message)

        return await self.app(scope, receive, send_wrapper)

    def _check_suspicious_content(self, content: str) -> bool:
        """Check if content contains suspicious patterns"""
        if not content:
            return False

        suspicious_patterns = [
            # SQL injection patterns
            "union select",
            "drop table",
            "exec(",
            "execute(",
            "xp_",
            "sp_",
            # XSS patterns
            "<script",
            "javascript:",
            "vbscript:",
            "onerror=",
            "onload=",
            # Common attack patterns
            "../../../../",
            "%00",
            "eval(",
            "document.cookie"
        ]

        content_lower = content.lower()
        for pattern in suspicious_patterns:
            if pattern in content_lower:
                return True

        return False

# Initialize security utilities
security_utils = SecurityUtils()