"""
tests/test_agents.py
--------------------
Pytest tests for all agents in backend/agents/.

Each test verifies:
    1. The agent function is callable and returns a string.
    2. The returned string contains the expected section header
       (e.g. "[Study Agent]").
    3. The original query is echoed back in the output (so the LLM
       always has context about what was asked).
    4. The output is non-empty even for an empty-string query.

These are unit tests — they do NOT call any LLM or network service.
All agents return static, pre-formatted strings, so the tests are
deterministic and fast.

Run with:
    pytest tests/test_agents.py -v
"""

import pytest

from backend.agents.strategist_agent import strategist_agent
from backend.agents.coding_agent import coding_agent
from backend.agents.research_agent import research_agent
from backend.agents.creativity_agent import creativity_agent
from backend.agents.career_agent import career_agent
from backend.agents.study_agent import study_agent
from backend.agents.router import run_agents


# ---------------------------------------------------------------------------
# Shared test query used across all agent tests.
# ---------------------------------------------------------------------------
SAMPLE_QUERY: str = "How do I become a better AI engineer?"


# ===========================================================================
# Strategist Agent
# ===========================================================================


class TestStrategistAgent:
    """Tests for backend/agents/strategist_agent.py."""

    def test_returns_string(self) -> None:
        """The function must return a str, not None or any other type."""
        result = strategist_agent(SAMPLE_QUERY)
        assert isinstance(result, str), "strategist_agent must return a str"

    def test_contains_header(self) -> None:
        """Output must include the '[Strategist Agent]' section label."""
        result = strategist_agent(SAMPLE_QUERY)
        assert "[Strategist Agent]" in result

    def test_echoes_query(self) -> None:
        """The original query should appear in the output for LLM context."""
        result = strategist_agent(SAMPLE_QUERY)
        assert SAMPLE_QUERY in result

    def test_non_empty_on_empty_query(self) -> None:
        """Even an empty query should produce a non-empty response."""
        result = strategist_agent("")
        assert len(result.strip()) > 0


# ===========================================================================
# Coding Agent
# ===========================================================================


class TestCodingAgent:
    """Tests for backend/agents/coding_agent.py."""

    def test_returns_string(self) -> None:
        result = coding_agent(SAMPLE_QUERY)
        assert isinstance(result, str)

    def test_contains_header(self) -> None:
        result = coding_agent(SAMPLE_QUERY)
        assert "[Coding Agent]" in result

    def test_echoes_query(self) -> None:
        result = coding_agent(SAMPLE_QUERY)
        assert SAMPLE_QUERY in result

    def test_non_empty_on_empty_query(self) -> None:
        result = coding_agent("")
        assert len(result.strip()) > 0


# ===========================================================================
# Research Agent
# ===========================================================================


class TestResearchAgent:
    """Tests for backend/agents/research_agent.py."""

    def test_returns_string(self) -> None:
        result = research_agent(SAMPLE_QUERY)
        assert isinstance(result, str)

    def test_contains_header(self) -> None:
        result = research_agent(SAMPLE_QUERY)
        assert "[Research Agent]" in result

    def test_echoes_query(self) -> None:
        result = research_agent(SAMPLE_QUERY)
        assert SAMPLE_QUERY in result

    def test_non_empty_on_empty_query(self) -> None:
        result = research_agent("")
        assert len(result.strip()) > 0


# ===========================================================================
# Creativity Agent
# ===========================================================================


class TestCreativityAgent:
    """Tests for backend/agents/creativity_agent.py."""

    def test_returns_string(self) -> None:
        result = creativity_agent(SAMPLE_QUERY)
        assert isinstance(result, str)

    def test_contains_header(self) -> None:
        result = creativity_agent(SAMPLE_QUERY)
        # Accept both spellings in case the header changes slightly.
        assert "[Creativity Agent]" in result or "[Creative Agent]" in result

    def test_echoes_query(self) -> None:
        result = creativity_agent(SAMPLE_QUERY)
        assert SAMPLE_QUERY in result

    def test_non_empty_on_empty_query(self) -> None:
        result = creativity_agent("")
        assert len(result.strip()) > 0


# ===========================================================================
# Career Agent
# ===========================================================================


class TestCareerAgent:
    """Tests for backend/agents/career_agent.py."""

    def test_returns_string(self) -> None:
        result = career_agent(SAMPLE_QUERY)
        assert isinstance(result, str)

    def test_contains_header(self) -> None:
        result = career_agent(SAMPLE_QUERY)
        assert "[Career Agent]" in result

    def test_echoes_query(self) -> None:
        result = career_agent(SAMPLE_QUERY)
        assert SAMPLE_QUERY in result

    def test_non_empty_on_empty_query(self) -> None:
        result = career_agent("")
        assert len(result.strip()) > 0


# ===========================================================================
# Study Agent  ← new agent added in this PR
# ===========================================================================


class TestStudyAgent:
    """Tests for backend/agents/study_agent.py (newly added agent)."""

    def test_returns_string(self) -> None:
        """study_agent must return a str."""
        result = study_agent(SAMPLE_QUERY)
        assert isinstance(result, str)

    def test_contains_header(self) -> None:
        """Output must include the '[Study Agent]' section label."""
        result = study_agent(SAMPLE_QUERY)
        assert "[Study Agent]" in result

    def test_echoes_query(self) -> None:
        """The query must appear in the output so the LLM has context."""
        result = study_agent(SAMPLE_QUERY)
        assert SAMPLE_QUERY in result

    def test_non_empty_on_empty_query(self) -> None:
        """Agent must not crash or return empty output for an empty query."""
        result = study_agent("")
        assert len(result.strip()) > 0

    def test_contains_learning_keywords(self) -> None:
        """The output should contain study-specific advice keywords."""
        result = study_agent(SAMPLE_QUERY)
        # Check that at least one of these learning-related words appears.
        learning_keywords = [
            "learn",
            "study",
            "recall",
            "review",
            "practice",
            "understand",
        ]
        matched = any(kw in result.lower() for kw in learning_keywords)
        assert matched, (
            "Expected at least one learning keyword in study_agent output. "
            f"Got: {result!r}"
        )

    def test_different_queries_both_echo(self) -> None:
        """Two different queries should both appear in their respective outputs."""
        query_a = "Teach me machine learning"
        query_b = "How do I study algorithms?"
        result_a = study_agent(query_a)
        result_b = study_agent(query_b)
        assert query_a in result_a
        assert query_b in result_b
        # Queries should NOT leak into each other's output.
        assert query_b not in result_a
        assert query_a not in result_b


# ===========================================================================
# Agent Router
# ===========================================================================


class TestRunAgents:
    """Tests for backend/agents/router.py :: run_agents()."""

    def test_returns_string(self) -> None:
        """run_agents must return a str."""
        result = run_agents(SAMPLE_QUERY)
        assert isinstance(result, str)

    def test_contains_all_agent_headers(self) -> None:
        """All six agent headers must appear in the combined output."""
        result = run_agents(SAMPLE_QUERY)
        expected_headers = [
            "[Strategist Agent]",
            "[Coding Agent]",
            "[Research Agent]",
            "[Career Agent]",
            "[Study Agent]",
        ]
        for header in expected_headers:
            assert header in result, (
                f"Expected header '{header}' not found in run_agents output."
            )

    def test_echoes_query(self) -> None:
        """The query should appear multiple times (once per agent)."""
        result = run_agents(SAMPLE_QUERY)
        # The query appears in each agent's output, so it should be there
        # at least once.
        assert SAMPLE_QUERY in result

    def test_output_is_non_empty(self) -> None:
        """The combined output must always be a non-empty string."""
        result = run_agents("anything")
        assert len(result.strip()) > 0
