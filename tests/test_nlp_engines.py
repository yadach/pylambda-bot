#!/usr/bin/env python3

import logging

import pytest

from pylambda_bot import nlp_engines

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "nlp_engine, text, nlp_params",
    [
        ("Echo", "こんにちは", {"num_repeat": 3}),
        ("OpenAI", "あなたのお名前は？", {"model": "gpt-3.5-turbo", "max_tokens": 32}),
    ],
)
def test_nlp_engines(nlp_engine: str, text: str, nlp_params: dict):
    """Test message services."""

    nlp_model = getattr(nlp_engines, nlp_engine)(params=nlp_params)
    res_text = nlp_model.get_reply(text)

    logger.info(res_text)
    assert type(res_text) == str
