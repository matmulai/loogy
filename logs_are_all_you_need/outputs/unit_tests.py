```python
import unittest

from codebase import search_word_in_dictionary  # Adjust the import based on your file structure

class TestSearchWordInDictionary(unittest.TestCase):
    
    def setUp(self):
        """Set up a sample dictionary for all tests."""
        self.sample_dictionary = {
            "python": "A high-level programming language.",
            "javascript": "A scripting language commonly used in web development.",
            "java": "A high-level, class-based, object-oriented programming language."
        }

    def test_existing_word_case_insensitive(self):
        """Test that a word exists in the dictionary regardless of case."""
        self.assertEqual(search_word_in_dictionary(self.sample_dictionary, "Python"), "A high-level programming language.")
        self.assertEqual(search_word_in_dictionary(self.sample_dictionary, "JAVASCRIPT"), "A scripting language commonly used in web development.")
        self.assertEqual(search_word_in_dictionary(self.sample_dictionary, "JaVa"), "A high-level, class-based, object-oriented programming language.")

    def test_non_existing_word(self):
        """Test searching for a word that does not exist in the dictionary."""
        self.assertIsNone(search_word_in_dictionary(self.sample_dictionary, "ruby"))
        self.assertIsNone(search_word_in_dictionary(self.sample_dictionary, "C++"))

    def test_empty_dictionary(self):
        """Test searching in an empty dictionary."""
        empty_dictionary = {}
        self.assertIsNone(search_word_in_dictionary(empty_dictionary, "Python"))
    
    def test_empty_word(self):
        """Test searching with an empty word."""
        self.assertIsNone(search_word_in_dictionary(self.sample_dictionary, ""))

    def test_special_characters(self):
        """Test searching for a word with special characters."""
        special_dictionary = {
            "hello!": "A greeting used to initiate conversation.",
            "goodbye!": "A parting expression."
        }
        self.assertEqual(search_word_in_dictionary(special_dictionary, "hello!"), "A greeting used to initiate conversation.")
        self.assertIsNone(search_word_in_dictionary(special_dictionary, "hi!"))

    def test_numerical_word(self):
        """Test searching for a word that is a number."""
        number_dictionary = {
            "one": "The first cardinal number.",
            "two": "The second cardinal number."
        }
        self.assertEqual(search_word_in_dictionary(number_dictionary, "ONE"), "The first cardinal number.")
        self.assertIsNone(search_word_in_dictionary(number_dictionary, "three"))

if __name__ == "__main__":
    unittest.main()
```
This comprehensive set of unit tests covers:
1. **Case Insensitivity:** Tests that the search function can find words regardless of their case.
2. **Non-Existing Words:** Validates that looking for words not in the dictionary returns `None`.
3. **Empty Dictionary:** Ensures searching in an empty dictionary correctly returns `None`.
4. **Empty Word Input:** Confirms that an empty search phrase appropriately returns `None`.
5. **Special Characters:** Tests the function's handling of dictionary entries with special characters.
6. **Numerical Words:** Validates that words that are numbers can also be searched in the dictionary.

This set of tests is well-documented, making it easy to understand what each test is verifying, ensuring thorough coverage of edge cases.