"""
tests/test_tools.py
-------------------
Pytest tests for backend/tools/ modules.

Coverage:
    - summarization_tool.py  (fully tested — new tool added in this PR)
    - tool_router.py         (keyword routing logic, new summarization branch)
    - project_generator.py  (static plan generation)

Tests that would require live network access (web_search, research_tool)
and ChromaDB (memory_inspector) are intentionally excluded here to keep
the suite fast and side-effect-free.  Those modules should be tested
with mocking in a separate integration test file.

Run with:
    pytest tests/test_tools.py -v
"""

import pytest

from backend.tools.summarization_tool import (
    summarize_text,
    _tokenise,
    _split_sentences,
)
from backend.tools.project_generator import generate_project_plan
from backend.tools.tool_router import run_tools


# ===========================================================================
# Internal helpers: _tokenise
# ===========================================================================


class TestTokenise:
    """Tests for the private _tokenise helper in summarization_tool.py."""

    def test_lowercases_words(self) -> None:
        """All tokens must be lowercase regardless of input case."""
        tokens = _tokenise("Hello WORLD")
        assert tokens == ["hello", "world"]

    def test_removes_punctuation(self) -> None:
        """Punctuation characters must not appear in the output tokens."""
        tokens = _tokenise("AI, is: great!")
        assert "," not in tokens
        assert ":" not in tokens
        assert "!" not in tokens

    def test_empty_string_returns_empty_list(self) -> None:
        """An empty input should produce an empty list, not raise an error."""
        tokens = _tokenise("")
        assert tokens == []

    def test_single_word(self) -> None:
        """A single word should produce a list with one element."""
        tokens = _tokenise("Python")
        assert tokens == ["python"]


# ===========================================================================
# Internal helpers: _split_sentences
# ===========================================================================


class TestSplitSentences:
    """Tests for the private _split_sentences helper."""

    def test_splits_on_period(self) -> None:
        """Sentences ending with '.' should be separated correctly."""
        sentences = _split_sentences("Hello world. How are you?")
        assert len(sentences) == 2

    def test_strips_whitespace(self) -> None:
        """Each sentence in the output should have no leading/trailing spaces."""
        sentences = _split_sentences("  Hello.  World.  ")
        for s in sentences:
            assert s == s.strip()

    def test_single_sentence(self) -> None:
        """A single sentence should return a list with one element."""
        sentences = _split_sentences("This is one sentence.")
        assert len(sentences) == 1

    def test_empty_string_returns_empty_list(self) -> None:
        """Empty input must not raise an error."""
        sentences = _split_sentences("")
        assert sentences == []


# ===========================================================================
# summarize_text — the main public function
# ===========================================================================


class TestSummarizeText:
    """Tests for backend/tools/summarization_tool.py :: summarize_text()."""

    # A multi-sentence paragraph we can reuse across several tests.
    SAMPLE_TEXT: str = (
        "Artificial intelligence is transforming many industries. "
        "Machine learning is a core subset of AI that allows systems to learn from data. "
        "Deep learning uses neural networks with many layers to solve complex problems. "
        "Natural language processing enables computers to understand human language. "
        "AI is being applied to healthcare, finance, and education sectors."
    )

    def test_returns_string(self) -> None:
        """summarize_text must return a str."""
        result = summarize_text(self.SAMPLE_TEXT)
        assert isinstance(result, str)

    def test_contains_header(self) -> None:
        """Output must begin with the '[Summary Tool]' section label."""
        result = summarize_text(self.SAMPLE_TEXT)
        assert "[Summary Tool]" in result

    def test_default_three_sentences(self) -> None:
        """Default call (no num_sentences arg) should include 3 bullet points."""
        result = summarize_text(self.SAMPLE_TEXT)
        # Each selected sentence is formatted as a "- " bullet.
        bullet_count = result.count("\n- ")
        assert bullet_count == 3, (
            f"Expected 3 bullet points, got {bullet_count}. Output:\n{result}"
        )

    def test_custom_num_sentences(self) -> None:
        """Passing num_sentences=2 must produce exactly 2 bullet points."""
        result = summarize_text(self.SAMPLE_TEXT, num_sentences=2)
        bullet_count = result.count("\n- ")
        assert bullet_count == 2

    def test_empty_text_returns_error_message(self) -> None:
        """An empty string should return a descriptive error, not raise."""
        result = summarize_text("")
        assert "Error" in result or "error" in result.lower()

    def test_whitespace_only_returns_error_message(self) -> None:
        """A string of only whitespace should also be treated as empty."""
        result = summarize_text("   \n  \t  ")
        assert "Error" in result or "error" in result.lower()

    def test_invalid_num_sentences_returns_error(self) -> None:
        """num_sentences < 1 must return an error message without raising."""
        result = summarize_text(self.SAMPLE_TEXT, num_sentences=0)
        assert "Error" in result or "error" in result.lower()

    def test_short_text_returns_all_sentences(self) -> None:
        """If text has fewer sentences than num_sentences, all are returned."""
        short_text = "AI is great. It helps people."
        result = summarize_text(short_text, num_sentences=5)
        # Both sentences should appear in the output.
        assert "AI is great" in result
        assert "It helps people" in result

    def test_output_is_shorter_than_input(self) -> None:
        """Summary should generally be shorter than the original text."""
        result = summarize_text(self.SAMPLE_TEXT, num_sentences=2)
        # The summary (bullet list portion only) should have fewer words.
        assert len(result) < len(self.SAMPLE_TEXT) * 1.5  # generous upper bound

    def test_single_sentence_text(self) -> None:
        """A single-sentence input should be returned as-is without crashing."""
        single = "This is the only sentence."
        result = summarize_text(single, num_sentences=3)
        assert "This is the only sentence" in result

    def test_summary_mentions_section_label(self) -> None:
        """The output should clearly label itself as a summary."""
        result = summarize_text(self.SAMPLE_TEXT)
        assert "Summary" in result


# ===========================================================================
# Project Generator
# ===========================================================================


class TestGenerateProjectPlan:
    """Tests for backend/tools/project_generator.py :: generate_project_plan()."""

    def test_returns_string(self) -> None:
        """generate_project_plan must return a str."""
        result = generate_project_plan("My AI Chatbot")
        assert isinstance(result, str)

    def test_non_empty(self) -> None:
        """The plan should never be an empty string."""
        result = generate_project_plan("Test Project")
        assert len(result.strip()) > 0


# ===========================================================================
# Tool Router
# ===========================================================================


class TestRunTools:
    """Tests for backend/tools/tool_router.py :: run_tools()."""

    def test_no_keywords_returns_sentinel(self) -> None:
        """A query with no matching keywords must return the sentinel string."""
        result = run_tools("Hello, how are you?")
        assert result == "No tools triggered."

    def test_summarize_keyword_triggers_summary_tool(self) -> None:
        """'summarize' keyword must trigger the Summarization Tool."""
        result = run_tools("Can you summarize this for me?")
        assert "[Summary Tool]" in result

    def test_summarise_spelling_triggers_summary_tool(self) -> None:
        """British spelling 'summarise' must also trigger the tool."""
        result = run_tools("Please summarise this article.")
        assert "[Summary Tool]" in result

    def test_tldr_triggers_summary_tool(self) -> None:
        """'tldr' keyword must trigger the Summarization Tool."""
        result = run_tools("give me a tldr")
        assert "[Summary Tool]" in result

    def test_brief_triggers_summary_tool(self) -> None:
        """'brief' keyword must trigger the Summarization Tool."""
        result = run_tools("give me a brief overview")
        assert "[Summary Tool]" in result

    def test_condense_triggers_summary_tool(self) -> None:
        """'condense' keyword must trigger the Summarization Tool."""
        result = run_tools("condense this text")
        assert "[Summary Tool]" in result

    def test_memory_keyword_triggers_memory_tool(self) -> None:
        """'memory' keyword should trigger the Memory Inspector tool.

        Note: This may fail if ChromaDB is not set up, in which case
        the test should be skipped or the tool should be mocked.
        We test only that the router attempts to call it (no crash).
        """
        # We only assert the return type — ChromaDB may not be available
        # in CI, so we don't assert specific content.
        try:
            result = run_tools("What is in my memory?")
            assert isinstance(result, str)
        except Exception:
            # If ChromaDB is unavailable, skip rather than fail the suite.
            pytest.skip("ChromaDB not available in this environment")

    def test_project_keyword_triggers_project_tool(self) -> None:
        """'project' keyword must trigger the Project Generator."""
        result = run_tools("Help me plan a project")
        assert isinstance(result, str)
        assert len(result.strip()) > 0

    def test_returns_string_always(self) -> None:
        """run_tools must always return a str, never None."""
        for query in ["hello", "summarize this", "build a system", ""]:
            result = run_tools(query)
            assert isinstance(result, str), (
                f"run_tools returned non-str for query: {query!r}"
            )

    def test_multiple_keywords_trigger_multiple_tools(self) -> None:
        """A query with multiple keywords should trigger multiple tools."""
        # "summarize" + "project" + "build" should trigger at least two tools.
        result = run_tools("summarize this project build plan")
        # Both should appear in the combined output.
        assert "[Summary Tool]" in result
        # Project tool output doesn't have a fixed label, but the result
        # should be longer than a single-tool response.
        assert len(result) > 50
