from flask import Flask

import observability


def test_observability_status_reports_missing_configuration():
    app = Flask(__name__)
    app.config.update(
        SENTRY_DSN=None,
        OTEL_ENABLED=False,
        OTEL_EXPORTER_OTLP_ENDPOINT=None,
        SENTRY_ENVIRONMENT='testing',
        SENTRY_TRACES_SAMPLE_RATE=0.0,
    )

    observability._SENTRY_INITIALIZED = False
    observability._OTEL_INITIALIZED = False
    observability._OBSERVABILITY_STATUS['sentry'] = {'enabled': False, 'reason': 'not_initialized'}
    observability._OBSERVABILITY_STATUS['opentelemetry'] = {'enabled': False, 'reason': 'not_initialized'}

    observability.init_observability(app)

    status = app.extensions['observability_status']
    assert status['sentry'] == {'enabled': False, 'reason': 'missing_dsn'}
    assert status['opentelemetry'] == {'enabled': False, 'reason': 'missing_configuration'}
