from contextvars import ContextVar

request_token = ContextVar('request_token', default=None)
