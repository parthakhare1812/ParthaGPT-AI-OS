# -----------------------------
# DETECT PERSONALITY MODE
# -----------------------------

def detect_personality_mode(query):

    query = query.lower()

    # -----------------------------
    # TECHNICAL MODE
    # -----------------------------

    if any(word in query for word in [
        "error",
        "bug",
        "fix",
        "flask",
        "code",
        "backend",
        "frontend",
        "python",
        "debug"
    ]):

        return {
            "mode": "technical",
            "tone": "precise technical assistant",
            "style": "concise and solution-oriented"
        }

    # -----------------------------
    # FUTURISTIC MODE
    # -----------------------------

    elif any(word in query for word in [
        "startup",
        "future",
        "innovation",
        "agent",
        "ai system",
        "autonomous",
        "vision"
    ]):

        return {
            "mode": "futuristic",
            "tone": "visionary AI strategist",
            "style": "ambitious and futuristic"
        }

    # -----------------------------
    # CAREER MODE
    # -----------------------------

    elif any(word in query for word in [
        "career",
        "resume",
        "placement",
        "internship",
        "job",
        "interview"
    ]):

        return {
            "mode": "career",
            "tone": "professional mentor",
            "style": "structured and growth-oriented"
        }

    # -----------------------------
    # REFLECTIVE MODE
    # -----------------------------

    elif any(word in query for word in [
        "stuck",
        "motivation",
        "confused",
        "mindset",
        "growth",
        "discipline"
    ]):

        return {
            "mode": "reflective",
            "tone": "supportive mentor",
            "style": "thoughtful and reflective"
        }

    # -----------------------------
    # DEFAULT MODE
    # -----------------------------

    return {
        "mode": "default",
        "tone": "intelligent AI clone",
        "style": "structured and futuristic"
    }