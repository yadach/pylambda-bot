#!/usr/bin/env python3

import logging
import os

import pytest

from pylambda_bot import message_services

logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="For local debugging only.")
@pytest.mark.parametrize(
    "msg_svc, text, msg_svc_params",
    [
        ("Slack", "Post test from CI.", {}),
    ],
)
def test_nlp_engines(msg_svc: str, text: str, msg_svc_params: dict):
    """Test NLP engines."""

    msg_svc = getattr(message_services, msg_svc)(**msg_svc_params)
    msg_svc.channel = os.environ.get("SlackChannel")
    res = msg_svc.post(text, in_thread=False)

    is_ok = res.json()["ok"]
    logger.info(f"Response ok: {is_ok}")
    assert type(is_ok)
