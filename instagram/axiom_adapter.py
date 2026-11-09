"""Axiom Compatibility Adapter
===========================
Menyediakan adapter format dataset dan pipeline ekstraksi komentar Instagram
yang 100% kompatibel dengan standar skema AXIOM (RFC 4180 CSV & JSON).

Skema Kolom Standar AXIOM:
  - comment_id          : ID unik komentar (string)
  - created_at          : Waktu publikasi ISO 8601 UTC
  - author_username     : Username berformat @username
  - author_display_name : Nama tampilan (display name) akun
  - raw_text            : Teks komentar yang dinormalisasi (1 baris)
  - likes_count         : Jumlah likes pada komentar (int)
  - is_reply            : Boolean apakah merupakan balasan komentar
  - target_context      : Konteks postingan/kreator asli
"""

import csv
import time
import random
from pathlib import Path
from typing import Dict, Any, List, Optional

from . import refs
from .posts import get_comments, full_item, _resolved
from . import parsers as P


AXIOM_FIELDNAMES = [
    "comment_id",
    "created_at",
    "author_username",
    "author_display_name",
    "raw_text",
    "likes_count",
    "is_reply",
    "target_context"
]


def format_comment_to_axiom(comment_dict: Dict[str, Any], target_context: str = "") -> Dict[str, Any]:
    """Mengonversi dictionary komentar hasil parsing internal menjadi format standar AXIOM."""
    user = comment_dict.get("user") or {}
    raw_uname = user.get("username") or "anon"
    clean_uname = raw_uname if raw_uname.startswith("@") else f"@{raw_uname}"
    display_name = user.get("full_name") or raw_uname.replace("_", " ").title()

    raw_text = str(comment_dict.get("text") or "").replace("\r\n", " ").replace("\n", " ").strip()

    return {
        "comment_id": str(comment_dict.get("id") or ""),
        "created_at": comment_dict.get("created_at") or "",
        "author_username": clean_uname,
        "author_display_name": display_name,
        "raw_text": raw_text,
        "likes_count": int(comment_dict.get("like_count") or 0),
        "is_reply": bool(comment_dict.get("parent_comment_id")),
        "target_context": target_context,
    }


def fetch_comments_axiom(
    url_or_code: str,
    max_comments: int = 100,
    page_delay: float = 1.5,
) -> Dict[str, Any]:
    """
    Menyedot komentar asli dari Instagram (zero-auth/logged-out) dan
    memformatnya langsung ke skema AXIOM.
    
    Fitur:
    - Resolusi URL post / reels / shortcode
    - Paginasi otomatis menggunakan next_cursor
    - Pacing delay antar request
    - Output format standar AXIOM
    """
    resolved_post = refs.resolve_post(url_or_code)
    code = resolved_post["code"]

    # Ambil metadata postingan untuk target_context
    target_context = f"Instagram Post: {code}"
    post_meta: Dict[str, Any] = {"code": code}
    try:
        raw_full = full_item(resolved_post["id"], code)
        parsed_media = P.media(raw_full)
        if parsed_media:
            owner_u = parsed_media.get("owner", {}).get("username", "unknown")
            caption_snip = (parsed_media.get("caption") or "")[:80]
            target_context = f"IG Creator: @{owner_u} | Caption: {caption_snip}"
            post_meta = {
                "code": code,
                "owner_username": owner_u,
                "caption": parsed_media.get("caption", ""),
                "likes_count": parsed_media.get("like_count", 0),
                "comments_count": parsed_media.get("comment_count", 0),
                "published_at": parsed_media.get("published_at"),
            }
    except Exception:
        pass

    all_axiom_comments: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    has_more = True

    while has_more and len(all_axiom_comments) < max_comments:
        res = get_comments(resolved_post, cursor=cursor)
        batch = res.get("comments", [])
        if not batch:
            break

        for c in batch:
            formatted = format_comment_to_axiom(c, target_context=target_context)
            all_axiom_comments.append(formatted)
            if len(all_axiom_comments) >= max_comments:
                break

        cursor = res.get("next_cursor")
        has_more = bool(res.get("has_more") and cursor)

        if has_more and len(all_axiom_comments) < max_comments:
            pause = page_delay + random.uniform(0.5, 1.2)
            time.sleep(pause)

    return {
        "post_info": post_meta,
        "target_context": target_context,
        "total_extracted": len(all_axiom_comments),
        "comments": all_axiom_comments,
    }


def write_axiom_csv(filepath: str | Path, comments: List[Dict[str, Any]]) -> str:
    """Menulis list komentar AXIOM ke file CSV standar RFC 4180 (UTF-8-SIG)."""
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)

    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=AXIOM_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for c in comments:
            writer.writerow(c)

    return str(p)
