"""Optional runtime observability bootstrap for production diagnostics."""

from __future__ import annotations

import logging
from typing import Any

_SENTRY_INITIALIZED = False
_OTEL_INITIALIZED = False
_OBSERVABILITY_STATUS = {
    'sentry': {'enabled': False, 'reason': 'not_initialized'},
    'opentelemetry': {'enabled': False, 'reason': 'not_initialized'},
}


def _get_sentry_sdk():
    try:
        import sentry_sdk
        return sentry_sdk
    except ImportError:
        return None


def _sanitize_event_data(data: Any) -> Any:
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            lowered = str(key).lower()
            if any(token in lowered for token in ('password', 'secret', 'token', 'authorization', 'cookie')):
                sanitized[key] = '[Filtered]'
            else:
                sanitized[key] = _sanitize_event_data(value)
        return sanitized
    if isinstance(data, list):
        return [_sanitize_event_data(item) for item in data]
    return data


def init_sentry(app) -> None:
    """Initialize Sentry when configured and dependency is available."""
    global _SENTRY_INITIALIZED
    if _SENTRY_INITIALIZED:
        _OBSERVABILITY_STATUS['sentry'] = {'enabled': True, 'reason': 'already_initialized'}
        return

    dsn = app.config.get('SENTRY_DSN')
    if not dsn:
        _OBSERVABILITY_STATUS['sentry'] = {'enabled': False, 'reason': 'missing_dsn'}
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
    except ImportError:
        _OBSERVABILITY_STATUS['sentry'] = {'enabled': False, 'reason': 'missing_dependency'}
        app.logger.warning('Sentry DSN configured but sentry-sdk is not installed')
        return

    def before_send(event, _hint):
        return _sanitize_event_data(event)

    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        environment=app.config.get('SENTRY_ENVIRONMENT', 'production'),
        traces_sample_rate=float(app.config.get('SENTRY_TRACES_SAMPLE_RATE', 0.1)),
        send_default_pii=bool(app.config.get('SENTRY_SEND_DEFAULT_PII', False)),
        before_send=before_send,
    )
    _SENTRY_INITIALIZED = True
    _OBSERVABILITY_STATUS['sentry'] = {'enabled': True, 'reason': 'initialized'}
    app.logger.info('Sentry observability enabled')


def add_sentry_breadcrumb(*, category: str, message: str, level: str = 'info', data: dict[str, Any] | None = None) -> None:
    """Add a Sentry breadcrumb when the SDK is available."""
    sentry_sdk = _get_sentry_sdk()
    if not sentry_sdk:
        return

    try:
        sentry_sdk.add_breadcrumb(
            category=category,
            message=message,
            level=level,
            data=_sanitize_event_data(data or {}),
        )
    except Exception:
        return


def set_sentry_user_context(user: dict[str, Any] | None) -> None:
    """Attach the current user to Sentry scope when the SDK is available."""
    sentry_sdk = _get_sentry_sdk()
    if not sentry_sdk:
        return

    try:
        sentry_sdk.set_user(_sanitize_event_data(user or {}))
    except Exception:
        return


def capture_observability_exception(
    exc: Exception,
    *,
    tags: dict[str, Any] | None = None,
    extra: dict[str, Any] | None = None,
    user: dict[str, Any] | None = None,
) -> None:
    """Capture an exception with optional tags, extra context, and user scope."""
    sentry_sdk = _get_sentry_sdk()
    if not sentry_sdk:
        return

    try:
        scope_factory = getattr(sentry_sdk, 'new_scope', None) or sentry_sdk.push_scope
        with scope_factory() as scope:
            if user:
                sanitized_user = _sanitize_event_data(user or {})
                scope_set_user = getattr(scope, 'set_user', None)
                if callable(scope_set_user):
                    scope_set_user(sanitized_user)
                else:
                    set_sentry_user_context(sanitized_user)
            for key, value in (tags or {}).items():
                scope.set_tag(str(key), str(value))
            for key, value in _sanitize_event_data(extra or {}).items():
                scope.set_extra(str(key), value)
            sentry_sdk.capture_exception(exc)
    except Exception:
        return


def init_opentelemetry(app) -> None:
    """Initialize OpenTelemetry tracing when configured and dependency is available."""
    global _OTEL_INITIALIZED
    if _OTEL_INITIALIZED:
        _OBSERVABILITY_STATUS['opentelemetry'] = {'enabled': True, 'reason': 'already_initialized'}
        return

    enabled = bool(app.config.get('OTEL_ENABLED', False))
    endpoint = app.config.get('OTEL_EXPORTER_OTLP_ENDPOINT')
    if not enabled and not endpoint:
        _OBSERVABILITY_STATUS['opentelemetry'] = {'enabled': False, 'reason': 'missing_configuration'}
        return

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        _OBSERVABILITY_STATUS['opentelemetry'] = {'enabled': False, 'reason': 'missing_dependency'}
        app.logger.warning('OpenTelemetry configured but packages are not installed')
        return

    try:
        resource = Resource.create({
            SERVICE_NAME: app.config.get('OTEL_SERVICE_NAME', 'museum-info-system'),
            'deployment.environment': app.config.get('SENTRY_ENVIRONMENT', 'production'),
        })
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
        trace.set_tracer_provider(provider)
        FlaskInstrumentor().instrument_app(app)
        RequestsInstrumentor().instrument()
    except Exception as exc:  # noqa: BLE001 - observability must not break app boot
        _OBSERVABILITY_STATUS['opentelemetry'] = {'enabled': False, 'reason': f'init_failed:{type(exc).__name__}'}
        logging.getLogger(__name__).warning('OpenTelemetry initialization failed: %s', exc)
        return

    _OTEL_INITIALIZED = True
    _OBSERVABILITY_STATUS['opentelemetry'] = {'enabled': True, 'reason': 'initialized'}
    app.logger.info('OpenTelemetry tracing enabled')


def get_observability_status() -> dict[str, dict[str, Any]]:
    """Return the last-known bootstrap status for observability integrations."""
    return {
        'sentry': dict(_OBSERVABILITY_STATUS['sentry']),
        'opentelemetry': dict(_OBSERVABILITY_STATUS['opentelemetry']),
    }


def init_observability(app) -> None:
    """Bootstrap optional observability integrations."""
    init_sentry(app)
    init_opentelemetry(app)
    status = get_observability_status()
    app.extensions['observability_status'] = status
    app.logger.info(
        'Observability status: sentry=%s(%s), opentelemetry=%s(%s)',
        'enabled' if status['sentry']['enabled'] else 'disabled',
        status['sentry']['reason'],
        'enabled' if status['opentelemetry']['enabled'] else 'disabled',
        status['opentelemetry']['reason'],
    )
