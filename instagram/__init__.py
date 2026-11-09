"""AC-InstagramScraper package.
High-performance zero-auth Instagram scraper engine.
"""

from .axiom_adapter import (
    AXIOM_FIELDNAMES,
    format_comment_to_axiom,
    fetch_comments_axiom,
    write_axiom_csv,
)

__all__ = [
    "AXIOM_FIELDNAMES",
    "format_comment_to_axiom",
    "fetch_comments_axiom",
    "write_axiom_csv",
]
