"""Generate a test YML file with 3 products from the local prom.ua catalog."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.catalog import PromProduct
from app.services.yml_test_generator import generate_test_yml

app = create_app()

with app.app_context():
    db.create_all()

    products = PromProduct.query.limit(3).all()

    if len(products) < 3:
        print(
            f"Ошибка: в базе только {len(products)} товаров. "
            "Сначала импортируйте каталог prom.ua (нужно минимум 3 товара)."
        )
        sys.exit(1)

    ext_ids = [p.external_id for p in products]
    output = os.path.join(app.instance_path, "test_feed.yml")
    path = generate_test_yml(ext_ids, output)

    print("Тестовый YML создан:", path)
    print()
    print("Использованные товары:")
    for p in products:
        price_display = f"{p.price / 100:.2f}" if p.price else "0.00"
        print(f"  ID: {p.external_id} | {p.name} | {price_display} {p.currency}")

    print()
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())
