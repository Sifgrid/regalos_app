import json
from pathlib import Path
from typing import List
from models import GiftItem, Contribution

DATA_DIR = Path("data")
GIFTS_FILE = DATA_DIR / "gifts.json"


def _ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not GIFTS_FILE.exists():
        GIFTS_FILE.write_text("[]", encoding="utf-8")


def load_gifts() -> List[GiftItem]:
    _ensure_data_file()
    raw = json.loads(GIFTS_FILE.read_text(encoding="utf-8"))
    gifts: List[GiftItem] = []

    for g in raw:
        contributions = [Contribution(**c) for c in g.get("contributions", [])]
        gifts.append(
            GiftItem(
                id=g["id"],
                name=g["name"],
                description=g.get("description", ""),
                url=g["url"],
                price=g["price"],
                contributions=contributions
            )
        )
    return gifts


def save_gifts(gifts: List[GiftItem]) -> None:
    _ensure_data_file()
    serializable = []

    for g in gifts:
        serializable.append({
            "id": g.id,
            "name": g.name,
            "url": g.url,
            "price": g.price,
            "description": g.description,
            "contributions": [c.__dict__ for c in g.contributions]
        })

    GIFTS_FILE.write_text(json.dumps(serializable, indent=2, ensure_ascii=False), encoding="utf-8")

