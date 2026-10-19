import json

from app.config import load_settings


def _write_settings_json(directory, data):
    (directory / "config").mkdir()
    (directory / "config" / "settings.json").write_text(json.dumps(data))


def test_settings_json_overrides_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DB_TYPE", raising=False)
    _write_settings_json(tmp_path, {"app_name": "Mi App", "db_type": "sqlite"})

    settings = load_settings()

    assert settings.app_name == "Mi App"
    assert settings.db_type == "sqlite"


def test_environment_variable_wins_over_settings_json(tmp_path, monkeypatch):
    """Docker fuerza DB_TYPE=postgresql aunque settings.json diga sqlite."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DB_TYPE", "postgresql")
    _write_settings_json(tmp_path, {"db_type": "sqlite", "app_name": "Mi App"})

    settings = load_settings()

    assert settings.db_type == "postgresql"
    # El resto de claves del JSON siguen aplicándose
    assert settings.app_name == "Mi App"


def test_missing_settings_json_uses_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DB_TYPE", raising=False)

    settings = load_settings()

    assert settings.db_type == "sqlite"
