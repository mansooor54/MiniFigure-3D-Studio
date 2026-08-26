from __future__ import annotations

import json
from pathlib import Path

from app.logging.redaction_policy import RedactionLimits, RedactionPolicy


def test_seeded_secrets_and_sensitive_payloads_are_removed() -> None:
    secret = "sk-" + "x" * 24
    policy = RedactionPolicy()
    redacted = policy.redact_fields(
        {
            "authorization": f"Bearer {secret}",
            "nested": {
                "api_key": secret,
                "cookie": "session=private",
                "source_image": b"person-image-bytes",
            },
            "environment": {"MINIFIGURE_EXTERNAL_API_KEY": secret},
            "safe_metric": 42,
        }
    )
    encoded = json.dumps(redacted, ensure_ascii=False)
    assert secret not in encoded
    assert "person-image-bytes" not in encoded
    assert "MINIFIGURE_EXTERNAL_API_KEY" not in encoded
    assert redacted["safe_metric"] == 42


def test_tokens_and_absolute_paths_are_redacted_from_text() -> None:
    policy = RedactionPolicy()
    access_id = "AKIA" + "ABCDEFGHIJKLMNOP"
    text = (
        "Bearer token-value /Users/person/private/photo.jpg "
        f"C:\\Users\\person\\photo.jpg {access_id}"
    )
    redacted = policy.redact_text(text)
    assert "token-value" not in redacted
    assert "/Users/person" not in redacted
    assert "C:\\Users" not in redacted
    assert access_id not in redacted


def test_secret_url_query_and_userinfo_are_removed() -> None:
    policy = RedactionPolicy()
    redacted = policy.redact_text(
        "https://user:password@example.invalid/upload?token=secret-value&mode=fast"
    )
    assert "user:password" not in redacted
    assert "secret-value" not in redacted
    assert "mode=fast" in redacted


def test_absolute_path_objects_and_relative_paths_are_distinguished() -> None:
    policy = RedactionPolicy()
    redacted = policy.redact_fields(
        {
            "path": Path("runs/one/result.json"),
            "source_path": Path("/private/project/photo.jpg"),
        }
    )
    assert redacted["path"] == "runs/one/result.json"
    assert redacted["source_path"] == "[ABSOLUTE_PATH_REDACTED]"


def test_limits_prevent_oversized_or_deep_log_values() -> None:
    policy = RedactionPolicy(
        RedactionLimits(maximum_depth=2, maximum_items=2, maximum_string_length=8)
    )
    redacted = policy.redact_fields(
        {
            "long": "123456789",
            "nested": {"level1": {"level2": {"value": "safe"}}},
            "ignored": "third item",
        }
    )
    assert redacted["long"] == "[OVERSIZED_VALUE_REDACTED]"
    assert "ignored" not in redacted
    assert "[DEPTH_LIMIT]" in json.dumps(redacted)
