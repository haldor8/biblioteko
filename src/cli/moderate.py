import os
import json
import time
import base64
import requests
from datetime import datetime
from mistralai import Mistral

from dotenv import load_dotenv

from cli.log import Log

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

# ===========================
# LLM COPYRIGHT CHECKER
# ===========================
class CopyrightLLMChecker:
    """
    Asks both Gemini and Mistral to evaluate the copyright status of a book
    using a non-yes/no deterministic prompt.
    """

    PROMPT_TEMPLATE = """
    You are a copyright classification expert.

    You will be given the title of a book and publication details if known.

    Your task is to classify the book into one of these categories **with a short explanation**:

    - "likely_public_domain":  
        The publication date is old enough (typically before 1929 in the U.S.),  
        or known authors have died long enough ago,  
        or the work is known to be public domain.

    - "likely_copyrighted":  
        Published recently, or known to be protected,  
        or falls within standard copyright duration.

    - "uncertain":  
        Not enough information to confidently determine the status.

    **Do not answer yes/no.  
    Return JSON only in the following structure:**

    {
        "classification": "...",
        "reason": "..."
    }

    Book to evaluate:
    "{BOOK_METADATA}"
    """

    def __init__(self):
        load_dotenv()
        # Load keys for both engines
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL")

        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.mistral_model = os.getenv("MISTRAL_MODEL")

        if not all([self.gemini_key, self.gemini_model,
                    self.mistral_key, self.mistral_model]):
            raise ValueError("Missing API keys or model names in environment variables.")

    # ========== Gemini Request ==========
    def ask_gemini(self, metadata: dict):
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.gemini_model}:generateContent?key={self.gemini_key}"
        )

        prompt_text = self.PROMPT_TEMPLATE.replace(
            "{BOOK_METADATA}",
            json.dumps(metadata, indent=2)
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }

        try:
            r = requests.post(url, json=payload, timeout=40)
            r.raise_for_status()
            data = r.json()

            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return extract_json_from_llm(text)

        except Exception as e:
            Log.write(f"[Gemini ERROR] {e}")
            return {"classification": "uncertain", "reason": f"Gemini error: {e}"}

    # ========== Mistral Request ==========
    def ask_mistral(self, metadata: dict):
        try:
            client = Mistral(api_key=self.mistral_key)
            prompt_text = self.PROMPT_TEMPLATE.replace(
                "{BOOK_METADATA}",
                json.dumps(metadata, indent=2)
            )

            resp = client.chat.complete(
                model=self.mistral_model,
                messages=[{
                    "role": "user",
                    "content": prompt_text
                }]
            )

            text = resp.choices[0].message.content
            return extract_json_from_llm(text)

        except Exception as e:
            Log.write(f"[Mistral ERROR] {e}")
            return {"classification": "uncertain", "reason": f"Mistral error: {e}"}

    # ========== Unified verdict ==========
    def evaluate(self, book_title: str):
        gem = self.ask_gemini(book_title)
        mis = self.ask_mistral(book_title)

        return gem, mis


# ===========================
# COPYRIGHT.GOV CHECKER
# ===========================
class CopyrightGovChecker:

    API_URL = (
        "https://api.publicrecords.copyright.gov/"
        "search_service_external/simple_search_dsl?page_number=1&"
        "query={TITLE}&field_type=title&records_per_page=10&sort_order=asc&model="
    )

    def search(self, book_title: str):
        safe_title = book_title.replace(" ", "%20")
        url = self.API_URL.format(TITLE=safe_title)

        try:
            resp = requests.get(url, timeout=40)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            Log.write(f"[Copyright.gov ERROR] {e}")
            return None

    @staticmethod
    def is_still_copyrighted(api_response: dict) -> bool:
        if not api_response or "data" not in api_response:
            return False

        for result in api_response["data"]:
            hit = result.get("hit", {})

            # registration_status = "published" usually means copyrighted
            if hit.get("registration_status") == "published":
                return True

        return False


# ===========================
# MAIN LOGIC
# ===========================
def check_book_copyright(book_metadata: str):

    book_title = book_metadata["title"]
    Log.write(f"Checking copyright status for: {book_title}")

    llm_checker = CopyrightLLMChecker()
    api_checker = CopyrightGovChecker()

    # --- Step 1: LLM evaluation ---
    gemini_result, mistral_result = llm_checker.evaluate(book_metadata)

    Log.write(f"Gemini classification: {gemini_result}")
    Log.write(f"Mistral classification: {mistral_result}")

    # --- Step 2: Copyright.gov API ---
    api_data = api_checker.search(book_title)
    still_copyrighted = api_checker.is_still_copyrighted(api_data)

    Log.write(f"Copyright.gov says copyrighted: {still_copyrighted}")

    # --- Final verdict ---
    if still_copyrighted:
        Log.write(f"FINAL VERDICT: '{book_title}' IS COPYRIGHTED.\n")
        return True

    # If BOTH LLMs say likely copyrighted → trust majority
    llm_votes = [
        gemini_result.get("classification"),
        mistral_result.get("classification")
    ]

    if llm_votes.count("likely_copyrighted") >= 2:
        Log.write(f"FINAL VERDICT: '{book_title}' is LIKELY copyrighted (LLM consensus).\n")
        return True

    Log.write(f"FINAL VERDICT: '{book_title}' appears NON-COPYRIGHTED.\n")
    return False


# ===========================
# CLI ENTRY POINT
# ===========================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python moderate.py \"Book Title Here\"")
        exit(1)

    title = " ".join(sys.argv[1:])
    check_book_copyright(title)
