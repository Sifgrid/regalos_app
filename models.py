from dataclasses import dataclass, field
from typing import List, Optional
import uuid
from datetime import datetime


@dataclass
class Contribution:
    id: str
    gift_id: str
    amount: float
    contributor_name: Optional[str]
    anonymous: bool
    created_at: str


@dataclass
class GiftItem:
    id: str
    name: str
    url: str
    price: float
    description: str
    contributions: List[Contribution]

    @property
    def total_contributed(self) -> float:
        return sum(c.amount for c in self.contributions)

    @property
    def remaining(self) -> float:
        return max(self.price - self.total_contributed, 0.0)


def create_gift(name: str, url: str, price: float) -> GiftItem:
    return GiftItem(
        id=str(uuid.uuid4()),
        name=name,
        url=url,
        price=price,
        contributions=[]
    )


def create_contribution(gift_id: str, amount: float, contributor_name: Optional[str], anonymous: bool) -> Contribution:
    return Contribution(
        id=str(uuid.uuid4()),
        gift_id=gift_id,
        amount=amount,
        contributor_name=contributor_name if not anonymous else None,
        anonymous=anonymous,
        created_at=datetime.utcnow().isoformat()
    )
