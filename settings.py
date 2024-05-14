import os

# Текущая директория проекта
BASE_DIR = os.path.dirname(__file__)


# Секретный ключ проекта
SECRET_KEY = os.getenv('SECRET_KEY', 'erngiergoierhngiowerjhifherugnrieogjeriouj')

# Ссылка на подключение к БД
DATABASE_URL = 'mysql://root:1234@localhost:3306/centek'

# Режим отладки
DEBUG = bool(os.getenv('DEBUG', True))

# Хост
HOST = os.getenv('HOST', '0.0.0.0')

# Порт
PORT = int(os.getenv('PORT', 8080))

# Директория media-файлов
MEDIA_DIR = os.path.join(BASE_DIR, 'media')


# Директория static-файлов
STATIC_DIR = os.path.join(BASE_DIR, 'static')


# Директория для хранения фото профилей пользователей
AVATAR_DIR = os.path.join(MEDIA_DIR, 'avatar')

# Путь к static-файлам
STATIC_URL = 'static'


# Путь к media-файлам
MEDIA_URL = 'media'


def get_relpath(path: os.PathLike | str):
    return os.path.relpath(path, BASE_DIR)


def get_avatar_save_path(file_name: str):
    save_path = os.path.join(AVATAR_DIR, file_name)

    return (
        save_path,
        get_relpath(save_path)
    )


def get_static_file_path(*file_paths: os.PathLike | str):
    path = os.path.join(STATIC_DIR, *file_paths)
    dir_name = os.path.dirname(path)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return path


def get_media_file_path(*file_paths: os.PathLike | str):
    path = os.path.join(MEDIA_DIR, *file_paths)
    dir_name = os.path.dirname(path)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return path


def path_exists(path: os.PathLike | str):
    return os.path.exists(path)


def is_dir(path: os.PathLike | str):
    return os.path.isdir(path)
