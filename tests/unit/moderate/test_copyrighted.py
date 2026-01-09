from base_test import BaseModerateTest
from cli.moderate import check_book_copyright

class TestCopyrightedBooks(BaseModerateTest):

    def test_harry_potter_copyright(self):
        """Case: Modern book (1997) - Should return True"""
        metadata = {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J.K. Rowling",
            "year": "1997"
        }

        # Simulate LLM consensus for copyrighted material
        mock_response = {
            "classification": "likely_copyrighted", 
            "reason": "Published recently (1997), author is alive."
        }
        self.mock_gemini.return_value = mock_response
        self.mock_mistral.return_value = mock_response

        # Execute
        result = check_book_copyright(metadata)

        # Assert
        self.assertTrue(result, "Harry Potter should be identified as copyrighted.")

    def test_modern_scientific_book(self):
        """Case: Recent educational book - Should return True"""
        metadata = {
            "title": "A Brief History of Time",
            "author": "Stephen Hawking",
            "year": "1988"
        }

        mock_response = {"classification": "likely_copyrighted", "reason": "Standard copyright duration applies."}
        self.mock_gemini.return_value = mock_response
        self.mock_mistral.return_value = mock_response

        self.assertTrue(check_book_copyright(metadata))