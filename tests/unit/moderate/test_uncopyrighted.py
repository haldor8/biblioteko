from base_test import BaseModerateTest
from cli.moderate import check_book_copyright

class TestPublicDomainBooks(BaseModerateTest):

    def test_les_miserables_public_domain(self):
        """Case: 19th-century classic - Should return False"""
        metadata = {
            "title": "Les Misérables",
            "author": "Victor Hugo",
            "year": "1862"
        }

        # Simulate LLM consensus for public domain
        mock_response = {
            "classification": "likely_public_domain", 
            "reason": "Author died in 1885, work is in the public domain."
        }
        self.mock_gemini.return_value = mock_response
        self.mock_mistral.return_value = mock_response

        # Execute
        result = check_book_copyright(metadata)

        # Assert
        self.assertFalse(result, "Les Misérables should be identified as Public Domain.")

    def test_shakspeare_public_domain(self):
        """Case: Very old work - Should return False"""
        metadata = {
            "title": "Hamlet",
            "author": "William Shakespeare",
            "year": "1603"
        }

        mock_response = {"classification": "likely_public_domain", "reason": "Ancient work."}
        self.mock_gemini.return_value = mock_response
        self.mock_mistral.return_value = mock_response

        self.assertFalse(check_book_copyright(metadata))