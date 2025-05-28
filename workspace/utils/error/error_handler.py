from workspace.config.rules import error_codes

class APIError(Exception):
    def __init__(self, message, status_code=None, code=error_codes.API_TIMEOUT):
        super().__init__(message)
        self.status_code = status_code
        self.code = code

class ValidationError(Exception):
    def __init__(self, message, code="VALIDATION_ERROR"):
        super().__init__(message)
        self.code = code

def handle_exception(e):
    if isinstance(e, APIError):
        return {
            "type": "api",
            "code": e.code,
            "status_code": e.status_code,
            "msg": str(e),
        }
    elif isinstance(e, ValidationError):
        return {
            "type": "validation",
            "code": e.code,
            "msg": str(e),
        }
    else:
        return {
            "type": "unknown",
            "msg": str(e),
        }
