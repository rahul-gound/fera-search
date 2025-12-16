# SPDX-License-Identifier: AGPL-3.0-or-later
"""Hugging Face summarization plugin for Fera Search.

This plugin provides AI-powered text summarization using Hugging Face's Inference API.
"""

import os
import typing

from flask_babel import gettext

from searx.result_types import EngineResults
from searx.plugins import Plugin, PluginInfo

if typing.TYPE_CHECKING:
    from searx.search import SearchWithPlugins
    from searx.extended_types import SXNG_Request
    from searx.plugins import PluginCfg

# Constants for text length validation
MIN_TEXT_LENGTH = 50
MAX_TEXT_LENGTH = 10000

# Hugging Face API token
HF_TOKEN = "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"


class SXNGPlugin(Plugin):
    """Plugin that provides text summarization using Hugging Face's Inference API.

    The summarization is triggered by using the prefix "summarize:" in the search query.
    """

    id = "hf_summarizer"

    def __init__(self, plg_cfg: "PluginCfg") -> None:
        super().__init__(plg_cfg)

        self.info = PluginInfo(
            id=self.id,
            name=gettext("AI Summarizer"),
            description=gettext("Summarize text using Hugging Face AI (prefix query with 'summarize:')"),
            preference_section="general",
        )

        # Use the configured HF token
        self.hf_token = HF_TOKEN
        self.model = "sshleifer/distilbart-cnn-12-6"

    def _summarize_text(self, text: str) -> str | None:
        """Summarize text using Hugging Face Inference API."""
        if not self.hf_token:
            self.log.warning("HF_TOKEN not configured")
            return None

        try:
            from huggingface_hub import InferenceClient

            client = InferenceClient(
                api_key=self.hf_token,
            )

            result = client.summarization(
                text,
                model=self.model,
            )

            if isinstance(result, dict) and "summary_text" in result:
                return result["summary_text"]
            elif isinstance(result, str):
                return result
            else:
                return str(result)

        except ImportError:
            self.log.error("huggingface_hub package not installed")
            return None
        except Exception as e:
            self.log.error("Error during summarization: %s", str(e))
            return None

    def post_search(self, request: "SXNG_Request", search: "SearchWithPlugins") -> EngineResults:
        results = EngineResults()

        # Only process on the first page
        if search.search_query.pageno > 1:
            return results

        query = search.search_query.query.strip()

        # Check if query starts with "summarize:"
        if not query.lower().startswith("summarize:"):
            return results

        # Extract the text to summarize
        text_to_summarize = query[10:].strip()  # Remove "summarize:" prefix

        if len(text_to_summarize) < MIN_TEXT_LENGTH:
            results.add(
                results.types.Answer(
                    answer=gettext("Please provide more text to summarize (at least %(min)d characters).")
                    % {"min": MIN_TEXT_LENGTH}
                )
            )
            return results

        # Limit text length to avoid API issues
        if len(text_to_summarize) > MAX_TEXT_LENGTH:
            text_to_summarize = text_to_summarize[:MAX_TEXT_LENGTH]

        summary = self._summarize_text(text_to_summarize)

        if summary:
            results.add(
                results.types.Answer(
                    answer=f"📝 **Summary:**\n\n{summary}"
                )
            )
        else:
            results.add(
                results.types.Answer(
                    answer=gettext("Unable to generate summary. Please try again later.")
                )
            )

        return results
