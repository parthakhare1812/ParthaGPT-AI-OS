"""
tests/conftest.py
-----------------
Pytest configuration and shared fixtures for the ParthaGPT-AI-OS test suite.

Why this file exists
--------------------
Several backend modules (retriever.py, memory_inspector.py, live_ingest.py)
import ``chromadb`` and ``sentence_transformers`` at module level.  These
packages are not available in lightweight CI environments or developer
machines that have only installed the core dependencies.

To keep the unit-test suite fast and side-effect-free, this conftest uses
``sys.modules`` to inject lightweight stub objects *before* any test module
is imported.  This technique is called "import patching" and is a standard
way to test code that has heavy optional dependencies.

The stubs only need to satisfy the attribute look-ups that happen during
import — they do not need to implement real functionality.

If you later add integration tests that actually need ChromaDB, mark them
with ``@pytest.mark.integration`` and skip them when the real package is
absent.
"""

import sys
import types


def _make_stub_module(name: str, **attrs) -> types.ModuleType:
    """Create a throwaway module with the given attributes.

    Args:
        name (str): The dotted module name (e.g. "chromadb").
        **attrs: Attribute name → value pairs to set on the stub.

    Returns:
        types.ModuleType: A minimal module object that satisfies
                          attribute accesses during import.
    """
    mod = types.ModuleType(name)
    for attr, value in attrs.items():
        setattr(mod, attr, value)
    return mod


# ---------------------------------------------------------------------------
# Stub: chromadb
# We only need the ``Client`` / ``PersistentClient`` classes to be present
# so that ``import chromadb`` and ``chromadb.PersistentClient(...)`` do not
# raise ``AttributeError`` during module-level import in retriever.py.
# ---------------------------------------------------------------------------

class _FakeChromaCollection:
    """Minimal stub for a ChromaDB collection object."""

    def query(self, *args, **kwargs):
        return {"documents": [[]], "metadatas": [[]]}

    def add(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        return {"documents": [], "ids": []}


class _FakeChromaClient:
    """Minimal stub for a ChromaDB client."""

    def get_or_create_collection(self, name: str, *args, **kwargs):
        return _FakeChromaCollection()

    def get_collection(self, name: str, *args, **kwargs):
        return _FakeChromaCollection()


# Register the chromadb stub so any "import chromadb" sees it.
_chromadb_stub = _make_stub_module(
    "chromadb",
    PersistentClient=lambda *a, **kw: _FakeChromaClient(),
    Client=lambda *a, **kw: _FakeChromaClient(),
)
sys.modules.setdefault("chromadb", _chromadb_stub)

# ---------------------------------------------------------------------------
# Stub: sentence_transformers
# retriever.py and ingest.py call SentenceTransformer(model_name).encode().
# The stub returns an empty list for every encode() call.
# ---------------------------------------------------------------------------

class _FakeSentenceTransformer:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, texts, *args, **kwargs):
        # Return a list of zero-vectors, one per input text.
        if isinstance(texts, str):
            return [0.0]
        return [[0.0] for _ in texts]


_st_stub = _make_stub_module(
    "sentence_transformers",
    SentenceTransformer=_FakeSentenceTransformer,
)
sys.modules.setdefault("sentence_transformers", _st_stub)

# ---------------------------------------------------------------------------
# Stub: langchain_text_splitters
# ingest.py uses RecursiveCharacterTextSplitter.
# ---------------------------------------------------------------------------

class _FakeTextSplitter:
    def __init__(self, *args, **kwargs):
        pass

    def split_text(self, text: str):
        # Return the whole text as a single chunk — good enough for import.
        return [text]


_lc_stub = _make_stub_module(
    "langchain_text_splitters",
    RecursiveCharacterTextSplitter=_FakeTextSplitter,
)
sys.modules.setdefault("langchain_text_splitters", _lc_stub)

# ---------------------------------------------------------------------------
# Stub: groq
# chatbot.py and reflection_engine.py import groq at module level.
# ---------------------------------------------------------------------------

class _FakeGroqChat:
    def create(self, *args, **kwargs):
        class _Msg:
            content = "stub response"

        class _Choice:
            message = _Msg()

        class _Resp:
            choices = [_Choice()]

        return _Resp()


class _FakeGroqCompletions:
    chat = property(lambda self: type(
        "_FakeChatNS", (), {"completions": _FakeGroqChat()}
    )())


class _FakeGroqClient:
    def __init__(self, *args, **kwargs):
        self.chat = type(
            "_FakeChatNS",
            (),
            {"completions": _FakeGroqChat()},
        )()


_groq_stub = _make_stub_module("groq", Groq=_FakeGroqClient)
sys.modules.setdefault("groq", _groq_stub)
