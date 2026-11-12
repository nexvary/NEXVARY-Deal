from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="NEXVARY Deal API", version="0.1.0")

Category = Literal["shopping", "domains", "hosting", "ai", "cloud", "software"]

class Offer(BaseModel):
    id: str
    provider: str
    title: str
    category: Category
    url: str
    verification: Literal["official", "tested", "community", "unverified"]
    coupon_code: str | None = None
    country: str | None = None

# No synthetic or unverified offers are returned as real results.
OFFERS: list[Offer] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/offers", response_model=list[Offer])
def search_offers(q: str = Query(default="", max_length=120), category: Category | None = None):
    term = q.casefold().strip()
    return [o for o in OFFERS if (not term or term in (o.provider + " " + o.title).casefold()) and (category is None or o.category == category)]
