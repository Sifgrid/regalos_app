from typing import List, Optional
import uuid
from models import GiftItem, create_gift, create_contribution
import repository
import requests

def get_all_gifts() -> List[GiftItem]:
    return repository.load_gifts()


def add_gift(name, url, price, description):
    gifts = repository.load_gifts()

    new_gift = GiftItem(
    id=str(uuid.uuid4()),
    name=name,
    url=url,
    price=price,
    description=description,
    contributions=[]
    )



    gifts.append(new_gift)
    repository.save_gifts(gifts)

    return new_gift



def add_contribution(gift_id: str, amount: float, contributor_name: Optional[str], anonymous: bool):
    gifts = repository.load_gifts()
    gift = next((g for g in gifts if g.id == gift_id), None)

    if gift is None:
        raise ValueError("Regalo no encontrado")

    # Evitar pasar del precio total
    if amount > gift.remaining:
        amount = gift.remaining

    contribution = create_contribution(gift_id, amount, contributor_name, anonymous)
    gift.contributions.append(contribution)

    repository.save_gifts(gifts)
    return contribution


def yen_to_eur_with_tva(amount_jpy: float) -> float:
    """
    Convierte yenes (JPY) a euros (EUR) y aplica TVA del 20%.
    """
    try:
        url = "https://api.exchangerate.host/convert?from=JPY&to=EUR"
        response = requests.get(url, timeout=5).json()
        rate = response["info"]["rate"]
        eur = amount_jpy * rate
        return eur * 1.20  # aplicar TVA del 20%
    except Exception:
        # fallback si la API falla
        fallback_rate = 0.0060
        eur = amount_jpy * fallback_rate
        return eur * 1.20

