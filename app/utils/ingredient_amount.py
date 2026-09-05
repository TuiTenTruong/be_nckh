"""Helpers for recipe ingredient quantity + unit (data_book.json format)."""


def format_ingredient_amount(quantity: str | None, unit: str | None) -> str:
    q = (quantity or "").strip()
    u = (unit or "").strip()
    if q and u:
        return f"{q} {u}"
    return q or u or ""


def parse_legacy_amount(amount: str | None) -> tuple[str | None, str | None]:
    """Best-effort split legacy combined amount into quantity + unit."""
    text = (amount or "").strip()
    if not text:
        return None, None
    parts = text.split(None, 1)
    if len(parts) == 1:
        return parts[0], None
    return parts[0], parts[1]
