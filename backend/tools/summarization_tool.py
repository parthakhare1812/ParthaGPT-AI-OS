"""
summarization_tool.py
---------------------
Text Summarization Tool for ParthaGPT-AI-OS.

This tool condenses a block of text into a shorter, structured summary.
It is designed to be lightweight (no external LLM call) so that it can
run instantly inside the tool_router pipeline.

The tool extracts the most important sentences from the input using a
simple frequency-based scoring algorithm:
    1. Split the text into sentences.
    2. Count how many times each word appears across all sentences
       (ignoring common stop-words).
    3. Score each sentence by summing the frequencies of its words.
    4. Return the top-N highest-scoring sentences in their original order.

This approach — called "extractive summarisation" — is easy to
understand and requires no external libraries beyond the Python
standard library.

Author: SSoC 2026 contributor
"""

import re
import string
from typing import List


# ---------------------------------------------------------------------------
# Common English stop-words to exclude from word-frequency scoring.
# These words (like "the", "is", "and") appear everywhere and would inflate
# scores for sentences that happen to contain many of them.
# ---------------------------------------------------------------------------
_STOP_WORDS: set = {
    "a", "an", "the", "is", "it", "in", "on", "at", "to", "for",
    "of", "and", "or", "but", "with", "this", "that", "was", "are",
    "be", "as", "by", "from", "have", "has", "had", "not", "do",
    "does", "did", "will", "would", "could", "should", "may", "might",
    "its", "their", "they", "we", "you", "i", "he", "she", "his",
    "her", "our", "your", "my", "so", "if", "then", "there", "than",
    "into", "about", "up", "also", "been", "can", "more", "which",
    "when", "who", "what", "how", "all", "no", "just",
}


def _tokenise(text: str) -> List[str]:
    """Split text into lowercase words, removing punctuation.

    Args:
        text (str): Raw input text.

    Returns:
        List[str]: Individual words in lowercase with no punctuation.

    Example:
        >>> _tokenise("Hello, World!")
        ['hello', 'world']
    """
    # Remove all punctuation and convert to lowercase so "AI" and "ai"
    # are treated as the same word.
    cleaned = text.lower().translate(
        str.maketrans("", "", string.punctuation)
    )
    return cleaned.split()


def _split_sentences(text: str) -> List[str]:
    """Split a paragraph into individual sentences.

    Uses a simple regex that splits on '. ', '! ', or '? ' so that
    decimal numbers (e.g. "v2.0") are not incorrectly split.

    Args:
        text (str): A block of text containing one or more sentences.

    Returns:
        List[str]: Each sentence as a separate string (stripped of
                   leading/trailing whitespace).

    Example:
        >>> _split_sentences("Hello world. How are you?")
        ['Hello world', 'How are you?']
    """
    # Split on sentence-ending punctuation followed by a space or
    # end-of-string so we don't break on abbreviations like "Dr. Smith".
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    # Remove blank strings that can appear after splitting.
    return [s.strip() for s in parts if s.strip()]


def summarize_text(text: str, num_sentences: int = 3) -> str:
    """Return an extractive summary of the provided text.

    Scores each sentence by the total frequency of its non-stop-word
    tokens across the full document, then returns the top-scoring
    sentences in their original order.

    Args:
        text (str): The body of text to summarise.  Should be at least
                    a few sentences long for meaningful results.
        num_sentences (int): How many sentences to include in the
                             summary.  Defaults to 3.  If the text
                             contains fewer sentences than this value,
                             all sentences are returned.

    Returns:
        str: A formatted summary string beginning with a header line,
             followed by the selected sentences as a bullet list.
             Returns an error message if ``text`` is empty or
             ``num_sentences`` is less than 1.

    Example:
        >>> text = "AI is transforming industries. It enables automation. " \
        ...        "Machine learning is a key subset of AI. " \
        ...        "Many companies invest heavily in AI research."
        >>> summary = summarize_text(text, num_sentences=2)
        >>> "[Summary]" in summary
        True
    """
    # --- Input validation ---
    if not text or not text.strip():
        return "[Summary Tool]\n\nError: No text provided to summarise."

    if num_sentences < 1:
        return "[Summary Tool]\n\nError: num_sentences must be at least 1."

    sentences = _split_sentences(text)

    # If the text is very short, just return it as-is.
    if len(sentences) <= num_sentences:
        bullet_list = "\n".join(f"- {s}" for s in sentences)
        return f"[Summary Tool]\n\nSummary:\n{bullet_list}"

    # --- Step 1: Count word frequencies across the entire document ---
    # We skip stop-words so that rare, meaningful words score higher.
    word_freq: dict = {}
    for word in _tokenise(text):
        if word not in _STOP_WORDS:
            word_freq[word] = word_freq.get(word, 0) + 1

    # --- Step 2: Score each sentence ---
    # A sentence's score is the sum of the frequencies of its words.
    # We divide by the sentence length to avoid favouring very long
    # sentences that simply contain more words in total.
    sentence_scores: List[tuple] = []
    for idx, sentence in enumerate(sentences):
        words = _tokenise(sentence)
        if not words:
            sentence_scores.append((idx, 0.0))
            continue

        # Sum frequencies of meaningful (non-stop) words only.
        score = sum(
            word_freq.get(w, 0)
            for w in words
            if w not in _STOP_WORDS
        )

        # Normalise by sentence length to penalise very long sentences.
        normalised_score = score / len(words)
        sentence_scores.append((idx, normalised_score))

    # --- Step 3: Pick the top-N sentences ---
    # Sort by score descending, take the best N, then re-sort by original
    # index so the summary reads in the same order as the source text.
    top_sentences = sorted(
        sentence_scores,
        key=lambda x: x[1],
        reverse=True,
    )[:num_sentences]

    # Restore original document order.
    top_sentences_ordered = sorted(top_sentences, key=lambda x: x[0])

    # --- Step 4: Format the output ---
    bullet_list = "\n".join(
        f"- {sentences[idx]}"
        for idx, _ in top_sentences_ordered
    )

    return f"[Summary Tool]\n\nSummary ({num_sentences} key sentences):\n{bullet_list}"
