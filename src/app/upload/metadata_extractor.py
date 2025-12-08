# metadata_extractor.py
import base64
import json
import requests
from mistralai import Mistral
import os


def extract_json_from_llm(text: str) -> dict:
        """
        Extracts the FIRST valid JSON object found in an LLM response.
        - Removes anything before the first '{'
        - Removes anything after the final matching '}'
        - Ignores markdown, code fences, explanations, or embedded text.
        """
        if not text:
            return {"classification": "uncertain", "reason": "Empty LLM response"}

        # 1. Find the first '{'
        start = text.find("{")
        if start == -1:
            return {"classification": "uncertain", "reason": "No JSON object found"}

        # 2. Now walk through text and match braces to find the closing '}'
        brace_count = 0
        end = None

        for i, ch in enumerate(text[start:], start=start):
            if ch == "{":
                brace_count += 1
            elif ch == "}":
                brace_count -= 1
                if brace_count == 0:
                    end = i
                    break

        if end is None:
            return {"classification": "uncertain", "reason": "Malformed JSON response"}

        json_str = text[start:end + 1]

        try:
            return json.loads(json_str)
        except Exception:
            return {"classification": "uncertain", "reason": "Failed to parse JSON"}

class MetadataExtractor:
    """
    Extracts metadata (title, author, year…) from the first 5 pages of a book
    using LLM-based OCR with Gemini or Mistral.
    """

    PROMPT = """
    You are an OCR assistant specialized in extracting book metadata.

    You will receive UP TO 5 IMAGES which correspond to the first pages of a book.

    Your job:
    - Identify the most likely **title**
    - Identify the **author** (or authors)
    - Identify the **publication year** if visible
    - If uncertain, return the closest plausible guess
    - NO explanations
    - Return STRICT JSON ONLY:

    {
        "title": "...",
        "author": "...",
        "year": "..."
    }
    """

    def __init__(self, engine="mistral"):
        self.engine = engine.lower()
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL")

        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.mistral_model = os.getenv("MISTRAL_MODEL")

    # ---------------------------------------------------
    # Helper – prepares an array of inlineData image parts
    # ---------------------------------------------------
    def _prepare_images(self, pages: list[bytes]):
        """Return Gemini/Mistral-ready list of image parts."""
        parts = []
        for page in pages[:2]:  # enforce first 5 pages
            encoded = base64.b64encode(page).decode("utf-8")
            parts.append({
                "inlineData": {
                    "mimeType": "image/jpeg",
                    "data": encoded
                }
            })
        return parts

    # ---------------------------------------------------
    # Gemini
    # ---------------------------------------------------
    def _gemini_extract(self, pages: list[bytes]):
        parts = [{"text": self.PROMPT}] + self._prepare_images(pages)

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.gemini_model}:generateContent?key={self.gemini_key}"
        )

        payload = {
            "contents": [{
                "parts": parts
            }]
        }

        try:
            r = requests.post(url, json=payload, timeout=60)
            data = r.json()

            # Error surface
            if "error" in data:
                print("[GEMINI ERROR]", data["error"])
                return {"title": "Unknown", "author": "Unknown", "year": "Unknown"}

            candidates = data.get("candidates")
            if not candidates:
                print("[GEMINI ERROR] No candidates returned:", data)
                return {"title": "Unknown", "author": "Unknown", "year": "Unknown"}

            parts = candidates[0].get("content", {}).get("parts", [])

            # Find text block and parse JSON
            for p in parts:
                if "text" in p:
                    try:
                        return extract_json_from_llm(p["text"])
                    except Exception:
                        print("[GEMINI ERROR] JSON parse failed:", p["text"])
                        return {"title": "Unknown", "author": "Unknown", "year": "Unknown"}

            print("[GEMINI ERROR] No text parts:", data)
            return {"title": "Unknown", "author": "Unknown", "year": "Unknown"}

        except Exception as e:
            print("[GEMINI EXCEPTION]", e)
            return {"title": "Unknown", "author": "Unknown", "year": "Unknown"}

    # ---------------------------------------------------
    # Mistral
    # ---------------------------------------------------
    def _mistral_extract(self, pages: list[bytes]):
        client = Mistral(api_key=self.mistral_key)

        content_blocks = [{"type": "text", "text": self.PROMPT}]
        for page in pages[:5]:
            encoded = base64.b64encode(page).decode("utf-8")
            content_blocks.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
            })

        resp = client.chat.complete(
            model=self.mistral_model,
            messages=[{
                "role": "user",
                "content": content_blocks
            }]
        )

        text = resp.choices[0].message.content

        try:
            return extract_json_from_llm(text)
        except Exception:
            print("[MISTRAL ERROR] JSON parse failed:", text)
            return {"title": "Unknown", "author": "Unknown", "year": "Unknown"}

    # ---------------------------------------------------
    # Public API
    # ---------------------------------------------------
    def extract_metadata(self, pages: list[bytes]) -> dict:
        """
        pages: list of raw bytes for each uploaded page image.
        Only the first 5 pages are used.
        """
        if self.engine == "gemini":
            return self._gemini_extract(pages)
        else:
            return self._mistral_extract(pages)
