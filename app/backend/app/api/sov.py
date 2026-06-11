from __future__ import annotations

from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User
from ..schemas import SovCheckRequest

router = APIRouter(prefix="/sov", tags=["sov"])


@router.post("/check")
def sov_check(
    payload: SovCheckRequest,
    current_user: User = Depends(get_current_user),
) -> dict:
    providers = payload.providers or ["chatgpt", "perplexity", "gemini"]
    mentions = [
        {
            "query": query,
            "provider": provider,
            "brand": payload.brand,
            "mentioned": None,
            "share_estimate": None,
            "notes": "Experimental starter scaffold. Populate from manual or future automated checks.",
        }
        for query in payload.queries
        for provider in providers
    ]
    return {
        "brand": payload.brand,
        "market": payload.market,
        "language": payload.language,
        "providers": providers,
        "mentions": mentions,
        "disclaimer": (
            "This is an experimental API starter for transparent AI Share of Voice tracking. "
            "It does not claim live provider ranking truth yet."
        ),
        "requested_by_user_id": current_user.id,
    }
