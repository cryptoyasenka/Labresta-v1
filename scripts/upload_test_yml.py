"""Upload the test YML file to shared hosting via FTP."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from app.services.ftp_upload import upload_to_ftp

FTP_HOST = os.environ.get("FTP_HOST", "")
FTP_USER = os.environ.get("FTP_USER", "")
FTP_PASS = os.environ.get("FTP_PASS", "")
FTP_REMOTE_PATH = os.environ.get("FTP_REMOTE_PATH", "")

missing = []
if not FTP_HOST:
    missing.append("FTP_HOST")
if not FTP_USER:
    missing.append("FTP_USER")
if not FTP_PASS:
    missing.append("FTP_PASS")
if not FTP_REMOTE_PATH:
    missing.append("FTP_REMOTE_PATH")

if missing:
    print("Ошибка: не заданы переменные окружения:", ", ".join(missing))
    print()
    print("Создайте файл .env на основе .env.example и заполните FTP-настройки:")
    print("  FTP_HOST=ftp.labresta.com")
    print("  FTP_USER=your-username")
    print("  FTP_PASS=your-password")
    print("  FTP_REMOTE_PATH=/public_html/feed.yml")
    sys.exit(1)

local_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "instance",
    "test_feed.yml",
)

if not os.path.isfile(local_path):
    print(f"Ошибка: файл {local_path} не найден.")
    print("Сначала запустите: uv run python scripts/generate_test_yml.py")
    sys.exit(1)

print(f"Загружаем {local_path} -> {FTP_HOST}:{FTP_REMOTE_PATH} ...")
result = upload_to_ftp(local_path, FTP_REMOTE_PATH, FTP_HOST, FTP_USER, FTP_PASS)

if result["success"]:
    # Derive public URL from remote path
    path_part = FTP_REMOTE_PATH
    for prefix in ("/public_html", "/www", "/htdocs"):
        if path_part.startswith(prefix):
            path_part = path_part[len(prefix):]
            break
    public_url = f"https://labresta.com{path_part}"

    print("Загрузка успешна!")
    print(f"Публичный URL: {public_url}")
    print()
    print("Следующие шаги:")
    print(f"  1. Откройте {public_url} в браузере — убедитесь, что YML отображается")
    print("  2. В prom.ua админке: Товары -> Импорт")
    print('  3. Режим: "Залишити без змін" для товаров не в файле')
    print('  4. Поля: только "Ціна" и "Наявність"')
    print("  5. Загрузите файл или укажите URL")
else:
    print(f"Ошибка загрузки: {result['error']}")
    sys.exit(1)
