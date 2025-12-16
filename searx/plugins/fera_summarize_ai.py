# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fera-SummarizeAI plugin for Fera Search.

This plugin provides AI-powered text summarization using Cohere's API.
"""

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

# Cohere API key
COHERE_API_KEY = "5gP0DYhtKdWGVQ4aUV2R8P89ZaibNqwf5bM01plD"


class SXNGPlugin(Plugin):
    """Fera-SummarizeAI: AI-powered text summarization using Cohere API.

    The summarization is triggered by using the prefix "summarize:" in the search query.
    """

    id = "fera_summarize_ai"

    def __init__(self, plg_cfg: "PluginCfg") -> None:
        super().__init__(plg_cfg)

        self.info = PluginInfo(
            id=self.id,
            name=gettext("Fera-SummarizeAI"),
            description=gettext("AI-powered summarization by Fera-SummarizeAI (prefix query with 'summarize:')"),
            preference_section="general",
        )

        self.api_key = COHERE_API_KEY

    def _summarize_text(self, text: str) -> str | None:
        """Summarize text using Cohere API."""
        if not self.api_key:
            self.log.warning("Cohere API key not configured")
            return None

        try:
            import cohere

            client = cohere.Client(self.api_key)

            response = client.summarize(
                text=text,
                length="medium",
                format="paragraph",
                model="command",
                extractiveness="medium",
            )

            if hasattr(response, 'summary'):
                return response.summary
            else:
                return str(response)

        except ImportError:
            self.log.error("cohere package not installed")
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
                    answer=gettext("Fera-SummarizeAI: Please provide more text to summarize (at least %(min)d characters).")
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
                    answer=f"Fera-SummarizeAI:\n\n{summary}"
                )
            )
        else:
            results.add(
                results.types.Answer(
                    answer=gettext("Fera-SummarizeAI: Unable to generate summary. Please try again later.")
                )
            )

        return results
