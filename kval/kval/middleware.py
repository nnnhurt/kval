import logging
from contextvars import ContextVar
from typing import Callable
from uuid import uuid4
from prometheus_client import Counter

from django.http import HttpRequest, HttpResponse


RESPONSE_HEADER_NAME = "X-Correlation-ID"
_correlation_id_var: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str:
    cid = _correlation_id_var.get()
    if cid:
        return cid
    cid = str(uuid4())
    _correlation_id_var.set(cid)
    return cid

def _extract_incoming_correlation_id(request: HttpRequest) -> str | None:
    value = request.META.get("HTTP_X_CORRELATION_ID")
    if value:
        value = value.strip()
        if value:
            return value
    return None


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = get_correlation_id()
        return True


class CorrelationIdMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        incoming_id = _extract_incoming_correlation_id(request)
        correlation_id = incoming_id or _correlation_id_var.get() or str(uuid4())
        token = _correlation_id_var.set(correlation_id)
        setattr(request, "correlation_id", correlation_id)

        try:
            response = self.get_response(request)
        except Exception:
            _correlation_id_var.reset(token)
            raise

        response[RESPONSE_HEADER_NAME] = correlation_id

        def _reset_correlation_id() -> None:
            _correlation_id_var.reset(token)

        response._resource_closers.append(_reset_correlation_id)  
        return response


REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['status_group']
)


class RequestMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        REQUEST_COUNT.labels(status_group='total').inc()

        status_code = response.status_code
        if 200 <= status_code < 300:
            group = '2xx'
        elif 400 <= status_code < 500:
            group = '4xx'
        elif 500 <= status_code < 600:
            group = '5xx'
        else:
            group = 'other'

        REQUEST_COUNT.labels(status_group=group).inc()

        return response

