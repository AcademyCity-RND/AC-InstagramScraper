"""Unit tests for the Axiom Adapter.
Validates RFC 4180 CSV formatting, schema alignment, and comment normalisation.
"""

import csv
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from instagram.axiom_adapter import (
    AXIOM_FIELDNAMES,
    format_comment_to_axiom,
    write_axiom_csv,
)


def test_axiom_fieldnames_consistency():
    """Verify that AXIOM_FIELDNAMES exactly matches the required Axiom schema."""
    expected = [
        "comment_id",
        "created_at",
        "author_username",
        "author_display_name",
        "raw_text",
        "likes_count",
        "is_reply",
        "target_context"
    ]
    assert AXIOM_FIELDNAMES == expected


def test_format_comment_to_axiom():
    """Verify that a raw comment is correctly transformed into Axiom format."""
    raw_comment = {
        "id": "18029384729102",
        "text": "Kawal terus aspirasi rakyat secara damai! #KawalAspirasi\nJangan terprovokasi.",
        "created_at": "2026-11-08T14:30:00+00:00",
        "like_count": 42,
        "reply_count": 3,
        "user": {
            "id": "99887766",
            "username": "budi_santoso",
            "full_name": "Budi Santoso",
            "is_verified": False
        },
        "parent_comment_id": None,
        "is_by_owner": False
    }

    target_context = "IG Creator: @kompascom | Caption: Demo Mahasiswa"
    formatted = format_comment_to_axiom(raw_comment, target_context=target_context)

    assert formatted["comment_id"] == "18029384729102"
    assert formatted["created_at"] == "2026-11-08T14:30:00+00:00"
    assert formatted["author_username"] == "@budi_santoso"
    assert formatted["author_display_name"] == "Budi Santoso"
    assert "\n" not in formatted["raw_text"]
    assert formatted["raw_text"] == "Kawal terus aspirasi rakyat secara damai! #KawalAspirasi Jangan terprovokasi."
    assert formatted["likes_count"] == 42
    assert formatted["is_reply"] is False
    assert formatted["target_context"] == target_context


def test_format_reply_comment():
    """Verify reply detection and anonymous user fallback."""
    raw_reply = {
        "id": "18029384729999",
        "text": "Setuju banget kawan",
        "created_at": "2026-11-08T14:35:00+00:00",
        "like_count": 5,
        "user": {
            "username": "ahmad_dani",
            "full_name": None
        },
        "parent_comment_id": "18029384729102"
    }

    formatted = format_comment_to_axiom(raw_reply)
    assert formatted["is_reply"] is True
    assert formatted["author_username"] == "@ahmad_dani"
    assert formatted["author_display_name"] == "Ahmad Dani"


def test_write_axiom_csv(tmp_path):
    """Verify writing to RFC 4180 CSV with UTF-8-SIG encoding."""
    comments = [
        {
            "comment_id": "c_001",
            "created_at": "2026-11-08T10:00:00+00:00",
            "author_username": "@user_one",
            "author_display_name": "User One",
            "raw_text": "Komentar pertama dengan koma, dan kutip \"oke\"",
            "likes_count": 10,
            "is_reply": False,
            "target_context": "Target Context 1"
        },
        {
            "comment_id": "c_002",
            "created_at": "2026-11-08T10:05:00+00:00",
            "author_username": "@user_two",
            "author_display_name": "User Two",
            "raw_text": "Komentar kedua",
            "likes_count": 0,
            "is_reply": True,
            "target_context": "Target Context 2"
        }
    ]

    out_file = tmp_path / "test_axiom_output.csv"
    res_path = write_axiom_csv(out_file, comments)

    assert os.path.exists(res_path)

    # Read back and verify CSV
    with open(out_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == AXIOM_FIELDNAMES
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["comment_id"] == "c_001"
        assert rows[0]["author_username"] == "@user_one"
        assert rows[0]["raw_text"] == "Komentar pertama dengan koma, dan kutip \"oke\""
        assert rows[1]["is_reply"] == "True"
