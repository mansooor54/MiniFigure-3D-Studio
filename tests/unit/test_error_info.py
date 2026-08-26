from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models.error_info import (
    ErrorCategory,
    ErrorCause,
    ErrorInfo,
    SafeDetail,
)


def test_error_info_accepts_structured_safe_details() -> None:
    error = ErrorInfo(
        code="IMAGE_LOW_RESOLUTION",
        category=ErrorCategory.INPUT,
        user_message_key="error.image.low_resolution",
        technical_summary="The decoded image is below the selected mode threshold.",
        retryable=True,
        remediation_keys=("action.replace_image", "action.change_mode"),
        details=(SafeDetail(key="width_px", value=320),),
        causal_chain=(
            ErrorCause(code="IMAGE_DECODED", summary="The decoder returned valid pixels."),
        ),
    )
    assert error.code == "IMAGE_LOW_RESOLUTION"
    assert error.details[0].value == 320


def test_error_info_rejects_unstable_code() -> None:
    with pytest.raises(ValidationError, match="uppercase stable error code"):
        ErrorInfo(
            code="low-resolution",
            category=ErrorCategory.INPUT,
            user_message_key="error.image.low_resolution",
            technical_summary="Invalid code fixture.",
            retryable=False,
        )


def test_error_info_rejects_unlocalized_message_key() -> None:
    with pytest.raises(ValidationError, match="stable lowercase identifier"):
        ErrorInfo(
            code="IMAGE_LOW_RESOLUTION",
            category=ErrorCategory.INPUT,
            user_message_key="Visible user sentence",
            technical_summary="Invalid localization fixture.",
            retryable=False,
        )
