import requests
from bs4 import BeautifulSoup

# -----------------------------
# WEB SEARCH
# -----------------------------

def web_search(query):

    try:

        url = f"https://www.google.com/search?q={query}"

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for g in soup.find_all("h3")[:5]:

            results.append(
                g.get_text()
            )

        if len(results) == 0:

            return "No web results found."

        return "\n".join(results)

    except Exception as e:

        return f"Web search error: {e}"