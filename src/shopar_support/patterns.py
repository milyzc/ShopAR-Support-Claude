"""Argentine identifiers that llm-guard's default patterns do not cover.

Anonymize only ships NER models for English and Chinese, so local identifiers
are added as regex patterns (regex matching works regardless of language).
The "languages" field must be "en" because that is the scanner's language.
"""

AR_PATTERNS = [
    {
        "name": "AR_DNI",
        "expressions": [r"\b\d{2}\.?\d{3}\.?\d{3}\b"],
        "examples": ["30111222", "30.111.222"],
        "context": ["dni", "documento"],
        "score": 0.75,
        "languages": ["en"],
    },
    {
        "name": "AR_CBU",
        "expressions": [r"\b\d{22}\b"],
        "examples": ["0170099220000011111111"],
        "context": ["cbu", "cuenta"],
        "score": 0.85,
        "languages": ["en"],
    },
]

AR_ENTITY_TYPES = [p["name"] for p in AR_PATTERNS]
