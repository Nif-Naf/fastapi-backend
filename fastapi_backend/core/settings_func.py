import json
import os
import sys
from logging import config

from dotenv import load_dotenv

main_dir = os.path.dirname(os.path.abspath(__file__))


def load_env_file() -> None:
    """Загрузка переменных."""
    path = os.path.join(main_dir, "envs/.env")
    env_conf = load_dotenv(dotenv_path=path)
    if not env_conf:
        raise Warning(f"File .env not found at path: {path}")


def load_test_env_file() -> None:
    """Загрузка тестовых переменных."""
    path = os.path.join(main_dir, "envs/.env.test")
    env_conf = load_dotenv(dotenv_path=path)
    if not env_conf:
        mess = f"File .env.test not found at path: {path}"
        raise Warning(mess)


def loads_envs_files() -> None:
    """Загрузка переменных."""
    if "pytest" in sys.argv[0]:
        load_test_env_file()
    else:
        load_env_file()


def load_logger_config() -> None:
    """Инициализация конфигурационного файла для логирования."""
    logger_conf = os.path.join(main_dir, "configs/logging_config.json")
    logs_directory = os.path.abspath(os.path.join(main_dir, '../../'))

    critical_log_file = os.path.join(logs_directory, "logs/critical.txt")
    auth_log_file = os.path.join(logs_directory, "logs/auth.txt")

    with open(logger_conf) as f:
        conf = json.load(f)
        conf["handlers"]["warn_handler"]["filename"] = critical_log_file
        conf["handlers"]["auth_handler"]["filename"] = auth_log_file
        config.dictConfig(conf)
