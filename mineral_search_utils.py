"""Helpers for parsing mineral search input."""

from typing import Dict, List, Optional


def split_search_terms(query: str) -> List[str]:
    """Split a search string into comma-separated terms."""
    query = (query or "").strip()
    if not query:
        return []

    terms = [term.strip() for term in query.split(",") if term.strip()]
    return terms or [query]


def build_search_specs(query: str) -> List[Dict[str, Optional[str]]]:
    """Build normalized search specs for SQL backends."""
    terms = split_search_terms(query)
    multi_term_search = len(terms) > 1
    specs: List[Dict[str, Optional[str]]] = []

    for term in terms:
        upper_term = term.upper()
        inv_num = None
        inv_prefix = None
        is_inventory_term = False

        if upper_term.startswith("M") and term[1:].isdigit():
            inv_num = term[1:]
            is_inventory_term = True
        elif term.isdigit():
            inv_num = term
            is_inventory_term = True
        elif upper_term.startswith("BEZ"):
            inv_prefix = f"{upper_term}%"
            is_inventory_term = True

        specs.append({
            "term": term,
            "pattern": f"%{term}%",
            "starts_with": f"{term}%",
            "inv_num": inv_num,
            "inv_prefix": inv_prefix,
            "inventory_only": multi_term_search and is_inventory_term,
        })

    return specs
