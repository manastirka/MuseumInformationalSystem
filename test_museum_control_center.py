import museum_control_center as control_center


def test_production_uses_local_cache_for_localhost_redis(tmp_path):
    env_file = tmp_path / '.env'
    env_file.write_text(
        'SESSION_TYPE=redis\n'
        'REDIS_URL=redis://localhost:6379/0\n',
        encoding='utf-8',
    )

    assert control_center.production_uses_local_cache(env_file) is True


def test_load_env_values_strips_inline_comments(tmp_path):
    env_file = tmp_path / '.env'
    env_file.write_text(
        'WTF_CSRF_TIME_LIMIT=3600  # 1 hour\n'
        'LOG_FORMAT=text  # Options: json, text\n'
        'QUOTED_VALUE=\"literal # keep this\"\n',
        encoding='utf-8',
    )

    env = control_center.load_env_values(env_file)

    assert env['WTF_CSRF_TIME_LIMIT'] == '3600'
    assert env['LOG_FORMAT'] == 'text'
    assert env['QUOTED_VALUE'] == 'literal # keep this'


def test_production_uses_local_cache_is_false_for_remote_redis(tmp_path):
    env_file = tmp_path / '.env'
    env_file.write_text(
        'SESSION_TYPE=redis\n'
        'REDIS_URL=redis://cache.internal:6379/0\n',
        encoding='utf-8',
    )

    assert control_center.production_uses_local_cache(env_file) is False


def test_build_services_config_adds_cache_and_excludes_dev_from_bulk(tmp_path, monkeypatch):
    env_file = tmp_path / '.env'
    env_file.write_text(
        'SESSION_TYPE=redis\n'
        'REDIS_URL=redis://localhost:6379/0\n',
        encoding='utf-8',
    )

    monkeypatch.setattr(control_center, 'systemd_unit_exists', lambda unit: unit == 'valkey')
    monkeypatch.setattr(control_center.shutil, 'which', lambda executable: '/usr/bin/valkey-server' if executable == 'valkey-server' else None)

    services = control_center.build_services_config(project_root=tmp_path, env_path=env_file)

    assert services['main_app_dev']['bulk_start'] is False
    assert services['cache']['systemd_service'] == 'valkey'

    controller = control_center.MuseumControlCenter.__new__(control_center.MuseumControlCenter)
    controller.services = services

    assert [service_id for service_id, _ in controller.get_bulk_services()] == [
        'postgresql',
        'cache',
        'museum_system',
        'nginx',
    ]


def test_build_qa_environment_loads_dotenv_and_overrides(tmp_path, monkeypatch):
    env_file = tmp_path / '.env'
    qa_env_file = tmp_path / '.env.qa'
    env_file.write_text(
        'CYPRESS_ADMIN_EMAIL=admin@example.com\n'
        'ADMIN_EMAIL=fallback-admin@example.com\n'
        'QA_SERVER_MODE=flask\n',
        encoding='utf-8',
    )
    qa_env_file.write_text(
        'CYPRESS_ADMIN_PASSWORD=secret\n'
        'CYPRESS_ARCHIVE_EMAIL=archive@example.com\n',
        encoding='utf-8',
    )

    monkeypatch.setattr(control_center, 'QA_ENV_FILE', qa_env_file)
    monkeypatch.setenv('CYPRESS_EMPLOYEE_EMAIL', 'employee@example.com')
    monkeypatch.setenv('CYPRESS_EMPLOYEE_PASSWORD', 'employee-secret')

    env = control_center.build_qa_environment(
        env_file,
        {
            'QA_SERVER_MODE': 'gunicorn',
            'QA_INCLUDE_K6': 1,
        },
    )

    assert env['CYPRESS_ADMIN_EMAIL'] == 'admin@example.com'
    assert env['CYPRESS_ADMIN_PASSWORD'] == 'secret'
    assert env['CYPRESS_EMPLOYEE_EMAIL'] == 'employee@example.com'
    assert env['CYPRESS_EMPLOYEE_PASSWORD'] == 'employee-secret'
    assert env['CYPRESS_ARCHIVE_EMAIL'] == 'archive@example.com'
    assert env['CYPRESS_ARCHIVE_PASSWORD'] == 'employee-secret'
    assert env['QA_SERVER_MODE'] == 'gunicorn'
    assert env['QA_INCLUDE_K6'] == '1'
    assert env['PYTHONUNBUFFERED'] == '1'


def test_get_missing_qa_env_vars_reports_only_missing_values():
    env = {
        'CYPRESS_ADMIN_EMAIL': 'admin@example.com',
        'CYPRESS_ADMIN_PASSWORD': 'secret',
    }

    missing = control_center.get_missing_qa_env_vars(env)

    assert 'CYPRESS_ADMIN_EMAIL' not in missing
    assert 'CYPRESS_ADMIN_PASSWORD' not in missing
    assert 'CYPRESS_EMPLOYEE_EMAIL' in missing
    assert 'CYPRESS_ARCHIVE_PASSWORD' not in missing


def test_qa_run_needs_browser_credentials_only_when_cypress_enabled():
    assert control_center.qa_run_needs_browser_credentials({'QA_INCLUDE_CYPRESS': '1'}) is True
    assert control_center.qa_run_needs_browser_credentials({'QA_INCLUDE_CYPRESS': '0'}) is False


def test_build_qa_email_defaults_prefers_env_then_db_then_directory():
    env = {
        'ADMIN_EMAIL': 'admin@nhmbeo.rs',
        'CYPRESS_ARCHIVE_EMAIL': '',
    }
    db_rows = [
        ('admin', 'admin-db@nhmbeo.rs'),
        ('employee', 'employee-db@nhmbeo.rs'),
    ]
    directory_entries = [
        {'role': 'admin', 'email': 'admin-directory@nhmbeo.rs'},
        {'role': 'employee', 'email': 'employee-directory@nhmbeo.rs'},
    ]

    defaults = control_center.build_qa_email_defaults(env, directory_entries=directory_entries, db_rows=db_rows)

    assert defaults['CYPRESS_ADMIN_EMAIL'] == 'admin@nhmbeo.rs'
    assert defaults['CYPRESS_EMPLOYEE_EMAIL'] == 'employee-db@nhmbeo.rs'
    assert defaults['CYPRESS_FIRST_LOGIN_EMAIL'] == 'employee-db@nhmbeo.rs'
    assert defaults['CYPRESS_RESET_TARGET_EMAIL'] == 'employee-db@nhmbeo.rs'
    assert defaults['CYPRESS_ARCHIVE_EMAIL'] == 'employee-db@nhmbeo.rs'


def test_build_qa_email_defaults_falls_back_to_directory_when_db_missing():
    env = {}
    directory_entries = [
        {'role': 'admin', 'email': 'admin'},
        {'role': 'employee', 'email': 'employee.one@nhmbeo.rs'},
        {'role': 'employee', 'email': 'employee.two@nhmbeo.rs'},
    ]

    defaults = control_center.build_qa_email_defaults(env, directory_entries=directory_entries, db_rows=[])

    assert 'CYPRESS_ADMIN_EMAIL' not in defaults
    assert defaults['CYPRESS_EMPLOYEE_EMAIL'] == 'employee.one@nhmbeo.rs'


def test_load_employee_directory_entries_reads_json_list(tmp_path):
    directory_file = tmp_path / 'employee_directory.json'
    directory_file.write_text(
        '[{"role": "employee", "email": "qa.employee@nhmbeo.rs"}]',
        encoding='utf-8',
    )

    entries = control_center.load_employee_directory_entries(directory_file)

    assert entries == [{'role': 'employee', 'email': 'qa.employee@nhmbeo.rs'}]
